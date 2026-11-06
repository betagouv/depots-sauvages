#!/usr/bin/env python3
"""Script de test et d'évaluation interactive de l'assistant IA Stop Dépôt Sauvage.

Permet de jouer des scénarios réalistes multi-tours face au véritable LLM configuré
dans ChatbotConfig (ex: Albert / Mistral ou OpenAI) ou en mode interactif.

Usage :
    pipenv run python scripts/eval_chatbot_scenarios.py [--scenario SCENARIO_ID] [--interactive]
"""

import argparse
import json
import os
import sys
import time

import django

# Initialisation Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.local")
django.setup()

from backend.chatbot.adapters import get_ai_adapter
from backend.chatbot.models import ChatbotConfig


SCENARIOS = [
    {
        "id": "constatation_complete",
        "title": "Axe 1 : Dépôt important -> Collecte progressive & brouillon avec volume m3",
        "description": "Un agent de voirie signale un dépôt important sans donner tous les détails au premier message.",
        "turns": [
            "Bonjour, on a un gros dépôt sauvage découvert ce matin sur la commune de Saint-Priest, des gravats avec du fibrociment.",
            "C'est au bord du chemin communal des Chênes, sur le domaine public. On a estimé ça à environ une benne de 15 m3. Et en regardant dedans, on a trouvé des courriers au nom d'une entreprise du coin !",
        ],
        "eval_criteria": {
            "propose_constatation": True,
            "volume_m3_expected": 15.0,
            "types_expected": ["Gravats", "Amiante"],
            "has_link_demarrer": "/demarrer-constatation",
        },
    },
    {
        "id": "constatation_petit_volume",
        "title": "Axe 1 bis : Petit dépôt du quotidien (sacs, matelas) -> Brouillon < 1m3",
        "description": "Un élu trouve quelques sacs poubelles et un vieux matelas abandonnés.",
        "turns": [
            "Un administré m'a signalé 4 sacs poubelles noirs et un vieux matelas jetés dans un fossé près de la mairie à Belleville.",
        ],
        "eval_criteria": {
            "propose_constatation": True,
            "volume_m3_max": 2.0,
            "types_expected": ["Ordures ménagères", "Encombrants"],
        },
    },
    {
        "id": "orientation_contact_humain",
        "title": "Axe 2 : Cas complexe / contentieux -> Orientation équipe & webinaire",
        "description": "Un maire est confronté à un contrevenant récalcitrant avec avocat et une situation bloquée.",
        "turns": [
            "Bonjour. Nous avons mis en demeure un professionnel pour 50 m3 de déchets, mais son avocat conteste la procédure administrative et menace d'attaquer la commune au tribunal administratif. La gendarmerie refuse de prendre la plainte. Que faire ?",
        ],
        "eval_criteria": {
            "mentions_contact": "/contact",
            "mentions_rdv": "/rdv",
        },
    },
    {
        "id": "pedagogie_sources_reelles",
        "title": "Axe 3 : Pédagogie juridique -> Sources réelles sans hallucination",
        "description": "Un garde champêtre demande si on a le droit d'ouvrir les sacs pour trouver des preuves.",
        "turns": [
            "Est-ce que j'ai légalement le droit de fouiller des sacs poubelles pour chercher des factures ou des lettres ?",
            "Quelles sont vos sources officielles sur ce point ?",
        ],
        "eval_criteria": {
            "expected_url_substr": "/faq/",
            "no_hallucinated_domains": ["help.", "antidepot", "stop-depot"],
        },
    },
    {
        "id": "calculateur_et_amende",
        "title": "Axe 3 bis : Évaluation de l'amende administrative et barème municipal",
        "description": "Un secrétaire de mairie demande si le conseil municipal peut voter un tarif fixe de 500 € par dépôt.",
        "turns": [
            "Notre conseil municipal veut voter un barème fixe de 500 € pour tout dépôt sauvage dans la commune. Est-ce légal et comment calculer l'amende ?",
        ],
        "eval_criteria": {
            "mentions_individualisation": True,
            "mentions_calculateur": "/calculateur",
            "mentions_formule": "250",
        },
    },
]


