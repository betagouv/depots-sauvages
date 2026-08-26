<template>
  <div class="pfmv-card fr-enlarge-link flex min-h-[26rem] w-full flex-col">
    <div class="card-image-wrapper">
      <img
        v-if="article.cover_image"
        :src="article.cover_image"
        :alt="article.title"
        class="card-image"
        loading="lazy"
      />
      <div v-else class="card-image-placeholder">
        <span class="fr-icon-article-line placeholder-icon" aria-hidden="true"></span>
      </div>
      <div v-if="!article.is_published" class="draft-badge">
        <span class="fr-badge fr-badge--warning fr-badge--sm">Brouillon</span>
      </div>
    </div>
    <div class="card-body">
      <h2 class="fr-h5 fr-mb-2w card-title">
        <router-link class="bg-none text-blue-hover" :to="`/blog/${article.slug}`">
          {{ article.title }}
        </router-link>
      </h2>
      <p v-if="article.summary" class="fr-text--sm fr-mb-3w card-summary">
        {{ article.summary }}
      </p>
      <div class="card-footer">
        <span class="card-date">Publié le {{ formattedDate }}</span>
        <div v-if="$slots.controls" class="card-controls">
          <slot name="controls" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export interface BlogArticleItem {
  id: number
  title: string
  slug: string
  summary?: string
  content?: any[]
  cover_image?: string | null
  is_published: boolean
  order: number
  created_at: string
  updated_at: string
}

const props = defineProps<{
  article: BlogArticleItem
}>()

const formattedDate = computed(() => {
  if (!props.article.created_at) return ''
  return new Date(props.article.created_at).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
})
</script>

<style scoped>
.pfmv-card {
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  position: relative;
  display: flex;
  flex-direction: column;
}

.pfmv-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: var(--border-active-blue-france);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  height: 12rem;
  background-color: var(--background-alt-grey);
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.pfmv-card:hover .card-image {
  transform: scale(1.03);
}

.card-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e8edff 0%, #f5f5fe 100%);
}

.placeholder-icon {
  font-size: 3rem;
  color: var(--text-action-high-blue-france);
  opacity: 0.6;
}

.draft-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 2;
}

.card-body {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 1.5rem;
}

.card-title {
  color: var(--text-title-grey);
  font-size: 1.2rem;
  line-height: 1.4;
  margin-bottom: 0.75rem;
}

.text-blue-hover {
  color: var(--text-title-grey);
  text-decoration: none;
  transition: color 0.15s ease;
}

.pfmv-card:hover .text-blue-hover {
  color: var(--text-action-high-blue-france);
}

.card-summary {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--text-mention-grey);
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.card-footer {
  margin-top: auto;
  padding-top: 1rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  border-top: 1px solid var(--border-default-grey);
}

.card-date {
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.card-controls {
  display: flex;
  align-items: center;
  position: relative;
  z-index: 20;
}
</style>
