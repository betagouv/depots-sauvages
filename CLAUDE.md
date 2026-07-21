# SEO : titre et description de page

Ce projet gère le titre et la description de chaque page à **deux endroits séparés, non synchronisés automatiquement** :

1. **Titre affiché dans l'onglet du navigateur** (côté frontend, dynamique) : propriété `meta.title` de chaque route dans [`frontend/main.js`](frontend/main.js), appliqué via `router.afterEach` dans [`frontend/services/matomo.js`](frontend/services/matomo.js).
2. **Titre et description utilisés pour le référencement et les aperçus de partage** (réseaux sociaux, WhatsApp, Google) : liste `SEO_PATTERNS` dans [`backend/seo/seo_metadata.py`](backend/seo/seo_metadata.py), injectée côté serveur dans le HTML avant envoi au navigateur (les robots de partage ne exécutent pas le JS, donc seul ce second mécanisme compte pour eux).

**À chaque nouvelle page créée ou modification significative du contenu d'une page existante**, penser à mettre à jour les deux :
- ajouter/mettre à jour l'entrée correspondante dans `SEO_PATTERNS` (`backend/seo/seo_metadata.py`) avec un titre et une description qui reflètent le contenu réel de la page ;
- ajouter/mettre à jour `meta.title` de la route associée dans `frontend/main.js`.

Une page sans entrée dans `SEO_PATTERNS` retombe silencieusement sur le titre/description générique de la page d'accueil — ce qui a déjà causé un bug (page `/comment-agir` sans métadonnée dédiée, corrigé le 2026-07-21, voir [Doc Dev](../Doc%20Dev/depots-sauvages-notedev/2026-07-21-titres-descriptions-seo-comment-agir-rdv.md)).