def run_scenario(scenario: dict, adapter, delay: float = 0.5):
    print("\n" + "=" * 80)
    print(f"🎬 SCÉNARIO : {scenario['title']}")
    print(f"ℹ️  {scenario['description']}")
    print("=" * 80)

    messages = []
    total_tools_called = []

    for turn_idx, user_text in enumerate(scenario["turns"], 1):
        print(f"\n👤 [Tour {turn_idx}] Usager :")
        print(f"   {user_text}\n")
        messages.append({"role": "user", "content": user_text})

        print(f"🤖 [Tour {turn_idx}] Assistant IA :")
        assistant_content = ""
        turn_tools = []

        try:
            for raw_event in adapter.stream_chat(messages=messages):
                for line in raw_event.strip().split("\n"):
                    if not line.startswith("data: "):
                        continue
                    payload_str = line[6:].strip()
                    if not payload_str or payload_str == "[DONE]":
                        continue
                    try:
                        event = json.loads(payload_str)
                    except json.JSONDecodeError:
                        continue

                    evt_type = event.get("type")
                    if evt_type == "text-delta":
                        chunk = event.get("delta", "")
                        assistant_content += chunk
                        print(chunk, end="", flush=True)
                    elif evt_type == "tool-input-available":
                        turn_tools.append(event)
                        total_tools_called.append(event)
                        print(f"\n   ⚙️ [TOOL CALL DÉTECTÉ] {event.get('toolName')}:")
                        print(f"      {json.dumps(event.get('input', {}), indent=6, ensure_ascii=False)}")
        except Exception as e:
            print(f"\n❌ Erreur lors de l'appel LLM : {e}")

        print("\n")
        messages.append({"role": "assistant", "content": assistant_content})
        time.sleep(delay)

    # Analyse des critères
    print("📋 ÉVALUATION DU SCÉNARIO :")
    crit = scenario.get("eval_criteria", {})
    all_text = " ".join(m["content"] for m in messages if m["role"] == "assistant")

    if crit.get("propose_constatation"):
        has_tool = any(t.get("toolName") == "propose_constatation_draft" for t in total_tools_called)
        status = "✅ OK" if has_tool else "⚠️ Non détecté"
        print(f"  - Déclenchement brouillon de constatation : {status}")

        if has_tool and "volume_m3_expected" in crit:
            last_draft = [t for t in total_tools_called if t.get("toolName") == "propose_constatation_draft"][-1]
            vol = last_draft.get("input", {}).get("volumeM3")
            expected_vol = crit["volume_m3_expected"]
            v_status = "✅ OK" if vol == expected_vol else f"⚠️ Trouvé {vol} m³, attendu {expected_vol} m³"
            print(f"  - Précision volume m³ : {v_status}")

    if "mentions_contact" in crit:
        has_c = crit["mentions_contact"] in all_text
        print(f"  - Orientation vers contact ({crit['mentions_contact']}) : {'✅ OK' if has_c else '⚠️ Absent'}")

    if "mentions_rdv" in crit:
        has_r = crit["mentions_rdv"] in all_text
        print(f"  - Orientation vers webinaire ({crit['mentions_rdv']}) : {'✅ OK' if has_r else '⚠️ Absent'}")

    if "mentions_calculateur" in crit:
        has_calc = crit["mentions_calculateur"] in all_text
        print(f"  - Mention du calculateur (/calculateur) : {'✅ OK' if has_calc else '⚠️ Absent'}")

    if "expected_url_substr" in crit:
        has_faq = crit["expected_url_substr"] in all_text
        print(f"  - Lien officiel vérifié ({crit['expected_url_substr']}) : {'✅ OK' if has_faq else '⚠️ Absent'}")

    if "no_hallucinated_domains" in crit:
        hallucinated = [d for d in crit["no_hallucinated_domains"] if d in all_text]
        h_status = "✅ Aucun domaine fictif" if not hallucinated else f"❌ Hallucination détectée : {hallucinated}"
        print(f"  - Absence de faux domaines : {h_status}")


def run_interactive(adapter):
    print("\n" + "=" * 80)
    print("💬 MODE INTERACTIF - TEST DIRECT DE L'ASSISTANT IA")
    print("Tapez 'exit' ou 'quit' pour quitter, 'clear' pour réinitialiser la conversation.")
    print("=" * 80)

    messages = []
    while True:
        try:
            user_input = input("\n👤 Vous > ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break
        if user_input.lower() == "clear":
            messages = []
            print("🧹 Conversation réinitialisée.")
            continue

        messages.append({"role": "user", "content": user_input})
        print("\n🤖 Assistant > ", end="", flush=True)

        assistant_content = ""
        for raw_event in adapter.stream_chat(messages=messages):
            for line in raw_event.strip().split("\n"):
                if not line.startswith("data: "):
                    continue
                payload_str = line[6:].strip()
                if not payload_str or payload_str == "[DONE]":
                    continue
                try:
                    event = json.loads(payload_str)
                except json.JSONDecodeError:
                    continue

                if event.get("type") == "text-delta":
                    chunk = event.get("delta", "")
                    assistant_content += chunk
                    print(chunk, end="", flush=True)
                elif event.get("type") == "tool-input-available":
                    print(f"\n   ⚙️ [TOOL CALL] {event.get('toolName')} : {json.dumps(event.get('input', {}), ensure_ascii=False)}")

        print("\n")
        messages.append({"role": "assistant", "content": assistant_content})


def main():
    parser = argparse.ArgumentParser(description="Évaluation de l'assistant IA Stop Dépôt Sauvage sur des scénarios terrain.")
    parser.add_argument("--scenario", choices=[s["id"] for s in SCENARIOS] + ["all"], default="all", help="Identifiant du scénario à exécuter")
    parser.add_argument("--interactive", action="store_true", help="Lancer en mode conversationnel libre")
    args = parser.parse_args()

    cfg = ChatbotConfig.get_solo()
    print(f"⚙️ Fournisseur IA : {cfg.provider} ({cfg.model}) sur {cfg.base_url}")
    adapter = get_ai_adapter()

    if args.interactive:
        run_interactive(adapter)
    else:
        to_run = SCENARIOS if args.scenario == "all" else [s for s in SCENARIOS if s["id"] == args.scenario]
        for s in to_run:
            run_scenario(s, adapter)


if __name__ == "__main__":
    main()
