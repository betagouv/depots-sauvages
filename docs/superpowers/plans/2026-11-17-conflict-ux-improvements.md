# Plan d'Implémentation : Optimisation UX Conflits & Neutralisation des Faux Autosaves

> **Objectif** : Rendre la gestion des conflits (HTTP 409) non-intrusive pendant la saisie en tâche de fond (autosave), supprimer les faux autosaves au rechargement ou sans modifications réelles, et réserver la modale bloquante aux actions de soumission explicites.

---

### Problématique actuelle
1. **Faux autosaves déclenchés par Vue** : Dès qu'on recharge (`resolveConflictReload`), les mutations d'état déclenchent les watchers profonds (`watch(() => ... , { deep: true })`), provoquant une nouvelle sauvegarde automatique involontaire qui ré-engendre un conflit en boucle.
2. **Absence de détection de dirty** : Des `PATCH` ou `PUT` sont émis même si aucune donnée n'a réellement changé par rapport au serveur.
3. **Modale DSFR bloquante pendant la frappe** : En plein milieu d'une saisie dans un champ texte, une fenêtre modale s'ouvre, interrompt l'utilisateur et bloque l'interface.

---

### Solution proposée

#### 1. Composant `ConflictBanner.vue` (DSFR non-intrusif)
- Créer un bandeau d'alerte discret placé au-dessus du formulaire (sur la procédure et sur la constatation) :
  - `fr-alert fr-alert--warning fr-mb-3w`
  - Affiche qui a modifié le dossier et quand : *« Ce dossier a été mis à jour par [Marc Dubois]. Vos saisies locales sont préservées. »*
  - Deux boutons d'action intégrés :
    - `[Recharger la version à jour]`
    - `[Écraser avec mes saisies]`
  - Bouton de fermeture optionnel pour masquer l'alerte sans forcer ni recharger.

#### 2. Différenciation Autosave (Bandeau) vs Soumission Explicite (Modale)
- **Lors d'un conflit en autosave** :
  - On suspend l'autosave.
  - On affiche le **bandeau** `ConflictBanner.vue` (pas de popup bloquant). L'utilisateur peut continuer à lire, comparer, réfléchir ou taper.
- **Lors d'une soumission explicite (Bouton « Enregistrer », validation formulaire)** :
  - Si un conflit existe toujours, on ouvre la modale `ConflictResolutionModal.vue` pour exiger un arbitrage avant enregistrement définitif.

#### 3. Neutralisation stricte des faux autosaves au rechargement
- Ajouter un flag `isReloading` ou `isSilentSync` pendant `resolveConflictReload`.
- Dès le clic sur *Recharger* :
  1. `isReloading = true`
  2. `conflictModalVisible = false`, `conflictBannerVisible = false`
  3. `cancel()` sur le debounce de sauvegarde
  4. Récupération et application des données serveur
  5. Mise à jour de `lastSyncedModified` et du snapshot de référence
  6. `await nextTick()` puis remise à zéro `isReloading = false`
- Le `watch` profond vérifie `if (isReloading) return`.

#### 4. Détection des changements effectifs (Dirty Check)
- Avant d'appeler l'API de sauvegarde en tâche de fond, vérifier si le payload a réellement des modifications par rapport aux données serveur synchronisées. Si identique : aucune requête envoyée.

---

### Découpage des tâches

- [ ] **Tâche 1 : Composant `ConflictBanner.vue` & Tests unitaires**
  - Créer `frontend/components/shared/ConflictBanner.vue` avec les styles DSFR.
  - Écrire un test unitaire dédié `frontend/tests/conflict-banner.test.ts`.

- [ ] **Tâche 2 : Gestion d'état et neutralisation des boucles dans les stores**
  - Mettre à jour `frontend/stores/suivi-procedure.ts` et `frontend/stores/constatation.ts`.
  - Ajouter `conflictBannerVisible`, `isReloading`, et snapshot pour dirty-check.
  - Tests unitaires des stores.

- [ ] **Tâche 3 : Intégration sur la page Procédure (`suivi-procedure.vue`)**
  - Remplacer l'ouverture de la modale en autosave par l'affichage du bandeau `ConflictBanner`.
  - Sécuriser le watcher avec `isReloading`.

- [ ] **Tâche 4 : Intégration sur la page Constatation (`constatation-form.vue`)**
  - Intégrer le bandeau `ConflictBanner` pour l'autosave.
  - Conserver la modale pour le `submitForm` final.

- [ ] **Tâche 5 : Validation globale et tests unitaires / lint**
  - Exécuter la suite complète de tests Vitest.
  - Vérifier la compilation frontend (`npm run build`).
