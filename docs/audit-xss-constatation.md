# Audit de sécurité xss - formulaire de constatation

Cet audit documente l'analyse de sécurité menée suite à l'introduction du formulaire de constatation de dépôt sauvage dans l'application. L'objectif est de vérifier l'absence de risques d'injection de scripts malveillants - cross-site scripting ou xss - réverbérés, stockés, ou basés sur le DOM.

---

## 1. Description du formulaire de constatation

Le formulaire de constatation est un parcours en plusieurs étapes structuré autour de :
- **Un composant d'entrée principal** qui initialise le contexte de l'utilisateur.
- **Un composant conteneur racine** qui gère la soumission globale.
- **Plusieurs sous-sections fonctionnelles** composant le parcours utilisateur :
  - La localisation du dépôt.
  - Les détails techniques de la constatation comme la date, l'heure, le rôle de l'agent.
  - La description physique du dépôt comme le volume, le type de déchets.
  - L'identification de l'auteur présumé.
  - L'estimation financière du préjudice.
  - La finalisation de la démarche comme les consentements, les coordonnées facultatives.

---

## 2. Analyse des vecteurs d'attaque xss

### A. Rendu client-side

Le frontend utilise Vue.js 3 en mode Single Page Application ou SPA. Vue.js offre intrinsèquement une protection contre le XSS en convertissant les chaînes de caractères insérées via l'interpolation standard `{{ expression }}` en nœuds de texte DOM non interprétés.

#### 1. Audit de la directive v-html
La directive v-html permet d'insérer du HTML brut et constitue le vecteur de risque XSS le plus courant. Une recherche globale sur l'intégralité du frontend a identifié uniquement deux occurrences de cette directive :

- **Dans le composant d'affichage des listes d'actions de suivi :**
  ```html
  <span class="action-label" v-html="action.label"></span>
  ```
  _Analyse :_ Ce composant affiche les listes de tâches à cocher pour le suivi de la procédure, par exemple pour la signature de pièces de procédure, ou la notification de l'auteur présumé. Toutes les listes d'actions sont construites dynamiquement à partir d'objets calculés contenant des chaînes de caractères statiques codées en dur, comme `"<strong>Faire signer la lettre d'information</strong> par l'autorité titulaire..."`. Aucune saisie utilisateur n'est concaténée ou interpolée dans ces labels.

- **Dans le composant d'affichage des bannières de mise en valeur :**
  ```html
  <span v-html="description"></span>
  ```
  _Analyse :_ Utilisé sur la page d'introduction de la procédure avec comme argument une chaîne interpolée contenant le nombre de dossiers en cours de l'utilisateur, retourné sous forme d'entier par l'API de profil. Le contenu n'est pas manipulable par l'utilisateur.

#### 2. Sécurisation des liaisons d'attributs
L'injection d'une URL de type `javascript:` dans un lien hypertexte dynamique `href` est une forme classique de XSS.
- Les liens de téléchargement de documents sont construits de manière sécurisée via des fonctions utilitaires dans le module de gestion des URLs de l'application. Le paramètre injecté est l'identifiant interne du dossier, casté sous forme d'entier lors de la navigation, excluant tout risque d'injection de protocole `javascript:`.
- La redirection ProConnect est passée en paramètre d'URL lors de la phase de connexion. Le paramètre est correctement encodé à l'aide d'une fonction d'encodage d'URI pour prévenir l'injection de paramètres HTTP ou d'URL arbitraires. De plus, le backend valide l'URL de redirection finale par rapport aux domaines autorisés en configuration de production.

#### 3. Composants d'autocomplétion
- Les composants d'autocomplétion de recherche d'adresses et d'entreprises effectuent des appels asynchrones vers des APIs externes de l'État de confiance.
- Les entrées utilisateur saisies au clavier sont sécurisées à l'envoi à l'aide d'un échappement d'URI strict.
- Le rendu de la liste des suggestions retournées par l'API externe s'effectue par interpolation classique, empêchant l'exécution de code malveillant si la réponse d'un tiers était compromise.

