# Architecture de Sécurité

Ce document décrit les principes de sécurité mis en œuvre dans l'application.

---

## 1. Principe de Défense en Profondeur (Front-end vs Back-end)

L'application sépare strictement la logique d'affichage (front-end) de la logique d'autorisation (back-end).

### Contrôles côté Client (Front-end)

Le front-end (Vue.js / Pinia / Vue Router) implémente des contrôles pour améliorer l'expérience utilisateur et restreindre la navigation :

- **Bascule "Mode Admin"** : Permet aux utilisateurs disposant des privilèges nécessaires de basculer l'affichage. Ce choix est conservé dans le `sessionStorage` (`protect_envi_admin_mode`).
- **Gardes de navigation (Router Guards)** : Empêchent l'accès aux pages de back-office aux utilisateurs non connectés ou ne disposant pas du flag `is_staff`.

### Contrôles côté Serveur (Back-end)

Le back-end (Django / Django REST Framework) est le seul garant de la sécurité et des autorisations. Chaque requête d'API subit les validations suivantes :

1. **Authentification** : Vérification de la validité de la session ou du token de l'utilisateur.
2. **Autorisation (Permissions)** :
   - Les endpoints sensibles sont protégés par la classe de permission qui valide la valeur de `user.is_staff` en base de données.
   - Tout accès ou modification d'une procédure standard vérifie que l'utilisateur connecté est soit le créateur du signalement, soit un membre du personnel autorisé (`is_staff`).

---

## 2. Cloisonnement des Données et Sérialisation Dynamique

Afin d'éviter toute élévation de privilèges ou fuite de données lors de la mise à jour d'un modèle :

- **Sérialiseurs conditionnels** : L'API adapte le sérialiseur Django REST Framework selon le niveau de droit de l'appelant.
  - _Exemple_ : Pour le suivi des procédures, un utilisateur standard reçoit le sérialiseur de base, tandis qu'un membre du personnel authentifié reçoit une version étendue permettant de manipuler des champs sensibles (ex: notes internes, agent assigné).
- **Validation stricte** : Les champs non inclus dans la configuration du sérialiseur d'un utilisateur standard sont ignorés lors des requêtes d'écriture (`POST`, `PUT`, `PATCH`).

---

## 3. Authentification et Intégration

### Fournisseur d'identité officiel (ProConnect)

- L'intégration s'appuie sur la bibliothèque standard `mozilla-django-oidc`.
- Le backend d'authentification `ProConnectOIDCBackend` ne donne **jamais** de privilèges d'administration (`is_staff` ou `is_superuser`) automatiquement lors de la création ou de la mise à jour de l'utilisateur. L'élévation d'un utilisateur en administrateur doit être réalisée manuellement par un administrateur système via la console d'administration Django.
- **Protection des données personnelles (PII)** : Lors des étapes de création ou mise à jour utilisateur, le backend filtre les logs pour ne consigner que l'identifiant technique opaque `sub` (niveau `INFO`), garantissant qu'aucune claim d'identité nominative (nom, prénom, e-mail) ne fuite dans les journaux d'application.

### Mode Démo / Environnement de test (Bypass Auth)

- Un mécanisme de bypass d'authentification (`BypassAuthBackend`) est disponible pour faciliter les tests locaux.
- **Mesures de protection** :
  1. Il est formellement bloqué si la variable `ENV_NAME` contient la chaîne `"prod"`.
  2. Il interdit la connexion aux comptes d'administration (`is_staff=True` ou `is_superuser=True`), limitant tout risque d'accès non autorisé si le bypass venait à être activé par erreur.
  3. **Blocage systématique des endpoints** : Si le paramètre `BYPASS_AUTH_ENABLED` est désactivé (ce qui est le cas par défaut et forcé en production), toutes les requêtes vers les endpoints de bypass d'authentification (`/api/bypass-auth/config/` et `/api/bypass-auth/login/`) sont interceptées au niveau de la classe de base commune et lèvent immédiatement une exception `404 Not Found`. Cela élimine tout risque d'accès réseau ou d'énumération de comptes.

---

## 4. Tests de Non-Régression de Sécurité

Chaque fonctionnalité de sécurité sensible doit faire l'objet de tests automatisés.

- Les droits d'accès aux routes de backoffice doivent être testés avec des utilisateurs non authentifiés, des utilisateurs standards et des administrateurs.
- Tout nouveau champ sensible ajouté à un modèle et réservé aux administrateurs doit être couvert par un test de validation de sérialiseur.
- **Cloisonnement des accès (IDOR)** : Le non-accès aux suivis de procédure par des utilisateurs tiers (non propriétaires) est validé par des tests unitaires dédiés (`backend/procedures/tests.py`), garantissant le respect de la politique d'isolation objet.

---

## 5. Traitement Sécurisé des Fichiers et Photos (Upload & Doc Maker)

L'application permet d'ajouter des photos lors d'une constatation pour enrichir le rapport généré. Plusieurs mécanismes de sécurité sont mis en œuvre pour prévenir les failles liées au téléversement de fichiers (telles que le téléchargement de scripts malveillants ou le déni de service) :

### Contrôles côté Client (Front-end)

- **Restriction des types MIME** : L'élément `<input type="file">` est configuré pour n'accepter que les images (`accept="image/*"`).
- **Limite de taille dynamique** : Une vérification stricte est appliquée sur `file.size` (max 20 Mo par photo) avant tout chargement ou conversion en mémoire afin d'éviter le blocage/OOM du navigateur.
- **Redimensionnement et re-encodage dynamique** : Avant d'être intégrées au payload, les images sont lues et redimensionnées via l'API Canvas HTML5 (`canvas.toDataURL('image/jpeg')`). Cela neutralise l'exécution potentielle de scripts exécutables cachés dans les métadonnées ou le conteneur du fichier original.

### Contrôles côté Serveur (Back-end)

- **Contrôle de taille binaire (Anti-DoS)** : Rejet strict des images décodées dépassant 20 Mo (`MAX_IMAGE_BYTES`).
- **Validation du format par Magic Bytes (`filetype`)** : Le serveur ne se fie pas à l'extension fournie ou au type MIME déclaré dans l'en-tête de la requête. Chaque image transmise est analysée au niveau binaire à l'aide de la bibliothèque `filetype` et filtrée via une liste blanche stricte de types MIME (`image/jpeg`, `image/png`, `image/webp`).
- **Validation stricte de l'extension** : Vérification que l'extension détectée fait partie d'une liste autorisée (`.jpg`, `.jpeg`, `.png`, `.webp`). Rejet immédiat en cas de non-conformité.
- **Protection contre les bombes de décompression (_Decompression Bomb_)** : Définition d'un seuil maximal de résolution (`Image.MAX_IMAGE_PIXELS = 25_000_000`) via la bibliothèque `Pillow` pour prévenir les attaques par déni de service mémoire.
- **Vérification de structure et assainissement (Pillow)** : Analyse d'intégrité binaire de l'image (`img.verify()`) puis ré-encodage complet du flux d'image pour supprimer tout EXIF malveillant ou script injecté (stéganographie).
- **Isolation des fichiers temporaires et nettoyage** : Les images traitées sont stockées temporairement via `tempfile.NamedTemporaryFile` et supprimées du disque (`os.unlink`) dès la génération du rapport terminée.
