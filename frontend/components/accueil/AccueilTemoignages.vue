<template>
  <div class="fr-background-alt--blue-france fr-py-8w testimonials-wrapper">
    <div class="fr-container">
      <h2 class="fr-h2 fr-mb-6w premium-text-center">{{ displayTitle }}</h2>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div
          v-for="(item, index) in displayTestimonials"
          :key="index"
          class="fr-col-12 fr-col-md-6"
        >
          <blockquote class="fr-quote quote-custom">
            <span class="quote-icon">“</span>
            <p class="fr-text fr-mb-3w">
              {{ item.quote }}
            </p>
            <cite class="fr-quote__author quote-author">
              <strong>{{ item.author }}</strong>
              <span class="fr-quote__source quote-source">
                {{ item.source }}
              </span>
            </cite>
          </blockquote>
        </div>
      </div>
    </div>

    <div v-if="isAdminMode" class="testimonials-admin-controls">
      <button
        class="admin-btn fr-icon-edit-line"
        title="Modifier les témoignages"
        @click="openEditModal"
      ></button>
    </div>

    <TestimonialsEditModal
      :opened="showEditModal"
      :title="displayTitle"
      :testimonials="displayTestimonials"
      @close="showEditModal = false"
      @save="saveTestimonials"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { SITE_CONTENT_SLUGS } from '../../constants/slugs'
import * as api from '../../services/api'
import { useAdminModeStore } from '../../stores/admin-mode'
import TestimonialsEditModal from './TestimonialsEditModal.vue'

interface TestimonialItem {
  quote: string
  author: string
  source: string
}

const adminModeStore = useAdminModeStore()
const isAdminMode = computed(() => adminModeStore.isAdminMode)

const DEFAULT_TITLE = "Ils ont agi avec Protect'Envi"
const DEFAULT_TESTIMONIALS: TestimonialItem[] = [
  {
    quote:
      "Protect'Envi permet de générer des courriers parfaitement structurés, que nous envoyons aux auteurs présumés des dépôts. Sur les trois derniers courriers envoyés, j'ai obtenu un retour en moins d'une semaine à chaque fois.",
    author: 'Philippe Barneron',
    source: 'Maire de Peyrins (26) — commune de 2 700 habitants',
  },
  {
    quote:
      "Travaillant seul, sans véritable soutien juridique en interne, cet accompagnement a été un véritable soulagement. Il m'a permis d'avancer dans une procédure qui stagnait depuis plus d'un an : l'auteur des faits a commencé à retirer ses déchets.",
    author: 'Ludovic Caramel',
    source: 'Police municipale de Saint-Sulpice-de-Royan (17) — commune de 3 450 habitants',
  },
]

const testimonialsRecord = ref<any>(null)
const existsInDb = ref(false)
const showEditModal = ref(false)

const displayTitle = computed<string>(() => {
  return testimonialsRecord.value?.title || DEFAULT_TITLE
})

const displayTestimonials = computed<TestimonialItem[]>(() => {
  if (testimonialsRecord.value && testimonialsRecord.value.content) {
    const block = testimonialsRecord.value.content.find((b: any) => b.type === 'testimonials')
    if (block && Array.isArray(block.value)) {
      return block.value
    }
  }
  return DEFAULT_TESTIMONIALS
})

const loadTestimonials = async () => {
  try {
    const data = await api.fetchResource(
      `${api.API_URL}/site-content/${SITE_CONTENT_SLUGS.HOME_TESTIMONIALS}/`
    )
    if (data) {
      testimonialsRecord.value = data
      existsInDb.value = true
    }
  } catch (err) {
    existsInDb.value = false
  }
}

const openEditModal = () => {
  showEditModal.value = true
}

const saveTestimonials = async (payload: { title: string; testimonials: TestimonialItem[] }) => {
  try {
    const body = {
      title: payload.title,
      slug: SITE_CONTENT_SLUGS.HOME_TESTIMONIALS,
      is_published: true,
      content: [
        {
          type: 'testimonials',
          value: payload.testimonials,
        },
      ],
    }

    let data
    if (existsInDb.value) {
      data = await api.patchResource(
        `${api.API_URL}/site-content/${SITE_CONTENT_SLUGS.HOME_TESTIMONIALS}/`,
        body
      )
    } else {
      data = await api.createResource(`${api.API_URL}/site-content/`, body)
    }

    if (data) {
      testimonialsRecord.value = data
      existsInDb.value = true
    }
    showEditModal.value = false
  } catch (err) {
    console.error('Error saving testimonials:', err)
  }
}

onMounted(() => {
  loadTestimonials()
})
</script>

<style scoped>
.testimonials-wrapper {
  position: relative;
}

.quote-custom {
  background: var(--background-default-grey);
  box-shadow: var(--premium-shadow);
  border-radius: 8px;
  padding: 2.5rem 2rem 2rem 2rem;
  position: relative;
  margin: 0;
  height: 100%;
}

.quote-icon {
  font-family: Marianne, Arial, sans-serif;
  font-size: 5rem;
  color: var(--background-active-blue-france);
  opacity: 0.2;
  position: absolute;
  top: -10px;
  left: 15px;
  line-height: 1;
}

.quote-author {
  font-size: 0.9rem;
}

.quote-source {
  display: block;
  font-weight: normal;
  color: var(--text-mention-grey);
}

.testimonials-admin-controls {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 10;
}

.admin-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50% !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-default-grey) !important;
  border: 1px solid var(--border-default-grey) !important;
  color: var(--text-action-high-blue-france) !important;
  padding: 0 !important;
  min-height: auto !important;
  transition: all 0.15s ease-in-out;
  cursor: pointer;
}

.admin-btn:hover {
  background-color: var(--background-alt-blue-france) !important;
  border-color: var(--border-default-blue-france) !important;
  color: var(--text-active-blue-france) !important;
}
</style>
