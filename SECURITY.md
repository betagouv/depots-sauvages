# Politique et auto-évaluation de sécurité - security

Ce document détaille la politique de sécurité de l'application Protect'Envi - Dépôts Sauvages en production, ainsi que notre auto-évaluation technique démontrant la robustesse de la plateforme.

---

## 1. Signaler une vulnérabilité - vulnerability reporting

Si vous découvrez une faille de sécurité dans cette application, merci de ne pas utiliser l'outil de ticket public - GitHub Issues. Signalez-la de manière responsable afin que nous puissions la corriger rapidement :

* Contact principal : Envoyez un e-mail détaillé à contact@protect-envi.beta.gouv.fr
* Canal officiel - DINUM : Si vous souhaitez utiliser le protocole de divulgation de vulnérabilités officiel de l'État, ou en l'absence de réponse, déposez un signalement sur la plateforme de la DINUM : [vdp.numerique.gouv.fr](https://vdp.numerique.gouv.fr/)

---

## 2. Auto-évaluation et robustesse de l'application

Nous appliquons les principes de sécurité par défaut - security by design - et de défense en profondeur - defense in depth - pour garantir l'intégrité des données des collectivités et des citoyens.

### A. Protection contre le cross-site scripting

La plateforme met en œuvre plusieurs couches de défense contre l'injection de scripts malveillants :
1. Échappement automatique systématique via le rendu frontend - Vue.js - et backend - templates Django.
2. Utilisation proscrite ou sécurisée de la directive v-html, limitée à du contenu statique ou contrôlé.
3. Génération de documents ODT sécurisée via python-odt-template avec échappement XML et téléchargement forcé en pièce jointe afin de neutraliser l'exécution de script.

> [!TIP]
> Un audit technique approfondi de l'absence de failles XSS sur l'ensemble du cycle de vie du formulaire de constatation est disponible dans le document dédié :
> 📖 **[Audit de sécurité xss - formulaire de constatation](./docs/audit-xss-constatation.md)**

---

### B. Politique de sécurité du contenu et permissions policy

* Politique de sécurité du contenu : Activée en production via django-csp pour limiter les scripts autorisés (pas d'inline script ni d'eval) et restreindre les origines de confiance comme Matomo, Crisp, Tally.
* Permissions policy : Restreint l'accès aux fonctionnalités matérielles du navigateur comme la caméra, le microphone, l'accès USB ou la géolocalisation pour limiter la surface d'attaque en cas de compromission et protéger la vie privée des collectivités.

> [!TIP]
> Pour consulter la configuration détaillée de nos en-têtes HTTP de sécurité et nos recommandations d'analyse externe, consultez le document dédié :
> 📖 **[Politique de sécurité du contenu et permissions policy](./docs/politique-csp-permissions.md)**

---

### C. Contrôle d'accès et prévention contre l'idor

Les vulnérabilités de type Insecure Direct Object Reference sont prévenues par une séparation stricte des données côté serveur :
* Toutes les requêtes API manipulant des constatations filtrent systématiquement les requêtes par rapport à l'utilisateur connecté : Constatation.objects.filter(user=self.request.user).
* Il est techniquement impossible pour un utilisateur authentifié de lire, modifier ou télécharger des documents liés à une constatation créée par un autre utilisateur.

---

### D. Limiteur de débit - rate limiting

Afin de prévenir les abus, le spam et les tentatives de brute force sur les formulaires ou l'envoi d'e-mails :
* Les endpoints API critiques, tels que la création ou mise à jour de constatations, sont soumis à un régulateur de débit limitant le nombre de requêtes autorisées par adresse IP et par utilisateur (par défaut 10/heure en production).

---

### E. Sécurisation des cookies et sessions

Les cookies de session et de sécurité sont configurés selon les meilleures pratiques du web :
* Le cookie CSRF et le cookie de session sont sécurisés, interdisant leur transmission sur des connexions non chiffrées (HTTP).
* L'attribut SameSite=Lax est appliqué pour limiter les risques d'attaques par falsification de requête intersites.

---

### F. Protection contre l'indexation des environnements hors production

Pour éviter que des moteurs de recherche n'indexent des environnements de staging ou de test et n'exposent des données factices :
* Un middleware Django dédié intercepte les requêtes sur ces environnements pour injecter l'en-tête HTTP X-Robots-Tag: noindex, nofollow.
* Le fichier robots.txt servi dynamiquement bloque également le parcours des robots d'indexation en dehors de l'environnement de production.
