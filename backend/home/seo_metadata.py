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
    for pattern, seo_data in SEO_PATTERNS:
        if re.match(pattern, normalized_path):
            return seo_data
    return None
