<template>
  <div class="step-waiting-placeholder fr-p-8w fr-mb-4w">
    <div class="fr-grid-row fr-grid-row--center">
      <div class="fr-col-12 fr-col-md-8 text-center">
        <button
          class="back-icon-btn fr-mb-2w"
          type="button"
          aria-label="Retourner à l'étape précédente"
          @click="$emit('action')"
        >
          <span
            class="fr-icon-arrow-left-line fr-icon--lg"
            aria-hidden="true"
            style="color: var(--text-action-high-blue-france)"
          ></span>
        </button>
        <h5 class="fr-h6 fr-mb-1w">{{ title }}</h5>
        <div class="fr-text--sm fr-mb-3w">
          <slot name="description">
            {{ description }}
          </slot>
        </div>
        <DsfrButton
          v-if="buttonLabel"
          :label="buttonLabel"
          secondary
          class="fr-btn--sm"
          @click="$emit('action')"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title?: string
    description?: string
    buttonLabel?: string
  }>(),
  {
    title: 'Décider des suites à donner à la procédure',
    description: "Veuillez d'abord choisir de sanctionner l'auteur présumé ou d'abandonner les poursuites.",
    buttonLabel: 'Décider des poursuites',
  }
)

defineEmits(['action'])
</script>

<style scoped>
.step-waiting-placeholder {
  background-color: var(--background-alt-grey);
  border: 1px dashed var(--border-default-grey);
  border-radius: 12px;
}

.text-center {
  text-align: center;
}

.back-icon-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 50%;
  transition:
    background-color 0.2s,
    transform 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.back-icon-btn:hover {
  background-color: var(--background-alt-blue-france);
  transform: translateX(-4px);
}

.back-icon-btn:active {
  transform: translateX(-2px) scale(0.95);
}
</style>
