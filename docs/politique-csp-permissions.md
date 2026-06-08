# Politique de sécurité du contenu et permissions policy

Ce document détaille la configuration des en-têtes HTTP de sécurité de l'application Protect'Envi - Dépôts Sauvages - en production, notamment la politique de sécurité du contenu et la politique de permissions.

---

## 1. Politique de sécurité du contenu

La politique de sécurité du contenu est un mécanisme de sécurité essentiel conçu pour atténuer et détecter certains types d'attaques, y compris les injections de scripts et les attaques de détournement de données. Elle définit quelles sources de contenu comme les scripts, les styles, les images, les polices, les cadres ou les connexions, le navigateur de l'utilisateur est autorisé à charger et exécuter.

### A. Configuration de production

L'en-tête de sécurité du contenu est configuré directement dans les paramètres de production de l'application via le middleware gérant la politique de sécurité du contenu. Cette configuration limite le chargement des scripts, styles et connexions externes aux seules origines explicitement autorisées, comme les outils de statistiques d'État, les formulaires de retour utilisateur ou les widgets d'assistance.

### B. Analyse de robustesse face aux risques de sécurité

1. **Absence de 'unsafe-inline' dans la directive des scripts** :
   C'est la règle d'or pour neutraliser la majorité des failles d'injection de script. Le navigateur n'exécutera aucun script directement intégré dans le code HTML, comme `<script>alert(1)</script>`, ni aucun gestionnaire d'événement inline, comme `<img src=x onerror=alert(1)>`. Les scripts doivent impérativement être chargés sous forme de fichiers externes provenant de sources approuvées.

2. **Absence de 'unsafe-eval' dans la directive des scripts** :
   Empêche l'exécution de code à partir de chaînes de caractères, par exemple avec `eval`, `new Function`, ou `setTimeout` avec une chaîne. Cela bloque les tentatives d'exécution d'injections de scripts complexes utilisant la manipulation dynamique de chaînes.

3. **Restriction de la sécurité de transport et HTTPS** :
   En production, toutes les communications sont chiffrées. L'application bloque le chargement d'éléments en HTTP non sécurisé via la politique de sécurité du contenu implicite.

4. **Restriction des cadres et en-tête d'intégration dans les cadres** :
   * La directive gérant le chargement des cadres limite l'intégration d'iframes aux seules origines autorisées, comme l'application elle-même, le simulateur externe d'éligibilité et l'outil de suivi interne. Cela protège l'utilisateur contre l'intégration de cadres malveillants.
   * L'en-tête de réponse HTTP gérant les options de cadres est configuré au niveau du middleware pour interdire le détournement de clic sur le site.

---

## 2. Politique de permissions

L'en-tête de politique de permissions permet au site de contrôler quelles fonctionnalités du navigateur peuvent être utilisées dans le document actif et par les cadres intégrés.

### A. Configuration

L'en-tête est défini de manière restrictive dans les paramètres de configuration de base de l'application via le middleware dédié. Toutes les API matérielles non utilisées par l'application sont déclarées désactivées à l'aide d'une liste vide.

### B. Objectifs de sécurité et vie privée

* **Réduction de la surface d'attaque** : En déclarant désactivées les fonctionnalités matérielles comme l'accès USB, la caméra ou le microphone, l'application s'assure que même si un attaquant réussit à exécuter du code malveillant sur le navigateur, il ne pourra pas utiliser le matériel de l'utilisateur pour l'espionner ou interagir avec ses périphériques locaux.
* **Protection de la vie privée des collectivités** : L'accès à la géolocalisation de l'appareil est bloqué au niveau du navigateur, car l'application s'appuie uniquement sur des saisies d'adresses textuelles et des coordonnées administratives déclaratives.
* **Sécurisation des paiements** : L'interdiction des API de demande de paiement empêche toute tentative de détournement de flux financier ou d'escroquerie au paiement dans le contexte du site.

---

## 3. Recommandations pour l'évaluation externe

Afin de valider la conformité de ces en-têtes auprès de vos partenaires institutionnels, nous recommandons de tester l'URL de production à l'aide des outils de référence suivants :

1. **Mozilla Observatory** - [Rapport protect-envi.beta.gouv.fr](https://observatory.mozilla.org/analyze/protect-envi.beta.gouv.fr) :
   * Analyse et note la configuration des en-têtes HTTP de sécurité comme le chiffrement, les types de contenus et les en-têtes de sécurité.
   * La configuration en place permet de viser la note maximale A ou A+.
2. **CSP Evaluator de Google** - [Analyse de protect-envi.beta.gouv.fr](https://csp-evaluator.withgoogle.com/?csp=https://protect-envi.beta.gouv.fr/) :
   * Valide la robustesse de la politique de sécurité du contenu vis-à-vis des contournements connus, par exemple par l'intermédiaire de l'usage de certains scripts de bibliothèques tierces autorisées.
3. **Security Headers** - [Rapport protect-envi.beta.gouv.fr](https://securityheaders.com/?q=https%3A%2F%2Fprotect-envi.beta.gouv.fr%2F&followRedirects=on) :
   * Analyse rapide de la présence et de la configuration des principaux en-têtes HTTP de sécurité.
