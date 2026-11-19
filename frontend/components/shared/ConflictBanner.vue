<template>
  <div
    v-if="visible"
    class="fr-alert fr-alert--warning fr-mb-3w conflict-banner"
    role="alert"
  >
    <h3 class="fr-alert__title">Ce dossier a été modifié par un autre utilisateur</h3>
    <p class="fr-text--sm fr-mb-2w">
      <strong>{{ updatedBy }}</strong> a enregistré des modifications entre-temps. Vos saisies locales sont préservées à l'écran et la sauvegarde automatique est suspendue.
    </p>

    <div class="fr-btns-group fr-btns-group--inline-sm fr-btns-group--sm fr-mt-2w">
      <button
        type="button"
        class="fr-btn fr-btn--sm"
        @click="emit('reload')"
      >
        Recharger la version à jour
      </button>
      <button
        type="button"
        class="fr-btn fr-btn--sm fr-btn--secondary"
        @click="emit('force-save')"
      >
        Conserver mes saisies et écraser
      </button>
      <button
        v-if="dismissible"
        type="button"
        class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline"
        @click="emit('close')"
      >
        Ignorer
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    visible: boolean
    updatedBy?: string
    dismissible?: boolean
  }>(),
  {
    updatedBy: 'Un autre utilisateur',
    dismissible: true,
  }
)

const emit = defineEmits<{
  (e: 'reload'): void
  (e: 'force-save'): void
  (e: 'close'): void
}>()
</script>

<style scoped>
.conflict-banner {
  border-left: 4px solid var(--border-action-high-warning, #fc5d00);
}
</style>
