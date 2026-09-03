<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-2w">Blog & Retours d'expérience</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Découvrez les initiatives, témoignages et retours d'expérience des collectivités dans la
          lutte contre les dépôts sauvages.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div v-if="isLoading" class="text-center fr-py-6w">
        <p class="fr-text--lead">Chargement des articles...</p>
      </div>

      <div v-else-if="articles.length === 0" class="fr-alert fr-alert--info fr-mb-4w">
        <h3 class="fr-alert__title">Aucun article publié</h3>
        <p>Il n'y a pas encore d'article disponible dans le blog.</p>
      </div>

      <div v-else class="grid-articles">
        <div v-for="(article, index) in articles" :key="article.id" class="article-col">
          <BlogArticleCard :article="article">
            <template #controls>
              <AdminControls
                v-if="isAdminMode"
                direction="horizontal"
                :up-disabled="index === 0"
                :down-disabled="index === articles.length - 1"
                up-label="Déplacer vers la gauche"
                down-label="Déplacer vers la droite"
                edit-label="Modifier cet article"
                delete-label="Supprimer cet article"
                @up="moveUp(article.slug)"
                @down="moveDown(article.slug)"
                @edit="openEditForm(article)"
                @delete="triggerDelete(article)"
              />
            </template>
          </BlogArticleCard>
        </div>
      </div>

      <div v-if="isAdminMode" class="fr-mt-6w text-center fr-grid-row fr-grid-row--center">
        <div class="fr-col-auto">
          <DsfrButton @click="openAddForm">
            <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
            Ajouter un article
          </DsfrButton>
        </div>
      </div>

      <BlogArticleModal
        :opened="showModal"
        :title="editingArticle ? 'Modifier l’article' : 'Ajouter un article'"
        :initial-data="form"
        :is-submitting="isSubmitting"
        @close="showModal = false"
        @save="handleSave"
      />

      <ConfirmModal
        :opened="showDeleteConfirm"
        title="Supprimer l’article ?"
        :message="`Êtes-vous sûr de vouloir supprimer l'article « <strong>${deletingArticle?.title || ''}</strong> » ? Cette action est irréversible.`"
        confirm-button-label="Oui, supprimer"
        cancel-button-label="Annuler"
        :is-danger="true"
        @close="showDeleteConfirm = false"
        @confirm="confirmDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import BlogArticleCard, { type BlogArticleItem } from '@/components/blog/BlogArticleCard.vue'
import BlogArticleModal, { type BlogArticleFormData } from '@/components/blog/BlogArticleModal.vue'
import ConfirmModal from '@/components/shared/ConfirmModal.vue'
import * as api from '@/services/api'
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, reactive, ref } from 'vue'
import { useAdminModeStore } from '../stores/admin-mode'
import { AdminControls } from '../vue-guillotine'

const adminModeStore = useAdminModeStore()
const isAdminMode = computed(() => adminModeStore.isAdminMode)

const articles = ref<BlogArticleItem[]>([])
const isLoading = ref(false)
const isSubmitting = ref(false)

const showModal = ref(false)
const editingArticle = ref<BlogArticleItem | null>(null)

const form = reactive<BlogArticleFormData>({
  title: '',
  summary: '',
  bodyHtml: '',
  coverImageFile: null,
  currentCoverImage: null,
  is_published: true,
})

const showDeleteConfirm = ref(false)
const deletingArticle = ref<BlogArticleItem | null>(null)

const loadArticles = async () => {
  isLoading.value = true
  try {
    const data = await api.fetchResource(`${api.API_URL}/blog-articles/`)
    articles.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error('Erreur de chargement des articles :', err)
  } finally {
    isLoading.value = false
  }
}

const moveUp = async (slug: string) => {
  try {
    await api.postResource(`${api.API_URL}/blog-articles/${slug}/move-up/`)
    await loadArticles()
  } catch (err) {
    console.error('Erreur lors du déplacement vers le haut :', err)
  }
}

const moveDown = async (slug: string) => {
  try {
    await api.postResource(`${api.API_URL}/blog-articles/${slug}/move-down/`)
    await loadArticles()
  } catch (err) {
    console.error('Erreur lors du déplacement vers le bas :', err)
  }
}

const openAddForm = () => {
  editingArticle.value = null
  form.title = ''
  form.summary = ''
  form.bodyHtml = ''
  form.coverImageFile = null
  form.currentCoverImage = null
  form.is_published = true
  showModal.value = true
}

const openEditForm = (article: BlogArticleItem) => {
  editingArticle.value = article
  form.title = article.title
  form.summary = article.summary || ''
  const richTextBlock = (article.content || []).find((b: any) => b.type === 'rich_text')
  form.bodyHtml = richTextBlock ? richTextBlock.value : ''
  form.coverImageFile = null
  form.currentCoverImage = article.cover_image
  form.is_published = article.is_published
  showModal.value = true
}

const handleSave = async (data: BlogArticleFormData) => {
  isSubmitting.value = true
  try {
    const content = [{ type: 'rich_text', value: data.bodyHtml }]

    // We send multipart FormData to support cover image upload
    const formData = new FormData()
    formData.append('title', data.title)
    formData.append('summary', data.summary)
    formData.append('content', JSON.stringify(content))
    formData.append('is_published', String(data.is_published))
    if (data.coverImageFile) {
      formData.append('cover_image', data.coverImageFile)
    }

    if (editingArticle.value) {
      await api.patchResource(
        `${api.API_URL}/blog-articles/${editingArticle.value.slug}/`,
        formData
      )
    } else {
      await api.createResource(`${api.API_URL}/blog-articles/`, formData)
    }

    showModal.value = false
    await loadArticles()
  } catch (err) {
    console.error("Erreur lors de l'enregistrement de l'article :", err)
  } finally {
    isSubmitting.value = false
  }
}

const triggerDelete = (article: BlogArticleItem) => {
  deletingArticle.value = article
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  if (deletingArticle.value) {
    try {
      await api.deleteResource(`${api.API_URL}/blog-articles/${deletingArticle.value.slug}/`)
      showDeleteConfirm.value = false
      deletingArticle.value = null
      await loadArticles()
    } catch (err) {
      console.error("Erreur lors de la suppression de l'article :", err)
    }
  }
}

onMounted(() => {
  loadArticles()
})
</script>

<style scoped>
.grid-articles {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
  gap: 2rem;
  justify-content: center;
}

@media (min-width: 992px) {
  .grid-articles {
    grid-template-columns: repeat(3, 1fr);
  }
}

.article-col {
  display: flex;
}
</style>
