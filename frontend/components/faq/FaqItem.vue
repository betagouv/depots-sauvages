<template>
  <section
    :id="item.slug"
    class="fr-accordion faq-item-section"
    :class="{ 'faq-draft': !item.is_published }"
  >
    <div
      class="fr-grid-row fr-grid-row--middle faq-item-header"
      :class="{ 'faq-item-header--expanded': isExpanded }"
    >
      <div class="fr-col">
        <h3 class="fr-accordion__title">
          <button
            class="fr-accordion__btn"
            :aria-expanded="isExpanded"
            :aria-controls="'accordion-' + item.id"
            @click="toggleAccordion"
          >
            {{ item.title }}
            <span v-if="!item.is_published" class="fr-badge fr-badge--warning fr-ml-2w"
              >Brouillon</span
            >
          </button>
        </h3>
      </div>

      <div class="fr-col-auto fr-pr-2w">
        <CopyButton
          :text="copyUrl"
          title="Copier le lien de cette question"
          copied-title="Lien copié !"
        />
      </div>

      <AdminControls
        v-if="isAdminMode"
        class="fr-col-auto fr-pr-2w faq-item-admin-controls"
        :up-disabled="index === 0"
        :down-disabled="index === listLength - 1"
        up-label="Monter cette question"
        down-label="Descendre cette question"
        edit-label="Modifier cette question"
        delete-label="Supprimer cette question"
        @up="$emit('up')"
        @down="$emit('down')"
        @edit="$emit('edit')"
        @delete="$emit('delete')"
      />
    </div>

    <div
      class="fr-collapse"
      :id="'accordion-' + item.id"
      :class="{ 'fr-collapse--expanded': isExpanded }"
      :style="isExpanded ? 'max-height: none;' : undefined"
    >
      <div class="fr-p-3w">
        <BlockRenderer :blocks="item.content" />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import CopyButton from '@/components/shared/CopyButton.vue'
import { useAnchorScroll } from '@/composables/useAnchorScroll'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { AdminControls, BlockRenderer } from '../../vue-guillotine'

interface FAQItem {
  id: number
  title: string
  slug: string
  content: Array<{ type: string; value: string }>
  order: number
  is_published: boolean
}

const props = defineProps<{
  item: FAQItem
  index: number
  listLength: number
  isAdminMode: boolean
}>()

defineEmits<{
  (e: 'up'): void
  (e: 'down'): void
  (e: 'edit'): void
  (e: 'delete'): void
 }>()

const route = useRoute()
const isExpanded = ref(false)

const copyUrl = computed(() => {
  if (typeof window === 'undefined') return ''
  return `${window.location.origin}/faq/${props.item.slug}`
})

const toggleAccordion = () => {
  isExpanded.value = !isExpanded.value
}

useAnchorScroll(isExpanded, props.item.slug, props.item.title)
</script>

<style scoped>
.faq-draft {
  opacity: 0.75;
  border-left: 4px solid #ffca00;
}
.faq-item-section {
  position: relative;
  margin-bottom: 1.5rem !important;
  border: 1px solid var(--border-default-grey) !important;
  border-radius: 8px !important;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 145, 0.02);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}
.faq-item-section:hover {
  border-color: var(--border-default-blue-france) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.05);
}
.faq-item-header {
  transition: background-color 0.2s ease;
}
.faq-item-header--expanded {
  background-color: var(--background-alt-blue-france);
}
.faq-item-header :deep(.fr-accordion__title) {
  margin: 0;
}
.faq-item-header :deep(.fr-accordion__btn) {
  padding: 1.25rem 1.5rem;
  background-color: transparent !important;
}
.faq-item-section :deep(.fr-accordion::before) {
  display: none !important;
}

@media (max-width: 767.98px) {
  .faq-item-admin-controls {
    flex: 0 0 100%;
    max-width: 100%;
    padding-left: 1.5rem !important;
    padding-bottom: 1.25rem !important;
    padding-top: 0.5rem !important;
  }
}
</style>
