import logging
import math
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"

# Table de synonymes métier pour relier le vocabulaire usager aux fiches juridiques
SYNONYMS_MAP = {
    "mettre": ["amende", "sanction", "montant", "calculateur"],
    "amender": ["amende", "sanctionner", "calculateur"],
    "tarif": ["bareme", "grille", "montant", "amende", "calculateur"],
    "lrar": ["recommande", "lettre", "information", "ar", "contradictoire", "notification"],
    "pli": ["recommande", "non_reclame", "ar", "presentation", "contradictoire"],
    "npai": ["adresse", "introuvable", "inconnue", "recherche", "procureur"],
    "camera": ["videoprotection", "chasse", "piege", "preuve", "images"],
    "fouiller": ["sacs", "fouille", "commissionnement", "indices", "dechets"],
    "fouille": ["fouiller", "sacs", "indices", "preuves"],
    "plaque": ["immatriculation", "siv", "gendarmerie", "vehicule"],
    "carcasse": ["vhu", "epave", "vehicule", "dangereux"],
    "gravats": ["inertes", "volume", "dechets", "metre_cube", "m3"],
    "rediger": ["rapport", "constat", "brouillon", "modeles"],
    "redaction": ["rapport", "constat", "brouillon", "modeles"],
    "ecrire": ["rediger", "rapport", "constat"],
    "modele": ["modeles", "trame", "document", "lettre", "rapport", "arrete"],
    "modeles": ["modele", "trame", "document", "lettre", "rapport", "arrete"],
    "rapport": ["constat", "constatation", "rediger", "modele"],
    "constat": ["rapport", "constatation", "brouillon", "rediger"],
    "constatation": ["rapport", "constat", "brouillon", "rediger"],
    "photo": ["photos", "preuve", "constat", "rapport", "photographie", "indices"],
    "photos": ["photo", "preuve", "constat", "rapport", "photographie", "indices"],
}


