<template>
  <div>
    <!-- Bandeau Webinaire -->
    <div v-if="notice.is_published || isAdminMode" class="webinaire-notice-wrapper">
      <DsfrNotice
        :title="notice.title"
        :closeable="false"
        class="fr-mb-0"
        :class="{ 'notice-draft': !notice.is_published }"
      >
        <template #desc>
          <router-link to="/rdv" class="fr-link fr-ml-1w"> S'inscrire au webinaire </router-link>
          <span v-if="!notice.is_published" class="fr-badge fr-badge--warning fr-ml-2w"
            >Brouillon</span
          >
        </template>
      </DsfrNotice>
      <div v-if="isAdminMode" class="notice-admin-controls">
        <button
          class="admin-btn fr-icon-edit-line"
          title="Modifier la notice"
          @click="openEditModal"
        ></button>
      </div>
    </div>

    <AccueilHero />
    <AccueilOrientation />
    <AccueilPouvoirAgir />
    <AccueilReassurance />
    <AccueilTemoignages />
    <AccueilStats />
    <AccueilCta />

    <!-- Modal d'édition de la notice -->
    <DsfrModal
      :opened="showEditModal"
      title="Modifier l'annonce du webinaire"
      :is-alert="true"
      @close="showEditModal = false"
    >
      <form @submit.prevent="saveNotice" class="fr-container--fluid fr-p-0">
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12">
            <div class="fr-input-group">
              <label class="fr-label" for="notice-title">Texte de l'annonce</label>
              <textarea
                v-model="editForm.title"
                class="fr-input"
                id="notice-title"
                required
                rows="3"
                placeholder="Ex: Prochain webinaire de : jeudi 23 juillet à 11h00..."
              ></textarea>
            </div>
          </div>

          <div class="fr-col-12">
            <div class="fr-checkbox-group">
              <input v-model="editForm.is_published" type="checkbox" id="notice-published" />
              <label class="fr-label" for="notice-published">Publié (visible de tous)</label>
            </div>
          </div>

          <div class="fr-col-12 fr-mt-3w text-right">
            <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--right">
              <li>
                <button
                  type="button"
                  class="fr-btn fr-btn--secondary"
                  @click="showEditModal = false"
                >
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
  </div>
</template>

<script setup lang="ts">
import AccueilCta from '@/components/accueil/AccueilCta.vue'
import AccueilHero from '@/components/accueil/AccueilHero.vue'
import AccueilOrientation from '@/components/accueil/AccueilOrientation.vue'
import AccueilPouvoirAgir from '@/components/accueil/AccueilPouvoirAgir.vue'
import AccueilReassurance from '@/components/accueil/AccueilReassurance.vue'
import AccueilStats from '@/components/accueil/AccueilStats.vue'
import AccueilTemoignages from '@/components/accueil/AccueilTemoignages.vue'
import { useTallyRoutes } from '@/composables/useTally'
import { SITE_CONTENT_SLUGS } from '@/constants/slugs'
import * as api from '@/services/api'
import { DsfrModal, DsfrNotice } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useAdminModeStore } from '../stores/admin-mode'

useTallyRoutes({
  '/simulateur': { formId: 'A7xA8z', options: { layout: 'modal', width: 900 } },
  '/calculateur': { formId: '9qElYG', options: { layout: 'modal', width: 900 } },
})

const adminModeStore = useAdminModeStore()
const isAdminMode = computed(() => adminModeStore.isAdminMode)

const DEFAULT_TITLE =
  'Prochain webinaire : une heure pour comprendre la procédure et poser vos questions.'

const notice = ref({
  id: null as number | null,
  title: DEFAULT_TITLE,
  is_published: true,
  slug: SITE_CONTENT_SLUGS.WEBINAIRE_NOTICE,
})

const existsInDb = ref(false)
const showEditModal = ref(false)
const editForm = ref({
  title: '',
  is_published: true,
})

const loadNotice = async () => {
  try {
    const data = await api.fetchResource(
      `${api.API_URL}/site-content/${SITE_CONTENT_SLUGS.WEBINAIRE_NOTICE}/`
    )
    if (data) {
      notice.value = data
      existsInDb.value = true
    }
  } catch (err) {
    // If not found or error, we keep the default notice structure
    existsInDb.value = false
  }
}

const openEditModal = () => {
  editForm.value = {
    title: notice.value.title,
    is_published: notice.value.is_published,
  }
  showEditModal.value = true
}

const saveNotice = async () => {
  try {
    const payload = {
      title: editForm.value.title,
      is_published: editForm.value.is_published,
      slug: SITE_CONTENT_SLUGS.WEBINAIRE_NOTICE,
      content: [],
    }

    let data
    if (existsInDb.value) {
      data = await api.patchResource(
        `${api.API_URL}/site-content/${SITE_CONTENT_SLUGS.WEBINAIRE_NOTICE}/`,
        payload
      )
    } else {
      data = await api.createResource(`${api.API_URL}/site-content/`, payload)
    }

    if (data) {
      notice.value = data
      existsInDb.value = true
    }
    showEditModal.value = false
  } catch (err) {
    console.error('Error saving webinaire notice:', err)
  }
}

onMounted(() => {
  loadNotice()
})
</script>

<style scoped>
.webinaire-notice-wrapper {
  position: relative;
}

.notice-draft {
  opacity: 0.8;
  border-left: 4px solid var(--border-plain-warning);
}

.notice-admin-controls {
  position: absolute;
  top: 50%;
  right: 1.5rem;
  transform: translateY(-50%);
  z-index: 10;
}

.admin-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50% !important;
  display: inline-flex;
  align-hidden: true;
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
