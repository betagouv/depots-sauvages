<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <!-- Filter Bar -->
    <div class="bo-filter-bar-container">
      <div class="bo-search-row">
        <label class="bo-filter-label" for="user-search-input">Rechercher un utilisateur</label>
        <input
          id="user-search-input"
          v-model="filters.search"
          type="text"
          class="fr-input bo-w-full"
          placeholder="🔍 Rechercher par e-mail, nom, prénom, SIRET, SIREN ou organisation..."
        />
      </div>

      <div class="bo-filters-grid">
        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-procedures-count">Nombre de procédures</label>
          <select id="filter-procedures-count" v-model="filters.hasProcedures" class="fr-select">
            <option value="Tous">Tous</option>
            <option value="Non">Aucune procédure (0)</option>
            <option value="Oui">Au moins une procédure (>0)</option>
          </select>
        </div>

        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-proconnect">Compte ProConnect</label>
          <select id="filter-proconnect" v-model="filters.hasProconnect" class="fr-select">
            <option value="Tous">Tous</option>
            <option value="Oui">Lié à ProConnect</option>
            <option value="Non">Non lié</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Count display / info bar & Export CSV & Pagination controls -->
    <div
      class="fr-mb-2w bo-info-bar"
      style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem"
    >
      <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap">
        <span class="fr-text--sm fr-text-mention--grey fr-mb-0">
          Nombre d'utilisateurs : <strong>{{ store.totalUsersCount }}</strong> au total
        </span>
        <button
          class="fr-btn fr-btn--sm fr-btn--secondary"
          type="button"
          :disabled="isExporting"
          @click="exportCsv"
        >
          <span class="fr-icon-download-line fr-mr-1w" aria-hidden="true"></span>
          {{ isExporting ? 'Export en cours...' : 'Exporter en CSV' }}
        </button>
      </div>

      <DsfrPagination
        v-if="totalPages > 1"
        :current-page="page - 1"
        :pages="pages"
        @update:current-page="(idx) => changePage(idx + 1)"
      />
    </div>

    <!-- Users Grid Table -->
    <div ref="tableContainerRef" class="bo-table-container">
      <table class="bo-table">
        <thead>
          <tr>
            <th class="bo-th-customizer">
              <div class="bo-customizer-container">
                <button
                  class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline bo-customizer-btn-toggle"
                  @click="showCustomizer = !showCustomizer"
                  title="Personnaliser les colonnes"
                >
                  <span class="fr-icon-settings-5-line" aria-hidden="true"></span>
                </button>
                <div
                  v-if="showCustomizer"
                  class="bo-customizer-popover bo-customizer-popover--left"
                >
                  <div class="bo-customizer-header">
                    <div class="bo-customizer-title bo-customizer-title--no-border">
                      Colonnes à afficher
                    </div>
                    <button
                      class="fr-btn fr-btn--sm fr-btn--tertiary-no-outline bo-btn-close-sm"
                      @click="showCustomizer = false"
                    >
                      ✕
                    </button>
                  </div>
                  <div class="bo-customizer-list">
                    <label
                      v-for="col in customizableColumns"
                      :key="col.key"
                      class="bo-customizer-item"
                    >
                      <input type="checkbox" v-model="visibleColumns[col.key]" />
                      <span>{{ col.label }}</span>
                    </label>
                  </div>
                </div>
              </div>
            </th>
            <th v-if="visibleColumns.id">ID</th>
            <th v-if="visibleColumns.email">E-mail</th>
            <th v-if="visibleColumns.name">Nom & Prénom</th>
            <th v-if="visibleColumns.proconnect">Lien ProConnect</th>
            <th v-if="visibleColumns.siret">SIRET / SIREN</th>
            <th v-if="visibleColumns.organization">Organisation</th>
            <th v-if="visibleColumns.procedures_count">Nb Procédures</th>
            <th v-if="visibleColumns.date_joined">Création</th>
            <th v-if="visibleColumns.last_login">Dernière connexion</th>
            <th v-if="visibleColumns.is_staff">Statut équipe</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td colspan="11" class="fr-text--center fr-py-3w">
              Chargement des utilisateurs...
            </td>
          </tr>
          <tr v-else-if="users.length === 0">
            <td colspan="11" class="fr-text--center fr-py-3w fr-text-mention--grey">
              Aucun utilisateur trouvé pour ces critères.
            </td>
          </tr>
          <tr
            v-for="user in users"
            :key="user.id"
            :class="{ 'bo-row-zero-procedures': user.procedures_count === 0 }"
          >
            <td></td>
            <td v-if="visibleColumns.id" class="bo-fw-bold">#{{ user.id }}</td>
            <td v-if="visibleColumns.email">
              <span class="bo-truncate" :title="user.email || '—'">
                {{ user.email || '—' }}
              </span>
            </td>
            <td v-if="visibleColumns.name">
              {{ formatUserName(user) }}
            </td>
            <td v-if="visibleColumns.proconnect">
              <span
                v-if="user.has_proconnect"
                class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon"
                title="Compte associé à ProConnect"
              >
                ProConnect
              </span>
              <span
                v-else
                class="fr-badge fr-badge--sm fr-badge--warning fr-badge--no-icon"
                title="Non associé"
              >
                Non lié
              </span>
            </td>
            <td v-if="visibleColumns.siret">
              <div v-if="user.proconnect_profile?.siret">
                <span class="fr-text--xs bo-fw-semibold" style="display: block">
                  {{ user.proconnect_profile.siret }}
                </span>
                <span
                  v-if="user.proconnect_profile?.siren && user.proconnect_profile.siren !== user.proconnect_profile.siret"
                  class="fr-text--xs fr-text-mention--grey"
                >
                  SIREN: {{ user.proconnect_profile.siren }}
                </span>
              </div>
              <span v-else class="fr-text-mention--grey">—</span>
            </td>
            <td v-if="visibleColumns.organization">
              <span
                v-if="user.proconnect_profile?.organization_label"
                class="bo-truncate"
                :title="user.proconnect_profile.organization_label"
              >
                {{ user.proconnect_profile.organization_label }}
              </span>
              <span v-else class="fr-text-mention--grey">—</span>
            </td>
            <td v-if="visibleColumns.procedures_count">
              <span
                v-if="user.procedures_count === 0"
                class="fr-badge fr-badge--sm fr-badge--warning fr-badge--no-icon"
                style="font-weight: 700"
              >
                0 procédure
              </span>
              <span
                v-else
                class="fr-badge fr-badge--sm fr-badge--success fr-badge--no-icon"
              >
                {{ user.procedures_count }}
              </span>
            </td>
            <td v-if="visibleColumns.date_joined" class="fr-text--xs">
              {{ formatDate(user.date_joined) }}
            </td>
            <td v-if="visibleColumns.last_login" class="fr-text--xs">
              {{ formatDate(user.last_login) }}
            </td>
            <td v-if="visibleColumns.is_staff">
              <span
                v-if="user.is_staff"
                class="fr-badge fr-badge--sm fr-badge--purple-glycine fr-badge--no-icon"
              >
                Équipe
              </span>
              <span v-else class="fr-text--xs fr-text-mention--grey">Utilisateur</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Bottom Pagination controls -->
    <div v-if="totalPages > 1" class="fr-mt-3w" style="display: flex; justify-content: flex-end">
      <DsfrPagination
        :current-page="page - 1"
        :pages="pages"
        @update:current-page="(idx) => changePage(idx + 1)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { API_URL } from '@/services/api'
