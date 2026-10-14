import json
import re
from urllib.parse import urljoin

from django.conf import settings
from django.utils.safestring import mark_safe

from backend.seo.blog import get_blog_seo_data
from backend.seo.faq import get_faq_seo_data

DEFAULT_TITLE = (
    "Stop Dépôt Sauvage - Accompagner les collectivités pour mieux lutter contre "
    "les dépôts sauvages."
)
DEFAULT_DESCRIPTION = "Signaler un dépôt sauvage avec Stop Dépôt Sauvage."
SITE_NAME = "Stop Dépôt Sauvage"

# Authenticated or backoffice pages excluded from search engine indexing even in production.
PRIVATE_PATH_PREFIXES = (
    "/mes-procedures",
    "/suivi-procedure/",
    "/constatation",
    "/constatation-fin/",
    "/tableau-de-bord",
    "/backoffice",
    "/procedures-liste",
    "/procedure-detail/",
    "/login-demo",
)

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
    (
        r"^/blog$",
        {
            "title": "Blog & Retours d'expérience - Stop Dépôt Sauvage",
            "desc": "Conseils pratiques et retours d'expérience pour aider les communes à traiter leurs dépôts sauvages par la voie administrative.",
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


def normalize_path(path):
    normalized_path = "/" + path.strip("/")
    if normalized_path == "//":
        normalized_path = "/"
    return normalized_path


def is_private_path(path):
    """Returns True if the path should remain excluded from search engine index."""
    return normalize_path(path).startswith(PRIVATE_PATH_PREFIXES)


def get_seo_data(path):
    normalized_path = normalize_path(path)
    faq_seo = get_faq_seo_data(normalized_path)
    if faq_seo:
        return faq_seo
    blog_seo = get_blog_seo_data(normalized_path)
    if blog_seo:
        return blog_seo
    for pattern, seo_data in SEO_PATTERNS:
        if re.match(pattern, normalized_path):
            return seo_data
    return None


def is_production():
    """Returns True if the current environment is production."""
    return "prod" in getattr(settings, "ENV_NAME", "").lower()


def absolute_url(path_or_url):
    """Resolves a relative path to a full public URL using SITE_BASE_URL."""
    if not path_or_url:
        return None
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    return urljoin(settings.SITE_BASE_URL.rstrip("/") + "/", path_or_url.lstrip("/"))


def build_article_jsonld(seo_data, canonical, image):
    """Builds schema.org BlogPosting structured data for search engines."""
    jsonld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": seo_data.get("title"),
        "description": seo_data.get("desc"),
        "mainEntityOfPage": canonical,
        "url": canonical,
        "inLanguage": "fr-FR",
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": settings.SITE_BASE_URL,
        },
    }
    if image:
        jsonld["image"] = image
    if seo_data.get("published_time"):
        jsonld["datePublished"] = seo_data["published_time"]
    if seo_data.get("modified_time"):
        jsonld["dateModified"] = seo_data["modified_time"]
    return jsonld


def build_seo_context(path):
    """Builds complete SEO template context (tags, canonical, robots, OG, and JSON-LD)."""
    seo_data = get_seo_data(path) or {}
    canonical = absolute_url(normalize_path(path))
    image = absolute_url(seo_data.get("image") or settings.SEO_DEFAULT_IMAGE)
    context = {
        "seo_title": seo_data.get("title") or DEFAULT_TITLE,
        "seo_description": seo_data.get("desc") or DEFAULT_DESCRIPTION,
        "seo_site_name": SITE_NAME,
        "seo_robots": (
            "index, follow" if is_production() and not is_private_path(path) else "noindex, nofollow"
        ),
        "seo_canonical": canonical,
        "seo_og_type": seo_data.get("og_type", "website"),
        "seo_image": image,
    }
    if seo_data.get("og_type") == "article":
        context["seo_published_time"] = seo_data.get("published_time")
        context["seo_modified_time"] = seo_data.get("modified_time")
        jsonld = build_article_jsonld(seo_data, canonical, image)
        # Escape '</' sequence to prevent prematurely closing script tags
        context["seo_jsonld"] = mark_safe(
            json.dumps(jsonld, ensure_ascii=False).replace("<", "\\u003C")
        )
    return context
