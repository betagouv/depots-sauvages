<template>
  <DsfrModal :opened="opened" :title="title" :is-alert="true" @close="$emit('close')">
    <form @submit.prevent="submitForm" class="fr-container--fluid fr-p-0">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <div class="fr-input-group">
            <label class="fr-label" for="category-label">Titre de la thématique</label>
            <input
              v-model="localForm.label"
              class="fr-input"
              type="text"
              id="category-label"
              required
              placeholder="Ex: ⚖️ Cadre général"
            />
          </div>
        </div>

        <div class="fr-col-12 fr-mt-3w text-right">
          <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--right">
            <li>
              <button type="button" class="fr-btn fr-btn--secondary" @click="$emit('close')">
                Annuler
              </button>
            </li>
            <li>
              <button type="submit" class="fr-btn">Enregistrer</button>
            </li>
          </ul>
        </div>
      </div>
    </form>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import { ref, watch } from 'vue'

interface CategoryForm {
  label: string
}

const props = defineProps<{
  opened: boolean
  title: string
  initialData: CategoryForm
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', data: CategoryForm): void
}>()

const localForm = ref<CategoryForm>({ ...props.initialData })

watch(
  () => props.opened,
  (isOpened) => {
    if (isOpened) {
      localForm.value = { ...props.initialData }
    }
  }
)

const submitForm = () => {
  emit('save', { ...localForm.value })
}
</script>