import { useBackofficeStore, type BackofficeUser } from '@/stores/backoffice'
import { parseQueryParam } from '@/utils/backoffice'
import { formatDate } from '@/utils/date'
import dayjs from 'dayjs'
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const store = useBackofficeStore()
const route = useRoute()
const router = useRouter()

const isLoading = ref(false)
const isExporting = ref(false)
const showCustomizer = ref(false)

const filters = reactive({
  search: parseQueryParam(route.query.user_search, ''),
  hasProcedures: parseQueryParam(route.query.has_procedures, 'Tous'),
  hasProconnect: parseQueryParam(route.query.has_proconnect, 'Tous'),
})

const page = ref(parseQueryParam(route.query.page, 1))
const pageSize = 50

const customizableColumns = [
  { key: 'id', label: 'ID' },
  { key: 'email', label: 'E-mail' },
  { key: 'name', label: 'Nom & Prénom' },
  { key: 'proconnect', label: 'Lien ProConnect' },
  { key: 'siret', label: 'SIRET / SIREN' },
  { key: 'organization', label: 'Organisation' },
  { key: 'procedures_count', label: 'Nombre de procédures' },
  { key: 'date_joined', label: 'Date de création' },
  { key: 'last_login', label: 'Dernière connexion' },
  { key: 'is_staff', label: 'Statut équipe' },
]

