<template>
  <DsfrModal :opened="opened" :title="title" :is-alert="true" size="lg" @close="$emit('close')">
    <form @submit.prevent="submitForm" class="fr-container--fluid fr-p-0 blog-edit-form">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <div class="fr-input-group">
            <label class="fr-label" for="blog-title">Titre de l'article</label>
            <input
              v-model="localForm.title"
              class="fr-input"
              type="text"
              id="blog-title"
              required
              placeholder="Ex : Réaménagement exemplaire à Peyrins"
            />
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-input-group">
            <label class="fr-label" for="blog-summary">
              Résumé court
              <span class="fr-hint-text">Affiché dans les cartes de listing (500 caractères max).</span>
            </label>
            <textarea
              v-model="localForm.summary"
              class="fr-input"
              id="blog-summary"
              rows="3"
              maxlength="500"
              placeholder="Bref résumé de l'article..."
            ></textarea>
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-upload-group">
            <label class="fr-label" for="blog-cover-image">
              Image de couverture
              <span class="fr-hint-text">Format JPG, PNG ou WEBP.</span>
            </label>
            <input
              class="fr-upload"
              type="file"
              id="blog-cover-image"
              accept="image/*"
              @change="handleFileChange"
            />
            <div v-if="previewUrl || localForm.currentCoverImage" class="image-preview-container fr-mt-2w">
              <p class="fr-text--xs fr-mb-1w">Aperçu :</p>
              <img :src="previewUrl || localForm.currentCoverImage" alt="Aperçu" class="preview-img" />
            </div>
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-input-group" :class="{ 'fr-input-group--error': showContentError }">
            <label class="fr-label" for="blog-content">
              Contenu de l'article
              <span class="fr-hint-text">Rédigez le texte complet de votre retour d'expérience ou article.</span>
            </label>
            <div class="tiptap-editor-wrapper">
              <RichTextEditor v-model="localForm.bodyHtml" />
            </div>
            <p v-if="showContentError" class="fr-error-text">
              Le contenu de l'article est obligatoire.
            </p>
          </div>
        </div>

        <div class="fr-col-12">
          <div class="fr-checkbox-group">
            <input v-model="localForm.is_published" type="checkbox" id="blog-published" />
            <label class="fr-label" for="blog-published">Publié (visible de tous les utilisateurs)</label>
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
              <button type="submit" class="fr-btn" :disabled="isSubmitting">
                {{ isSubmitting ? 'Enregistrement...' : 'Enregistrer' }}
              </button>
            </li>
          </ul>
        </div>
      </div>
    </form>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import DOMPurify from 'dompurify'
import { ref, watch } from 'vue'
import RichTextEditor from '../shared/RichTextEditor.vue'

export interface BlogArticleFormData {
  title: string
  summary: string
  bodyHtml: string
  coverImageFile: File | null
  currentCoverImage?: string | null
  is_published: boolean
}

const props = defineProps<{
  opened: boolean
  title: string
  initialData: BlogArticleFormData
  isSubmitting?: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', data: BlogArticleFormData): void
}>()

const localForm = ref<BlogArticleFormData>({ ...props.initialData })
const previewUrl = ref<string | null>(null)
const showContentError = ref(false)

const isContentEmpty = (html: string) => {
  if (!html) return true
  const text = DOMPurify.sanitize(html, { ALLOWED_TAGS: [] }).trim()
  return text.length === 0
}

watch(
  () => props.opened,
  (isOpened) => {
    if (isOpened) {
      localForm.value = { ...props.initialData, coverImageFile: null }
      previewUrl.value = null
      showContentError.value = false
    }
  }
)

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    localForm.value.coverImageFile = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const submitForm = () => {
  if (isContentEmpty(localForm.value.bodyHtml)) {
    showContentError.value = true
    return
  }
  showContentError.value = false
  emit('save', { ...localForm.value })
}
</script>

<style scoped>
.blog-edit-form {
  padding-right: 0.25rem;
}

.image-preview-container {
  max-width: 250px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid var(--border-default-grey);
}

.preview-img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  display: block;
}

.text-right {
  text-align: right;
}
</style>
