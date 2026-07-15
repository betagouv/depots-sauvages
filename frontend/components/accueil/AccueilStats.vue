<template>
  <div class="fr-py-6w stats-bar-wrapper">
    <div class="fr-py-0 stats-bar">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--gutters">
          <div
            v-for="(stat, index) in displayStats"
            :key="index"
            class="fr-col-12 fr-col-sm-6 fr-col-md-3"
          >
            <div class="stat-item">
              <div class="stat-number">{{ stat.number }}</div>
              <p class="stat-label">{{ stat.label }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Admin Controls -->
    <div v-if="isAdminMode" class="stats-admin-controls">
      <button
        class="admin-btn fr-icon-edit-line"
        title="Modifier les chiffres clés"
        @click="openEditModal"
      ></button>
    </div>

    <!-- Edit Modal -->
    <StatsEditModal
      :opened="showEditModal"
      :stats="displayStats"
      @close="showEditModal = false"
      @save="saveStats"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { SITE_CONTENT_SLUGS } from '../../constants/slugs'
import * as api from '../../services/api'
import { useAdminModeStore } from '../../stores/admin-mode'
import StatsEditModal from './StatsEditModal.vue'

interface StatItem {
  number: string
  label: string
}

const adminModeStore = useAdminModeStore()
const isAdminMode = computed(() => adminModeStore.isAdminMode)

const DEFAULT_STATS: StatItem[] = [
  { number: '600 m³', label: 'de déchets retirés par les auteurs' },
  { number: '500', label: 'procédures engagées' },
  { number: '26 000 €', label: "d'amendes prononcées" },
  { number: '300+', label: 'collectivités accompagnées' },
]

const statsRecord = ref<any>(null)
const existsInDb = ref(false)
const showEditModal = ref(false)

const displayStats = computed<StatItem[]>(() => {
  if (statsRecord.value && statsRecord.value.content) {
    const statsBlock = statsRecord.value.content.find((b: any) => b.type === 'stats_bar')
    if (statsBlock && Array.isArray(statsBlock.value)) {
      return statsBlock.value
    }
  }
  return DEFAULT_STATS
})

const loadStats = async () => {
  try {
    const data = await api.fetchResource(
      `${api.API_URL}/site-content/${SITE_CONTENT_SLUGS.HOME_STATS}/`
    )
    if (data) {
      statsRecord.value = data
      existsInDb.value = true
    }
  } catch (err) {
    existsInDb.value = false
  }
}

const openEditModal = () => {
  showEditModal.value = true
}

const saveStats = async (newStats: StatItem[]) => {
  try {
    const payload = {
      title: "Chiffres clés de l'accueil",
      slug: SITE_CONTENT_SLUGS.HOME_STATS,
      is_published: true,
      content: [
        {
          type: 'stats_bar',
          value: newStats,
        },
      ],
    }

    let data
    if (existsInDb.value) {
      data = await api.patchResource(
        `${api.API_URL}/site-content/${SITE_CONTENT_SLUGS.HOME_STATS}/`,
        payload
      )
    } else {
      data = await api.createResource(`${api.API_URL}/site-content/`, payload)
    }

    if (data) {
      statsRecord.value = data
      existsInDb.value = true
    }
    showEditModal.value = false
  } catch (err) {
    console.error('Error saving stats:', err)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stats-bar-wrapper {
  position: relative;
  background-color: var(--background-flat-blue-france);
}

.stats-bar {
  color: var(--text-inverted-blue-france);
}

.stat-item {
  padding-left: 1.5rem;
  border-left: 2px solid #6a6af4;
}

.stat-number {
  font-size: 2.5rem;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-inverted-blue-france);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 0;
  color: var(--text-inverted-blue-france);
}

.stats-admin-controls {
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
