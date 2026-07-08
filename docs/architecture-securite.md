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

### Mode Démo / Environnement de test (Bypass Auth)

- Un mécanisme de bypass d'authentification (`BypassAuthBackend`) est disponible pour faciliter les tests locaux.
- **Mesures de protection** :
  1. Il est formellement bloqué si la variable `ENV_NAME` contient la chaîne `"prod"`.
  2. Il interdit la connexion aux comptes d'administration (`is_staff=True` ou `is_superuser=True`), limitant tout risque d'accès non autorisé si le bypass venait à être activé par erreur.

---

## 4. Tests de Non-Régression de Sécurité

Chaque fonctionnalité de sécurité sensible doit faire l'objet de tests automatisés.

- Les droits d'accès aux routes de backoffice doivent être testés avec des utilisateurs non authentifiés, des utilisateurs standards et des administrateurs.
- Tout nouveau champ sensible ajouté à un modèle et réservé aux administrateurs doit être couvert par un test de validation de sérialiseur.

