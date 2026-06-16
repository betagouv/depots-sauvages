<template>
  <DsfrModal :opened="opened" :title="title" :is-alert="true" @close="$emit('close')">
    <form @submit.prevent="submitForm" class="fr-container--fluid fr-p-0 faq-edit-form">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <div class="fr-input-group">
            <label class="fr-label" for="faq-question">Question</label>
            <input
              v-model="localForm.title"
              class="fr-input"
              type="text"
              id="faq-question"
              required
              placeholder="Ex: Qu'est-ce qu'un dépôt sauvage ?"
            />
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-select-group">
            <label class="fr-label" for="faq-category">Thématique / Catégorie</label>
            <select v-model="localForm.categoryId" class="fr-select" id="faq-category">
              <option :value="null">Aucune thématique (placer en bas)</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-input-group">
            <label class="fr-label" for="faq-answer">Réponse</label>
            <div class="tiptap-editor-wrapper">
              <RichTextEditor v-model="localForm.answer" />
            </div>
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-checkbox-group">
            <input v-model="localForm.is_published" type="checkbox" id="faq-published" />
            <label class="fr-label" for="faq-published">Publié (visible de tous)</label>
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
import RichTextEditor from '../shared/RichTextEditor.vue'

interface FAQCategory {
  id: number
  label: string
}

interface QuestionForm {
  title: string
  answer: string
  categoryId: number | null
  is_published: boolean
}

const props = defineProps<{
  opened: boolean
  title: string
  categories: FAQCategory[]
  initialData: QuestionForm
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', data: QuestionForm): void
}>()

const localForm = ref<QuestionForm>({ ...props.initialData })

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
