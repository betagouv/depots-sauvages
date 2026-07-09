# Vue Guillotine

`vue-guillotine` est une bibliothèque de composants et de composables Vue 3 conçue pour faciliter l'édition et le rendu de contenus "block-based".

Elle est pensée comme le pendant frontend headless UI des structures de données générées par le backend **django-guillotine**.

---

## Philosophie et choix d'architecture

L'architecture de `vue-guillotine` repose sur le principe de briques de construction autonomes :

- **Éditeur modulaire** : Plutôt que de fournir un composant d'édition monolithique rigide, la bibliothèque fournit des outils et des composants unitaires - `Toolbar`, `ToolbarButton`, `EditorContent`, `LinkInput` et `useEditor`.
- **Assemblage par le projet client** : L'application cliente assemble ces pièces dans ses propres composants, par exemple en créant un fichier `RichTextEditor.vue`.
- **Personnalisation** : Cela permet à chaque application d'adapter l'éditeur à sa charte graphique, et de sélectionner précisément les boutons et fonctionnalités de mise en forme requis pour ses types de contenus.

---

## Librairies utilisées et intégration DSFR

- **Tiptap v3** : Moteur d'édition de texte riche, framework wrapper autour de ProseMirror, hautement extensible et personnalisable.
- **Système de design de l'État français - DSFR** :
  - Les styles de `vue-guillotine` utilisent nativement les variables CSS sémantiques du DSFR, par exemple `var(--border-default-grey)`, `var(--border-active-blue-france)`, `var(--background-alt-grey)`.
  - Les éléments générés respectent la nomenclature DSFR, par exemple l'extension Link génère des balises avec la classe `fr-link`.

---

## Composants disponibles

### 1. Édition - Tiptap wrappers

- **`EditorContent`** : Encapsule la zone d'édition Tiptap via `TiptapEditorContent`. Il gère le focus global via `:focus-within`, la bordure extérieure aux normes du DSFR, ainsi qu'une zone de défilement interne et un slot `#toolbar`.
- **`Toolbar`** : Conteneur horizontal flexible et enveloppant pour regrouper les boutons de contrôle de l'éditeur.
- **`ToolbarButton`** : Bouton individuel de barre d'outils avec gestion des états actif et inactive.
- **`SimpleToolbarButtons`** : Raccourci regroupant les fonctionnalités basiques d'édition comme le gras, l'italique et le lien.
- **`LinkInput`** : Popover de saisie et de validation d'URL pour l'insertion de liens hypertexte.

### 2. Rendu de blocs

- **`BlockRenderer`** : Composant de rendu dynamique d'une liste de blocs compatible avec le format JSON de type guillotine ou blocks.
  - Gère par défaut les types `rich_text` et `heading` sous forme de titre `h2` avec la classe `fr-h4`.
  - Propose un système de slots dynamiques nommés d'après le type du bloc pour permettre au projet client d'étendre facilement le rendu, par exemple `<template #mon_bloc_perso="{ block }">`.

---

## Composables

### `useEditor(props, emit)`

Initialise une instance de Tiptap configurée pour l'écosystème :

- Configure `StarterKit` avec des classes CSS spécifiques pour les listes ordonnées/puces (`tiptap-ol`, `tiptap-ul`).
- Configure l'extension `Link` (ouverture au clic désactivée, classe `fr-link`).
- Synchronise la valeur bidirectionnelle (`modelValue`) avec gestion du cycle de mise à jour pour éviter les curseurs qui sautent.

### `useBlockList(initialBlocks)`

Permet de manipuler localement une liste ordonnée de blocs réutilisables (ajout, suppression, déplacement vers le haut ou le bas).

---

## Exemple d'utilisation dans un projet client

Voici comment assembler un éditeur sur-mesure dans votre application :

```vue
<template>
  <EditorContent v-if="editor" :editor="editor">
    <template #toolbar>
      <Toolbar>
        <SimpleToolbarButtons :editor="editor" v-model="showLinkInput" />
      </Toolbar>
      <LinkInput v-if="showLinkInput" :editor="editor" @close="showLinkInput = false" />
    </template>
  </EditorContent>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { EditorContent, Toolbar, SimpleToolbarButtons, LinkInput, useEditor } from 'vue-guillotine'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits(['update:modelValue'])

const editor = useEditor(props, emit)
const showLinkInput = ref(false)
</script>
```
