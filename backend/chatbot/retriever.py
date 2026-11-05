import logging
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"


class KnowledgeRetriever:
    """
    Indexeur et moteur de recherche documentaire léger (BM25 simplifié)
    pour les FAQ, modèles ODT et guides du chatbot.
    """

    def __init__(self, knowledge_dir: Path = KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir
        self.documents: List[Dict[str, str]] = []  # {"title": ..., "source": ..., "content": ..., "tokens": set()}
        self._load_documents()

    def _tokenize(self, text: str) -> List[str]:
        # Minuscules, élimination des caractères spéciaux
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = cleaned.split()
        # Filtrage des petits mots vides français courants
        stopwords = {
            "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "et", "ou",
            "en", "à", "dans", "par", "pour", "sur", "avec", "sans", "sous", "ce",
            "cet", "cette", "ces", "qui", "que", "quoi", "dont", "où", "est", "sont",
            "a", "ont", "au", "aux", "il", "ils", "elle", "elles", "on", "nous", "vous",
            "se", "sa", "son", "ses", "leur", "leurs", "ne", "pas", "plus", "je", "tu"
        }
        return [t for t in tokens if len(t) > 2 and t not in stopwords]

    def _load_documents(self):
        self.documents = []
        if not self.knowledge_dir.exists():
            logger.warning("Knowledge directory not found: %s", self.knowledge_dir)
            return

        # Parcours récursif de tous les fichiers .md et .txt (hors raw/)
        for file_path in self.knowledge_dir.rglob("*"):
            if "raw" in file_path.parts:
                continue
            if not file_path.is_file() or file_path.suffix not in (".md", ".txt"):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                # Si c'est un fichier FAQ avec plusieurs Q/R découpées par '## '
                if "faq" in file_path.parts:
                    sections = re.split(r"\n(?=##\s+)", content)
                    for sec in sections:
                        sec_str = sec.strip()
                        if not sec_str or sec_str.startswith("# FAQ -"):
                            continue
                        lines = sec_str.split("\n", 1)
                        title = lines[0].replace("#", "").strip()
                        tokens = set(self._tokenize(sec_str))
                        self.documents.append({
                            "title": title,
                            "source": f"FAQ ({file_path.stem})",
                            "content": sec_str,
                            "tokens": tokens,
                        })
                else:
                    # Modèles, Blog ou Guides Custom
                    lines = content.strip().split("\n", 1)
                    title = lines[0].replace("#", "").strip() if lines else file_path.stem
                    # Pour les gros articles de blog ou modèles, on conserve l'ensemble ou on découpe
                    tokens = set(self._tokenize(content))
                    self.documents.append({
                        "title": title,
                        "source": f"{file_path.parent.name}/{file_path.name}",
                        "content": content,
                        "tokens": tokens,
                    })
            except Exception as e:
                logger.error("Error reading knowledge file %s: %s", file_path, e)

        logger.info("Loaded %d knowledge chunks for chatbot", len(self.documents))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        Recherche les k documents les plus pertinents pour la requête.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens or not self.documents:
            return []

        scored_docs: List[Tuple[float, Dict[str, str]]] = []
        for doc in self.documents:
            # Score par recouvrement de tokens avec bonus si le terme est dans le titre
            doc_tokens = doc["tokens"]
            common_tokens = set(query_tokens).intersection(doc_tokens)
            if not common_tokens:
                continue

            score = len(common_tokens)
            title_tokens = set(self._tokenize(doc["title"]))
            title_intersection = set(query_tokens).intersection(title_tokens)
            score += len(title_intersection) * 2.5  # Bonus fort sur le titre

            # Normalisation légère par la longueur pour ne pas toujours favoriser les très longs textes
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
