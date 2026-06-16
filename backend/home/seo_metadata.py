import re

SEO_PATTERNS = [
    # Pages statiques
    (
        r"^/$",
        {
            "title": "Protect’Envi - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.",
            "desc": "Signaler un dépôt sauvage avec Protect'Envi.",
        },
    ),
    (
        r"^/simulateur$",
        {
            "title": "Simulateur d'amende pour dépôt sauvage - Protect'Envi",
            "desc": "Simulez le montant de l'amende pour un dépôt sauvage avec Protect'Envi.",
        },
    ),
    (
        r"^/calculateur$",
        {
            "title": "Calculateur de préjudice écologique - Protect'Envi",
            "desc": "Calculez le préjudice écologique d'un dépôt sauvage avec Protect'Envi.",
        },
    ),
    (
        r"^/comprendre-la-procedure$",
        {
            "title": "Comprendre la procédure - Protect'Envi",
            "desc": "Découvrez comment fonctionne la procédure de lutte contre les dépôts sauvages.",
        },
    ),
    (
        r"^/mes-procedures$",
        {
            "title": "Mes procédures - Protect'Envi",
            "desc": "Consultez et suivez l'avancement de vos procédures de constatation.",
        },
    ),
    (
        r"^/contact$",
        {
            "title": "Contact - Protect'Envi",
            "desc": "Contactez l'équipe de Protect'Envi.",
        },
    ),
    (
        r"^/demarche-numerique-rejoindre-protectenvi$",
        {
            "title": "Rejoindre le dispositif - Protect'Envi",
            "desc": "Rejoignez le dispositif Protect'Envi pour lutter contre les dépôts sauvages.",
        },
    ),
    (
        r"^/rdv$",
        {
            "title": "Prendre rendez-vous - Protect'Envi",
            "desc": "Prenez rendez-vous avec un conseiller Protect'Envi.",
        },
    ),
    (
        r"^/login-demo$",
        {
            "title": "Connexion démo - Protect'Envi",
            "desc": "Connectez-vous à l'espace de démonstration de Protect'Envi.",
        },
    ),
    (
        r"^/demarrer-constatation$",
        {
            "title": "Démarrer une constatation - Protect'Envi",
            "desc": "Démarrer une nouvelle constatation de dépôt sauvage.",
        },
    ),
    (
        r"^/constatation$",
        {
            "title": "Créer une constatation - Protect'Envi",
            "desc": "Remplir le formulaire de constatation de dépôt sauvage.",
        },
    ),
    (
        r"^/faq$",
        {
            "title": "Foire Aux Questions - Protect'Envi",
            "desc": "Retrouvez toutes les réponses aux questions les plus fréquentes sur la lutte contre les dépôts sauvages.",
        },
    ),
    # Pages dynamiques avec identifiants
    (
        r"^/suivi-procedure/[^/]+$",
        {
            "title": "Suivi de procédure - Protect'Envi",
            "desc": "Suivez l'avancement de cette procédure de constatation.",
        },
    ),
    (
        r"^/constatation-fin/[^/]+$",
        {
            "title": "Constatation enregistrée - Protect'Envi",
            "desc": "Votre constatation de dépôt sauvage a été enregistrée avec succès.",
        },
    ),
    (
        r"^/constatation/[^/]+$",
        {
            "title": "Modifier la constatation - Protect'Envi",
            "desc": "Modifier les détails de la constatation de dépôt sauvage.",
        },
    ),
]


def get_seo_data(path):
    normalized_path = "/" + path.strip("/")
    if normalized_path == "//":
        normalized_path = "/"

    # Handle dynamic FAQ items (/faq/slug)
    faq_match = re.match(r"^/faq/(?P<slug>[\w-]+)$", normalized_path)
    if faq_match:
        slug = faq_match.group("slug")
        try:
            from backend.faq.models import FAQItem

            faq_item = FAQItem.objects.filter(slug=slug).first()
            if faq_item:
                desc = "Protect'Envi - Foire Aux Questions"
                for block in faq_item.content:
                    if block.get("type") == "rich_text" and block.get("value"):
                        from django.utils.html import strip_tags

                        plain_text = strip_tags(block["value"])
                        plain_text = plain_text.replace("&nbsp;", " ").strip()
                        if len(plain_text) > 150:
                            desc = plain_text[:147] + "..."
                        else:
                            desc = plain_text
                        break
                return {
                    "title": f"{faq_item.title} - Protect'Envi",
                    "desc": desc,
                }
        except Exception:
            pass

    for pattern, seo_data in SEO_PATTERNS:
        if re.match(pattern, normalized_path):
            return seo_data
    return None