const visibleColumns = reactive<Record<string, boolean>>({
  id: true,
  email: true,
  name: true,
  proconnect: true,
  siret: true,
  organization: true,
  procedures_count: true,
  date_joined: true,
  last_login: true,
  is_staff: true,
})

const formatUserName = (user: BackofficeUser) => {
  const parts = [user.first_name, user.last_name].filter(Boolean)
  return parts.length ? parts.join(' ') : '—'
}

const users = computed(() => store.users)

const totalPages = computed(() => Math.ceil(store.totalUsersCount / pageSize) || 1)

const pages = computed(() => {
  return Array.from({ length: totalPages.value }, (_, i) => ({
    label: String(i + 1),
    title: `Page ${i + 1}`,
    href: '#',
  }))
})

const tableContainerRef = ref<HTMLElement | null>(null)

const changePage = (newPage: number) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage
    updateUrlParams()
    loadUsers()
    if (tableContainerRef.value) {
      tableContainerRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }
}

const updateUrlParams = () => {
  const query: Record<string, string> = { ...route.query } as Record<string, string>

  if (page.value > 1) query.page = String(page.value)
  else delete query.page

  if (filters.search) query.user_search = filters.search
  else delete query.user_search

  if (filters.hasProcedures !== 'Tous') query.has_procedures = filters.hasProcedures
  else delete query.has_procedures

  if (filters.hasProconnect !== 'Tous') query.has_proconnect = filters.hasProconnect
  else delete query.has_proconnect

  try {
    const res = router.replace({ query })
    if (res && typeof res.catch === 'function') {
      res.catch(() => {})
    }
  } catch {
    // ignore
  }
}

const loadUsers = async () => {
  isLoading.value = true
  try {
    await store.fetchUsers({
      page: page.value,
      page_size: pageSize,
      search: filters.search || undefined,
      has_procedures: filters.hasProcedures !== 'Tous' ? filters.hasProcedures : undefined,
      has_proconnect: filters.hasProconnect !== 'Tous' ? filters.hasProconnect : undefined,
    })
  } finally {
    isLoading.value = false
  }
}

// Watch filters to reset page to 1, update URL and load users
watch(
  () => [filters.search, filters.hasProcedures, filters.hasProconnect],
  () => {
    page.value = 1
    updateUrlParams()
    loadUsers()
  }
)

// Sync route query changes to backend fetch
watch(
  () => route.query,
  async (newQuery) => {
    if (route.path === '/utilisateurs-liste') {
      const qPage = parseQueryParam(newQuery.page, 1)
      const qSearch = parseQueryParam(newQuery.user_search, '')
      const qHasProc = parseQueryParam(newQuery.has_procedures, 'Tous')
      const qHasPc = parseQueryParam(newQuery.has_proconnect, 'Tous')

      if (
        page.value !== qPage ||
        filters.search !== qSearch ||
        filters.hasProcedures !== qHasProc ||
        filters.hasProconnect !== qHasPc
      ) {
        page.value = qPage
        filters.search = qSearch
        filters.hasProcedures = qHasProc
        filters.hasProconnect = qHasPc
        await loadUsers()
      }
    }
  }
)

const exportCsv = async () => {
  isExporting.value = true
  try {
    const params = new URLSearchParams()
    if (filters.search) params.append('search', filters.search)
    if (filters.hasProcedures !== 'Tous') params.append('has_procedures', filters.hasProcedures)
    if (filters.hasProconnect !== 'Tous') params.append('has_proconnect', filters.hasProconnect)

    const queryStr = params.toString() ? `?${params.toString()}` : ''
    const exportUrl = `${API_URL}/backoffice-users/export-csv/${queryStr}`

    // Trigger download
    const link = document.createElement('a')
    link.href = exportUrl
    link.setAttribute('download', `utilisateurs_${dayjs().format('YYYYMMDD_HHmm')}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    console.error('Failed to export CSV:', error)
  } finally {
    isExporting.value = false
  }
}

// Initial load if route.query didn't trigger it (e.g. nested tab without route change)
onMounted(() => {
  if (store.users.length === 0) {
    loadUsers()
  }
})
</script>

<style scoped>
.bo-row-zero-procedures {
  background-color: var(--background-contrast-warning) !important;
}
</style>