class KnowledgeRetriever:
    """
    Indexeur et moteur de recherche documentaire léger (BM25 simplifié)
    pour les FAQ, modèles ODT et guides du chatbot.
    Exclut par défaut les sections destinées aux citoyens non-collectivités.
    """

    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        self.documents: List[Dict[str, Any]] = []
        self._load_documents()

    def _normalize(self, text: str) -> str:
        """Supprime les accents et met en minuscules."""
        nfkd = unicodedata.normalize("NFKD", text)
        no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
        return re.sub(r"[^\w\s]", " ", no_accents.lower())

    def _tokenize(self, text: str) -> List[str]:
        cleaned = self._normalize(text)
        tokens = cleaned.split()
        stopwords = {
            "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "et", "ou",
            "en", "a", "dans", "par", "pour", "sur", "avec", "sans", "sous", "ce",
            "cet", "cette", "ces", "qui", "que", "quoi", "dont", "ou", "est", "sont",
            "ont", "au", "aux", "il", "ils", "elle", "elles", "on", "nous", "vous",
            "se", "sa", "son", "ses", "leur", "leurs", "ne", "pas", "plus", "je", "tu",
            "comment", "faire", "peut", "quelles", "quel", "quelle", "quels"
        }
        return [t for t in tokens if len(t) > 2 and t not in stopwords]

    def _load_documents(self):
        self.documents = []
        if not self.knowledge_dir.exists():
            logger.warning("Knowledge directory not found: %s", self.knowledge_dir)
            return

        for file_path in self.knowledge_dir.rglob("*"):
            if "raw" in file_path.parts:
                continue
            if not file_path.is_file() or file_path.suffix not in (".md", ".txt"):
                continue

            # Ne pas indexer la FAQ destinée aux citoyens non-collectivités
            if "vous_n_êtes_pas_une_collectivité" in file_path.stem:
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                if "faq" in file_path.parts:
                    sections = re.split(r"\n(?=##\s+)", content)
                    for sec in sections:
                        sec_str = sec.strip()
                        if not sec_str or sec_str.startswith("# FAQ -"):
                            continue
                        lines = sec_str.split("\n", 1)
                        header_line = lines[0].replace("#", "").strip()
                        # Extraire le slug si présent sous la forme <!-- slug: ... -->
                        slug_match = re.search(r"<!--\s*slug:\s*([^\s>]+)\s*-->", header_line)
                        slug = slug_match.group(1) if slug_match else ""
                        title = re.sub(r"<!--.*?-->", "", header_line).strip()
                        tokens = set(self._tokenize(sec_str))
                        self.documents.append({
                            "title": title,
                            "slug": slug,
                            "url": f"/faq/{slug}" if slug else "/faq",
                            "source": f"FAQ ({file_path.stem})",
                            "content": sec_str,
                            "tokens": tokens,
                        })
                elif "blog" in file_path.parts:
                    lines = content.strip().split("\n", 1)
                    title = lines[0].replace("#", "").strip() if lines else file_path.stem
                    slug = file_path.stem
                    tokens = set(self._tokenize(content))
                    self.documents.append({
                        "title": title,
                        "slug": slug,
                        "url": f"/blog/{slug}",
                        "source": f"blog/{file_path.name}",
                        "content": content,
                        "tokens": tokens,
                    })
                elif "custom" in file_path.parts and "README" not in file_path.name:
                    # Découper les gros guides custom en sections H2 pour un ciblage précis
                    sections = re.split(r"\n(?=##\s+)", content)
                    main_title = ""
                    for i, sec in enumerate(sections):
                        sec_str = sec.strip()
                        if not sec_str:
                            continue
                        lines = sec_str.split("\n", 1)
                        header_line = lines[0].replace("#", "").strip()
                        if i == 0 and sec_str.startswith("# "):
                            main_title = header_line
                        title = f"{main_title} - {header_line}" if main_title and i > 0 else header_line
                        tokens = set(self._tokenize(sec_str))
                        self.documents.append({
                            "title": title,
                            "slug": "",
                            "url": "/comprendre-la-procedure",
                            "source": f"Guide ({file_path.stem})",
                            "content": sec_str,
                            "tokens": tokens,
                        })
                else:
                    lines = content.strip().split("\n", 1)
                    title = lines[0].replace("#", "").strip() if lines else file_path.stem
                    tokens = set(self._tokenize(content))
                    self.documents.append({
                        "title": title,
                        "slug": "",
                        "url": "/comprendre-la-procedure",
                        "source": f"{file_path.parent.name}/{file_path.name}",
                        "content": content,
                        "tokens": tokens,
                    })
            except Exception as e:
                logger.error("Error reading knowledge file %s: %s", file_path, e)

        logger.info("Loaded %d knowledge chunks for chatbot", len(self.documents))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Recherche les k documents les plus pertinents pour la requête,
        avec expansion par synonymes.
        """
        raw_tokens = self._tokenize(query)
        if not raw_tokens or not self.documents:
            return []

        expanded_tokens = list(raw_tokens)
        for t in raw_tokens:
            if t in SYNONYMS_MAP:
                expanded_tokens.extend(SYNONYMS_MAP[t])

        query_tokens = set(expanded_tokens)

        scored_docs: List[Tuple[float, Dict[str, Any]]] = []
        for doc in self.documents:
            doc_tokens = doc["tokens"]
            common_tokens = query_tokens.intersection(doc_tokens)
            if not common_tokens:
                continue

            score = len(common_tokens)
            title_tokens = set(self._tokenize(doc["title"]))
            title_intersection = query_tokens.intersection(title_tokens)
            score += len(title_intersection) * 3.5  # Bonus fort sur le titre

            # Normalisation par la longueur
            score = score / (math.log(len(doc_tokens) + 10) + 1.0)
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:top_k]]



# Instance singleton
_retriever: Optional[KnowledgeRetriever] = None


def get_retriever() -> KnowledgeRetriever:
    global _retriever
    if _retriever is None:
        _retriever = KnowledgeRetriever()
    return _retriever
