<template>
  <div class="fr-container fr-py-4w">
    <DsfrBreadcrumb :links="breadcrumbLinks" class="fr-mb-4w" />

    <div v-if="isLoading" class="text-center fr-py-6w">
      <p class="fr-text--lead">Chargement de l'article...</p>
    </div>

    <div v-else-if="!article" class="fr-alert fr-alert--error fr-mb-4w">
      <h3 class="fr-alert__title">Article introuvable</h3>
      <p>Cet article n'existe pas ou n'est plus disponible.</p>
      <router-link to="/blog" class="fr-btn fr-btn--secondary fr-mt-2w">
        Retour aux articles
      </router-link>
    </div>

    <article v-else class="blog-detail-container">
      <div v-if="!article.is_published" class="fr-alert fr-alert--warning fr-mb-4w">
        <p>
          <strong>Mode brouillon :</strong> Cet article n'est actuellement visible que par les
          administrateurs.
        </p>
      </div>

      <div class="article-header fr-mb-4w">
        <div class="header-title-row">
          <h1 class="fr-h1 fr-mb-2w">{{ article.title }}</h1>
          <div v-if="isAdminMode" class="admin-header-actions">
            <button
              class="admin-btn fr-icon-edit-line"
              title="Modifier cet article"
              @click="openEditModal"
            ></button>
          </div>
        </div>
        <p class="fr-text--sm text-mention-grey">
          Publié le {{ formattedDate }}
          <span v-if="article.updated_at && article.updated_at !== article.created_at">
            (Mis à jour le {{ formattedUpdateDate }})
          </span>
        </p>
      </div>

      <div v-if="article.cover_image" class="article-hero-banner fr-mb-6w">
        <img :src="article.cover_image" :alt="article.title" class="hero-image" />
      </div>

      <div v-if="article.summary" class="article-summary-lead fr-mb-4w">
        <p class="fr-text--lead">
          {{ article.summary }}
        </p>
      </div>

      <div class="article-body">
        <BlockRenderer v-if="article.content && article.content.length" :blocks="article.content" />
      </div>

      <div class="article-footer fr-mt-8w fr-pt-4w">
        <router-link
          to="/blog"
          class="fr-btn fr-btn--secondary fr-icon-arrow-left-line fr-btn--icon-left"
        >
          Tous les articles
        </router-link>
      </div>

      <BlogArticleModal
        :opened="showModal"
        title="Modifier l’article"
        :initial-data="form"
        :is-submitting="isSubmitting"
        @close="showModal = false"
        @save="handleSave"
      />
    </article>
  </div>
</template>

<script setup lang="ts">
import type { BlogArticleItem } from '@/components/blog/BlogArticleCard.vue'
import BlogArticleModal, { type BlogArticleFormData } from '@/components/blog/BlogArticleModal.vue'
import * as api from '@/services/api'
import { DsfrBreadcrumb } from '@gouvminint/vue-dsfr'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminModeStore } from '../stores/admin-mode'
import { BlockRenderer } from '../vue-guillotine'

const route = useRoute()
const router = useRouter()
const adminModeStore = useAdminModeStore()
const isAdminMode = computed(() => adminModeStore.isAdminMode)

const article = ref<BlogArticleItem | null>(null)
const isLoading = ref(true)
const isSubmitting = ref(false)
const showModal = ref(false)

const form = reactive<BlogArticleFormData>({
  title: '',
  summary: '',
  bodyHtml: '',
  coverImageFile: null,
  currentCoverImage: null,
  is_published: true,
})

const breadcrumbLinks = computed(() => [
  { text: 'Accueil', to: '/' },
  { text: 'Blog', to: '/blog' },
  { text: article.value ? article.value.title : 'Article', to: route.path },
])

const formattedDate = computed(() => {
  if (!article.value?.created_at) return ''
  return new Date(article.value.created_at).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
})

const formattedUpdateDate = computed(() => {
  if (!article.value?.updated_at) return ''
  return new Date(article.value.updated_at).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
})

const loadArticle = async () => {
  isLoading.value = true
  const slug = route.params.slug as string
  try {
    const data = await api.fetchResource(`${api.API_URL}/blog-articles/${slug}/`)
    article.value = data
  } catch (err) {
    console.error('Erreur chargement article :', err)
    article.value = null
  } finally {
    isLoading.value = false
  }
}

const openEditModal = () => {
  if (!article.value) return
  form.title = article.value.title
  form.summary = article.value.summary || ''
  const richTextBlock = (article.value.content || []).find((b: any) => b.type === 'rich_text')
  form.bodyHtml = richTextBlock ? richTextBlock.value : ''
  form.coverImageFile = null
  form.currentCoverImage = article.value.cover_image
  form.is_published = article.value.is_published
  showModal.value = true
}

const handleSave = async (data: BlogArticleFormData) => {
  if (!article.value) return
  isSubmitting.value = true
  try {
    const content = [{ type: 'rich_text', value: data.bodyHtml }]
    const formData = new FormData()
    formData.append('title', data.title)
    formData.append('summary', data.summary)
    formData.append('content', JSON.stringify(content))
    formData.append('is_published', String(data.is_published))
    if (data.coverImageFile) {
      formData.append('cover_image', data.coverImageFile)
    }

    const updated = await api.patchResource(
      `${api.API_URL}/blog-articles/${article.value.slug}/`,
      formData
    )

    showModal.value = false
    // If slug changed, redirect to new URL
    if (updated?.slug && updated.slug !== article.value.slug) {
      router.replace(`/blog/${updated.slug}`)
    } else {
      article.value = updated
    }
  } catch (err) {
    console.error("Erreur lors de l'enregistrement de l'article :", err)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadArticle()
})
</script>

<style scoped>
.blog-detail-container {
  max-width: 900px;
  margin: 0 auto;
}

.header-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.admin-header-actions {
  display: flex;
  align-items: center;
}

.admin-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50% !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-default-grey) !important;
  border: 1px solid var(--border-default-grey) !important;
  color: var(--text-action-high-blue-france) !important;
  padding: 0 !important;
  transition: all 0.15s ease-in-out;
  cursor: pointer;
}

.admin-btn:hover {
  background-color: var(--background-alt-blue-france) !important;
  border-color: var(--border-default-blue-france) !important;
}

.text-mention-grey {
  color: var(--text-mention-grey);
}

.article-hero-banner {
  width: 100%;
  max-height: 450px;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.hero-image {
  width: 100%;
  height: 100%;
  max-height: 450px;
  object-fit: cover;
  display: block;
}

.article-summary-lead {
  border-left: 4px solid var(--border-default-blue-france);
  padding-left: 1.5rem;
  font-style: italic;
}

.article-body {
  line-height: 1.8;
  font-size: 1.1rem;
}

.article-footer {
  border-top: 1px solid var(--border-default-grey);
}
</style>
