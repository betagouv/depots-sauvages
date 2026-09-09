import re

from backend.seo.faq import get_faq_seo_data

SEO_PATTERNS = [
    # Pages statiques
    (
        r"^/$",
        {
            "title": "Stop Dépôt Sauvage - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.",
            "desc": "Signaler un dépôt sauvage avec Stop Dépôt Sauvage.",
        },
    ),
    (
        r"^/simulateur$",
        {
            "title": "Simulateur d'éligibilité à la procédure administrative - Stop Dépôt Sauvage",
            "desc": "Répondez à quelques questions, en 1 minute, pour savoir si Stop Dépôt Sauvage peut vous aider à agir efficacement.",
        },
    ),
    (
        r"^/calculateur$",
        {
            "title": "Calculateur d'amende administrative - Stop Dépôt Sauvage",
            "desc": "Evaluer le montant de l'amende que vous pouvez émettre en cas de dépôt sauvage",
        },
    ),
    (
        r"^/comprendre-la-procedure$",
        {
            "title": "Comprendre la procédure - Stop Dépôt Sauvage",
            "desc": "Découvrez comment fonctionne la procédure de lutte contre les dépôts sauvages.",
        },
    ),
    (
        r"^/mes-procedures$",
        {
            "title": "Mes procédures - Stop Dépôt Sauvage",
            "desc": "Consultez et suivez l'avancement de vos procédures de constatation.",
        },
    ),
    (
        r"^/contact$",
        {
            "title": "Contact - Stop Dépôt Sauvage",
            "desc": "Contactez l'équipe de Stop Dépôt Sauvage.",
        },
    ),
    (
        r"^/demarche-numerique-rejoindre-(?:protectenvi|stop-depot-sauvage)$",
        {
            "title": "Rejoindre le dispositif - Stop Dépôt Sauvage",
            "desc": "Rejoignez le dispositif Stop Dépôt Sauvage pour lutter contre les dépôts sauvages.",
        },
    ),
    (
        r"^/rdv$",
        {
            "title": "Participez à notre webinaire - Stop Dépôt Sauvage",
            "desc": "Inscrivez-vous gratuitement à notre webinaire hebdomadaire pour comprendre comment agir contre les dépôts sauvages.",
        },
    ),
    (
        r"^/comment-agir$",
        {
            "title": "Comment agir contre les dépôts sauvages ? - Stop Dépôt Sauvage",
            "desc": "Découvrez comment une collectivité peut agir efficacement contre les dépôts sauvages.",
        },
    ),
    (
        r"^/login-demo$",
        {
            "title": "Connexion démo - Stop Dépôt Sauvage",
            "desc": "Connectez-vous à l'espace de démonstration de Stop Dépôt Sauvage.",
        },
    ),
    (
        r"^/demarrer-constatation$",
        {
            "title": "Démarrer une constatation - Stop Dépôt Sauvage",
            "desc": "Démarrer une nouvelle constatation de dépôt sauvage.",
        },
    ),
    (
        r"^/constatation$",
        {
            "title": "Créer une constatation - Stop Dépôt Sauvage",
            "desc": "Remplir le formulaire de constatation de dépôt sauvage.",
        },
    ),
    (
        r"^/faq$",
        {
            "title": "Foire Aux Questions - Stop Dépôt Sauvage",
            "desc": "Retrouvez toutes les réponses aux questions les plus fréquentes sur la lutte contre les dépôts sauvages.",
        },
    ),
    # Pages dynamiques avec identifiants
    (
        r"^/suivi-procedure/[^/]+$",
        {
            "title": "Suivi de procédure - Stop Dépôt Sauvage",
            "desc": "Suivez l'avancement de cette procédure de constatation.",
        },
    ),
    (
        r"^/constatation-fin/[^/]+$",
        {
            "title": "Constatation enregistrée - Stop Dépôt Sauvage",
            "desc": "Votre constatation de dépôt sauvage a été enregistrée avec succès.",
        },
    ),
    (
        r"^/constatation/[^/]+$",
        {
            "title": "Modifier la constatation - Stop Dépôt Sauvage",
            "desc": "Modifier les détails de la constatation de dépôt sauvage.",
        },
    ),
]


def get_seo_data(path):
    normalized_path = "/" + path.strip("/")
    if normalized_path == "//":
        normalized_path = "/"
    # Dynamic FAQ metadata
    faq_seo = get_faq_seo_data(normalized_path)
    if faq_seo:
        return faq_seo
    for pattern, seo_data in SEO_PATTERNS:
        if re.match(pattern, normalized_path):
            return seo_data
    return None