---

### B. Persistance et stored xss

Le stored xss se produit lorsque l'entrée utilisateur malveillante est sauvegardée en base de données et ré-affichée plus tard sans échappement adéquat.

#### 1. Transmission API JSON
- Toutes les données de constatation sont soumises via une requête POST/PUT au format JSON à destination du contrôleur de l'API de gestion des constatations.
- L'accès aux points de terminaison est restreint aux seuls utilisateurs authentifiés possédant les droits d'écriture sur l'objet en question.
- L'API sérialise les données entrantes et sortantes sous forme de JSON strict, qui n'est pas interprété en HTML par le navigateur lors de son transfert.

#### 2. Interface d'administration
- L'interface d'administration de la plateforme permet aux administrateurs de consulter l'ensemble des constatations.
- L'auto-échappement HTML est activé par défaut dans les templates d'administration du framework de backend.
- Aucun champ de données utilisateur de la constatation, comme la localisation ou les précisions textuelles, ne fait l'objet d'une désactivation de l'auto-échappement dans les vues de l'administration.

#### 3. Modèles de courriels
- Le template HTML utilisé pour envoyer les documents au demandeur affiche dynamiquement la commune et l'identifiant du signalement. Ces variables sont automatiquement échappées par le moteur de rendu de gabarits du serveur, évitant tout risque d'exécution XSS dans le client de messagerie du destinataire.

---

### C. Génération de documents

Lors de la validation du formulaire, l'application génère des fichiers au format ODT - OpenDocument Text - comme le rapport de constatation et la lettre d'information.

1. **Génération XML sécurisée** :
   Le traitement du document fusionne les données saisies par l'utilisateur avec un template de document. Ce traitement est réalisé par une bibliothèque dédiée qui applique un échappement automatique des balises XML, comme `<`, `>`, et `&`. Cela garantit que :
   - L'utilisateur ne peut pas briser la structure du fichier XML interne du document, notamment le contenu textuel.
   - Aucun script ou entité externe malveillante, de type XML External Entity, ne peut être injecté dans l'archive du document.

2. **Mode de livraison sécurisé par pièce jointe** :
   Les documents sont téléchargés depuis un contrôleur de téléchargement sécurisé. Le serveur retourne les fichiers avec l'en-tête de téléchargement forcé Content-Disposition: attachment et le type MIME correspondant à l'OpenDocument Text. Le navigateur force ainsi le téléchargement local des fichiers, ce qui supprime tout risque de XSS contextuel au domaine du site.

---

## 3. Synthèse des protections et risque résiduel

| Phase du traitement                  | Risque ciblé                              | Protection mise en place                                                                                                                                | Statut      |
| :----------------------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------- |
| **Saisie & Validation**              | Injection de script à la soumission       | Validation d'API, typage fort des données (JSON) et encodage URI côté client.                                                                           | ✅ Maîtrisé |
| **Rendu Interface**                  | Reflected & Stored XSS                    | Rendu sécurisé par défaut dans le framework frontend. Aucun usage de rendu HTML brut ou de constructeur d'URL dynamique avec des variables utilisateur. | ✅ Maîtrisé |
| **Espace Admin**                     | Exploitation du backoffice par Stored XSS | Auto-échappement des gabarits d'administration par défaut.                                                                                              | ✅ Maîtrisé |
| **Courriels d'accompagnement**       | XSS dans le client de messagerie          | Auto-échappement des variables dans les courriels.                                                                                                      | ✅ Maîtrisé |
| **Téléchargement de pièces jointes** | Exécution de code via document            | En-tête HTTP forçant le téléchargement local des fichiers générés.                                                                                      | ✅ Maîtrisé |

## Conclusion

L'analyse de la gestion des flux de données et du rendu de l'application démontre le respect rigoureux des exigences de développement sécurisé. Grâce à l'échappement par défaut des frameworks modernes utilisés, tant côté client que côté serveur, et au traitement restrictif des livrables dynamiques, la plateforme présente une excellente robustesse face aux risques d'injections de scripts.
