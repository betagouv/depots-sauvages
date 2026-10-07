<template>
  <div
    class="fr-tabs__panel fr-tabs__panel--selected proconnect-config-panel"
    role="tabpanel"
    tabindex="0"
  >
    <div class="bo-header-row fr-mb-3w">
      <div class="bo-header-row__title">
        <h2 class="fr-h3 fr-mb-0-5v">
          <span
            class="fr-icon-lock-line fr-text-title-blue-france fr-mr-1w"
            aria-hidden="true"
          ></span>
          Règles d’accès ProConnect
        </h2>
        <p class="fr-text--sm fr-text-mention-grey fr-mb-0">
          Définissez les organismes publics habilités via leurs catégories juridiques ou via une
          liste blanche de SIREN.
        </p>
      </div>

      <div class="bo-header-row__actions">
        <button
          v-if="hasUnsavedChanges"
          type="button"
          class="fr-btn fr-btn--secondary fr-btn--sm"
          :disabled="isSaving || isLoading"
          @click="resetChanges"
        >
          <span class="fr-icon-arrow-go-back-line fr-mr-1w" aria-hidden="true"></span>
          Annuler les modifications
        </button>
        <button
          type="button"
          class="fr-btn fr-btn--primary fr-btn--sm"
          :class="{ 'fr-btn--secondary': !hasUnsavedChanges }"
          :disabled="isSaving || isLoading || !hasUnsavedChanges"
s          @click="saveConfig"
        >
          <span
            :class="isSaving ? 'fr-icon-refresh-line' : 'fr-icon-checkbox-circle-line'"
            class="fr-mr-1w"
            aria-hidden="true"
          ></span>
          {{
            isSaving
              ? 'Enregistrement...'
              : hasUnsavedChanges
                ? `Enregistrer (${unsavedCount})`
                : 'À jour'
          }}
        </button>
      </div>
    </div>

    <div v-if="successMessage" class="fr-alert fr-alert--success fr-mb-3w">
      <p>{{ successMessage }}</p>
    </div>

    <div v-if="errorMessage" class="fr-alert fr-alert--error fr-mb-3w">
      <p>{{ errorMessage }}</p>
    </div>

    <div v-if="isLoading" class="fr-py-4w text-center">
      <p class="fr-text--lead">Chargement des configurations ProConnect...</p>
    </div>

    <div v-else class="fr-grid-row fr-grid-row--gutters">
      <!-- 1. Catégories juridiques autorisées (Règles générales) -->
      <div class="fr-col-12 fr-mb-3w">
        <div class="fr-card fr-p-3w bo-rule-card">
          <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
            <div class="fr-col">
              <h3 class="fr-h4 fr-mb-0">
                <span
                  class="fr-icon-community-line fr-mr-1w fr-text-title-blue-france"
                  aria-hidden="true"
                ></span>
                Catégories juridiques autorisées (Règle générale)
              </h3>
            </div>
            <div class="fr-col-auto">
              <span class="fr-badge fr-badge--info">{{ categories.length }} règle(s)</span>
            </div>
          </div>
          <p class="fr-text--xs fr-text-mention-grey fr-mb-2w">
            Filtrage par préfixe de code catégorie INSEE/SIRENE (ex: 72 pour Communes, Départements,
            Régions ; 734 pour Intercommunalités).
          </p>

          <form class="bo-form-box fr-p-2w fr-mb-3w" @submit.prevent="addCategory">
            <div class="bo-form-grid">
              <!-- Ligne des labels -->
              <div class="bo-form-cell--code">
                <label class="fr-label fr-text--xs fr-mb-0-5v" for="new-cat-code">
                  Code préfixe <span class="text-danger">*</span>
                </label>
              </div>
              <div class="bo-form-cell--label">
                <label class="fr-label fr-text--xs fr-mb-0-5v" for="new-cat-label">
                  Description / Collectivités <span class="text-danger">*</span>
                </label>
              </div>
              <div class="bo-form-cell--btn"></div>

              <!-- Ligne des contrôles -->
              <div class="bo-form-cell--code">
                <input
                  id="new-cat-code"
                  v-model="newCatCode"
                  class="fr-input fr-input--sm font-mono"
                  type="text"
                  placeholder="Ex: 72, 734"
                  inputmode="numeric"
                  maxlength="6"
                  @input="onCatCodeInput"
                />
              </div>
              <div class="bo-form-cell--label">
                <input
                  id="new-cat-label"
                  v-model="newCatLabel"
                  class="fr-input fr-input--sm"
                  type="text"
                  placeholder="Ex: Communes et groupements"
                />
              </div>
              <div class="bo-form-cell--btn">
                <button
                  type="submit"
                  class="fr-btn fr-btn--secondary fr-btn--sm w-100 bo-btn-add"
                  :disabled="!canAddCategory"
                >
                  Ajouter
                </button>
              </div>

              <!-- Ligne d'aide sous les champs -->
              <div class="bo-form-cell--code">
                <span
                  v-if="catHint"
                  class="bo-input-hint"
                  :class="{ 'bo-input-hint--error': isCatFormatError || isCatDuplicate }"
                >
                  {{ catHint }}
                </span>
              </div>
              <div class="bo-form-cell--label"></div>
              <div class="bo-form-cell--btn"></div>
            </div>
          </form>

          <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
            <div class="fr-col">
              <input
                v-model="catSearch"
                type="search"
                class="fr-input fr-input--sm"
                placeholder="Rechercher par code ou description..."
              />
            </div>
          </div>

          <div class="fr-table fr-table--bordered fr-table--no-caption fr-mb-0">
            <div class="fr-table__wrapper">
              <div class="fr-table__container">
                <div class="fr-table__content">
                  <table class="w-100 table-fixed">
                    <thead>
                      <tr>
                        <th scope="col" style="width: 120px">Préfixe</th>
                        <th scope="col">Description</th>
                        <th scope="col" style="width: 80px; text-align: right">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="cat in filteredCategories"
                        :key="cat.code"
                        :class="{ 'bo-row--new': cat.isNew }"
                      >
                        <td>
                          <span class="fr-badge fr-badge--blue-cumulus font-mono">{{
                            cat.code
                          }}</span>
                          <span
                            v-if="cat.isNew"
                            class="fr-badge fr-badge--new fr-badge--sm fr-ml-1w"
                            >Nouveau</span
                          >
                        </td>
                        <td class="cell-wrap">{{ cat.nom || 'Sans description' }}</td>
                        <td class="text-right">
                          <button
                            type="button"
                            class="fr-btn fr-btn--tertiary-no-outline fr-icon-delete-line fr-btn--sm"
                            title="Supprimer cette catégorie"
                            @click="removeCategory(cat.code)"
                          ></button>
                        </td>
                      </tr>
                      <tr v-if="filteredCategories.length === 0">
                        <td colspan="3" class="text-center fr-py-3w fr-text-mention-grey">
                          {{
                            catSearch
                              ? 'Aucune catégorie correspondant à la recherche.'
                              : 'Aucune catégorie configurée.'
                          }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. SIREN autorisés (Dérogations et services nationaux) -->
      <div class="fr-col-12 fr-mb-3w">
        <div class="fr-card fr-p-3w bo-rule-card">
          <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
            <div class="fr-col">
              <h3 class="fr-h4 fr-mb-0">
                <span
                  class="fr-icon-building-line fr-mr-1w fr-text-title-blue-france"
                  aria-hidden="true"
                ></span>
                SIREN autorisés (Liste blanche & dérogations)
              </h3>
            </div>
            <div class="fr-col-auto">
              <span class="fr-badge fr-badge--info">{{ sirens.length }} actif(s)</span>
            </div>
          </div>
          <p class="fr-text--xs fr-text-mention-grey fr-mb-2w">
            Accès dérogatoire direct par identifiant SIREN à 9 chiffres (ex: Gendarmerie Nationale,
            ONF, OFB, ministères).
          </p>

          <form class="bo-form-box fr-p-2w fr-mb-3w" @submit.prevent="addSiren">
            <div class="bo-form-grid">
              <!-- Ligne des labels -->
              <div class="bo-form-cell--code">
                <label class="fr-label fr-text--xs fr-mb-0-5v" for="new-siren">
                  SIREN (9 chiffres) <span class="text-danger">*</span>
                </label>
              </div>
              <div class="bo-form-cell--label">
                <label class="fr-label fr-text--xs fr-mb-0-5v" for="new-siren-label">
                  Organisme / Motif <span class="text-danger">*</span>
                </label>
              </div>
              <div class="bo-form-cell--btn"></div>

              <!-- Ligne des contrôles -->
              <div class="bo-form-cell--code">
                <input
                  id="new-siren"
                  v-model="newSiren"
                  class="fr-input fr-input--sm font-mono"
                  type="text"
                  placeholder="Ex: 157000019"
                  maxlength="9"
                  inputmode="numeric"
                  @input="onSirenInput"
                />
              </div>
              <div class="bo-form-cell--label">
                <input
                  id="new-siren-label"
                  v-model="newSirenLabel"
                  class="fr-input fr-input--sm"
                  type="text"
                  placeholder="Ex: Gendarmerie Nationale"
                />
              </div>
              <div class="bo-form-cell--btn">
                <button
                  type="submit"
                  class="fr-btn fr-btn--secondary fr-btn--sm w-100 bo-btn-add"
                  :disabled="!canAddSiren"
                >
                  Ajouter
                </button>
              </div>

              <!-- Ligne d'aide sous les champs -->
              <div class="bo-form-cell--code">
                <span
                  v-if="sirenHint"
                  class="bo-input-hint"
                  :class="{ 'bo-input-hint--error': isSirenFormatError || isSirenDuplicate }"
                >
                  {{ sirenHint }}
                </span>
              </div>
              <div class="bo-form-cell--label"></div>
              <div class="bo-form-cell--btn"></div>
            </div>
          </form>

          <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
            <div class="fr-col">
              <input
                v-model="sirenSearch"
                type="search"
                class="fr-input fr-input--sm"
                placeholder="Rechercher un SIREN ou organisme..."
              />
            </div>
          </div>

          <div class="fr-table fr-table--bordered fr-table--no-caption fr-mb-0">
            <div class="fr-table__wrapper">
              <div class="fr-table__container">
                <div class="fr-table__content">
                  <table class="w-100">
                    <thead>
                      <tr>
                        <th scope="col" style="width: 160px">SIREN</th>
                        <th scope="col">Organisme</th>
                        <th scope="col" style="width: 80px; text-align: right">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="item in filteredSirens"
                        :key="item.siren"
                        :class="{ 'bo-row--new': item.isNew }"
                      >
                        <td class="font-mono font-weight-bold">
                          {{ formatSirenDisplay(item.siren) }}
                          <span
                            v-if="item.isNew"
                            class="fr-badge fr-badge--new fr-badge--sm fr-ml-1w"
                            >Nouveau</span
                          >
                        </td>
                        <td>{{ item.nom || 'Sans libellé' }}</td>
                        <td class="text-right">
                          <button
                            type="button"
                            class="fr-btn fr-btn--tertiary-no-outline fr-icon-delete-line fr-btn--sm"
                            title="Supprimer ce SIREN"
                            @click="removeSiren(item.siren)"
                          ></button>
                        </td>
                      </tr>
                      <tr v-if="filteredSirens.length === 0">
                        <td colspan="3" class="text-center fr-py-3w fr-text-mention-grey">
                          {{
                            sirenSearch
                              ? 'Aucun SIREN correspondant à la recherche.'
                              : 'Aucun SIREN configuré.'
                          }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Barre d'action sticky en bas d'écran lors de modifications non enregistrées -->
    <transition name="slide-up">
      <div v-if="hasUnsavedChanges" class="bo-sticky-bar">
        <div class="fr-container">
          <div class="bo-sticky-bar__inner">
            <div class="bo-sticky-bar__info">
              <span
                class="fr-icon-alert-line fr-text-default-warning fr-mr-1w"
                aria-hidden="true"
              ></span>
              <strong>{{ unsavedCount }} modification(s) non enregistrée(s)</strong>
              <span class="fr-text--xs fr-text-mention-grey fr-ml-2w bo-sticky-bar__desc">
                Pensez à sauvegarder vos modifications pour les appliquer aux connexions ProConnect.
              </span>
            </div>
            <div class="bo-sticky-bar__actions">
              <button
                type="button"
                class="fr-btn fr-btn--secondary fr-btn--sm"
                :disabled="isSaving"
                @click="resetChanges"
              >
                <span class="fr-icon-arrow-go-back-line fr-mr-1w" aria-hidden="true"></span>
                Annuler
              </button>
              <button
                type="button"
                class="fr-btn fr-btn--primary fr-btn--sm"
                :disabled="isSaving"
                @click="saveConfig"
              >
                <span
                  :class="isSaving ? 'fr-icon-refresh-line' : 'fr-icon-checkbox-circle-line'"
                  class="fr-mr-1w"
                  aria-hidden="true"
                ></span>
                {{ isSaving ? 'Enregistrement...' : 'Enregistrer les modifications' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { API_URLS, fetchResource, updateResource } from '@/services/api'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

interface SirenRule {
  siren: string
  nom: string
  isNew?: boolean
}

interface CategoryRule {
  code: string
  nom: string
  isNew?: boolean
}

const route = useRoute()
const sirens = ref<SirenRule[]>([])
const categories = ref<CategoryRule[]>([])
const initialSirens = ref<string>('[]')
const initialCategories = ref<string>('[]')

const isLoading = ref(true)
const isSaving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const newSiren = ref('')
const newSirenLabel = ref('')
const sirenSearch = ref('')

const newCatCode = ref('')
const newCatLabel = ref('')
const catSearch = ref('')

const cleanSirenInput = computed(() => newSiren.value.replace(/\D/g, ''))
const cleanCatInput = computed(() => newCatCode.value.replace(/\D/g, ''))

const isSirenFormatError = computed(() => {
  const s = cleanSirenInput.value
  return s.length > 0 && s.length < 9
})

const isSirenDuplicate = computed(() => {
  const s = cleanSirenInput.value
  return s.length === 9 && sirens.value.some((item) => item.siren === s)
})

const sirenHint = computed(() => {
  const len = cleanSirenInput.value.length
  if (len === 0) return ''
  if (isSirenDuplicate.value) return 'Ce SIREN est déjà présent dans la liste'
  if (len < 9) return `${len}/9 chiffres requis`
  return 'Format valide (9 chiffres)'
})

const canAddSiren = computed(() => {
  return (
    cleanSirenInput.value.length === 9 &&
    newSirenLabel.value.trim().length > 0 &&
    !isSirenDuplicate.value
  )
})

const isCatFormatError = computed(() => {
  return newCatCode.value.length > 0 && !/^\d+$/.test(newCatCode.value.trim())
})

const isCatDuplicate = computed(() => {
  const c = cleanCatInput.value
  return c.length > 0 && categories.value.some((item) => item.code === c)
})

const catHint = computed(() => {
  if (!newCatCode.value) return ''
  if (isCatFormatError.value) return 'Chiffres uniquement'
  if (isCatDuplicate.value) return 'Ce code est déjà présent dans la liste'
  return ''
})

const canAddCategory = computed(() => {
  return (
    cleanCatInput.value.length > 0 &&
    newCatLabel.value.trim().length > 0 &&
    !isCatFormatError.value &&
    !isCatDuplicate.value
  )
})

const formatSirenDisplay = (siren: string) => {
  const clean = (siren || '').replace(/\D/g, '')
  if (clean.length === 9) {
    return `${clean.slice(0, 3)} ${clean.slice(3, 6)} ${clean.slice(6, 9)}`
  }
  return siren
}

const onSirenInput = () => {
  newSiren.value = newSiren.value.replace(/[^\d\s]/g, '')
}

const onCatCodeInput = () => {
  newCatCode.value = newCatCode.value.replace(/\D/g, '')
}

const filteredSirens = computed(() => {
  const q = sirenSearch.value.trim().toLowerCase()
  if (!q) return sirens.value
  return sirens.value.filter(
    (s) => s.siren.toLowerCase().includes(q) || (s.nom && s.nom.toLowerCase().includes(q))
  )
})

const filteredCategories = computed(() => {
  const q = catSearch.value.trim().toLowerCase()
  if (!q) return categories.value
  return categories.value.filter(
    (c) => c.code.toLowerCase().includes(q) || (c.nom && c.nom.toLowerCase().includes(q))
  )
})

const currentSirensClean = computed(() => {
  return JSON.stringify(
    sirens.value.map((s) => ({ siren: s.siren.trim(), nom: (s.nom || '').trim() }))
  )
})

const currentCategoriesClean = computed(() => {
  return JSON.stringify(
    categories.value.map((c) => ({ code: c.code.trim(), nom: (c.nom || '').trim() }))
  )
})

const hasUnsavedChanges = computed(() => {
  return (
    currentSirensClean.value !== initialSirens.value ||
    currentCategoriesClean.value !== initialCategories.value
  )
})

const unsavedCount = computed(() => {
  let count = 0
  const origSirens: SirenRule[] = JSON.parse(initialSirens.value || '[]')
  const origCats: CategoryRule[] = JSON.parse(initialCategories.value || '[]')
  const sirenDiff = Math.abs(sirens.value.length - origSirens.length)
  const catDiff = Math.abs(categories.value.length - origCats.length)
  count += sirenDiff + catDiff
  return count > 0 ? count : 1
})

const fetchConfig = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const data = await fetchResource(API_URLS.backofficeProConnectConfig)
    if (data) {
      const serverSirens = (data.sirens_autorises || []).map((s: any) => ({
        siren: String(s.siren || s).trim(),
        nom: String(s.nom || '').trim(),
      }))
      const serverCats = (data.categories_juridiques_autorisees || []).map((c: any) => ({
        code: String(c.code || c).trim(),
        nom: String(c.nom || '').trim(),
      }))
      sirens.value = serverSirens
      categories.value = serverCats
      initialSirens.value = JSON.stringify(serverSirens)
      initialCategories.value = JSON.stringify(serverCats)
    }
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement de la configuration ProConnect.'
  } finally {
    isLoading.value = false
  }
}

const addSiren = () => {
  const clean = cleanSirenInput.value
  if (!canAddSiren.value) return
  if (sirens.value.some((s) => s.siren === clean)) {
    errorMessage.value = `Le SIREN ${clean} est déjà présent dans la liste.`
    return
  }
  sirens.value.unshift({
    siren: clean,
    nom: newSirenLabel.value.trim(),
    isNew: true,
  })
  newSiren.value = ''
  newSirenLabel.value = ''
  errorMessage.value = ''
}

const removeSiren = (sirenToRemove: string) => {
  sirens.value = sirens.value.filter((s) => s.siren !== sirenToRemove)
}

const addCategory = () => {
  const clean = cleanCatInput.value
  if (!canAddCategory.value) return
  if (categories.value.some((c) => c.code === clean)) {
    errorMessage.value = `Le code catégorie ${clean} est déjà présent dans la liste.`
    return
  }
  categories.value.unshift({
    code: clean,
    nom: newCatLabel.value.trim(),
    isNew: true,
  })
  newCatCode.value = ''
  newCatLabel.value = ''
  errorMessage.value = ''
}

const removeCategory = (codeToRemove: string) => {
  categories.value = categories.value.filter((c) => c.code !== codeToRemove)
}

const resetChanges = () => {
  sirens.value = JSON.parse(initialSirens.value)
  categories.value = JSON.parse(initialCategories.value)
  errorMessage.value = ''
}

const formatApiErrors = (error: any): string => {
  if (typeof error === 'string') return error
  if (Array.isArray(error)) return error.map(formatApiErrors).filter(Boolean).join(', ')
  if (typeof error === 'object' && error !== null) {
    return Object.entries(error)
      .map(([k, v]) => {
        const keyLabel =
          k === 'sirens_autorises'
            ? 'SIREN'
            : k === 'categories_juridiques_autorisees'
              ? 'Catégories'
              : k
        const valText = formatApiErrors(v)
        return valText ? `${keyLabel} : ${valText}` : ''
      })
      .filter(Boolean)
      .join(' | ')
  }
  return String(error)
}

const saveConfig = async () => {
  isSaving.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const payload = {
      categories_juridiques_autorisees: categories.value.map((c) => ({
        code: c.code,
        nom: c.nom,
      })),
      sirens_autorises: sirens.value.map((s) => ({
        siren: s.siren,
        nom: s.nom,
      })),
    }
    const response = await updateResource(API_URLS.backofficeProConnectConfig, payload)
    if (response) {
      sirens.value.forEach((s) => (s.isNew = false))
      categories.value.forEach((c) => (c.isNew = false))
      initialSirens.value = currentSirensClean.value
      initialCategories.value = currentCategoriesClean.value
      successMessage.value = 'Règles d’accès ProConnect enregistrées avec succès.'
      setTimeout(() => {
        successMessage.value = ''
      }, 4000)
    }
  } catch (error: any) {
    const formatted = formatApiErrors(error)
    errorMessage.value = formatted
      ? `Erreur de validation : ${formatted}`
      : 'Erreur lors de la sauvegarde de la configuration.'
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  fetchConfig()
  const sirenQuery = route.query.siren
  if (typeof sirenQuery === 'string' && /^\d{9}$/.test(sirenQuery.trim())) {
    newSiren.value = sirenQuery.trim()
  }
})
</script>

<style scoped>
.proconnect-config-panel {
  padding-bottom: 5rem;
}
.bo-header-row {
  border-bottom: 1px solid var(--border-default-grey);
  padding-bottom: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.bo-header-row__title {
  flex: 1 1 320px;
}
.bo-header-row__actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.bo-rule-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.bo-form-box {
  background-color: var(--background-alt-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 6px;
}
.bo-form-grid {
  display: grid;
  grid-template-columns: 180px 1fr 120px;
  column-gap: 1rem;
  row-gap: 0.25rem;
  align-items: center;
}
.bo-form-cell--code {
  width: 100%;
}
.bo-form-cell--label {
  width: 100%;
}
.bo-form-cell--btn {
  width: 100%;
}
.bo-btn-add {
  height: 2.5rem;
  min-height: 2.5rem;
  padding: 0 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin: 0 !important;
}
.bo-input-hint {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  margin-top: 0.25rem;
  min-height: 1.1rem;
  display: block;
}
.bo-input-hint--error {
  color: var(--text-default-error);
}
.text-danger {
  color: var(--text-default-error);
}
.font-mono {
  font-family: monospace;
}
.font-weight-bold {
  font-weight: 700;
}
.w-100 {
  width: 100%;
}
.text-right {
  text-align: right;
}
.text-center {
  text-align: center;
}
.table-fixed {
  table-layout: fixed;
}
.cell-wrap {
  white-space: normal !important;
  word-break: break-word;
  line-height: 1.4;
}
.bo-row--new {
  background-color: #f0fdf4 !important;
}
.bo-sticky-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--background-default-grey);
  border-top: 2px solid var(--border-active-blue-france);
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.12);
  padding: 0.85rem 1rem;
  z-index: 1000;
}
.bo-sticky-bar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.bo-sticky-bar__info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.bo-sticky-bar__actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
@media (max-width: 768px) {
  .bo-form-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  .bo-sticky-bar__desc {
    display: none;
  }
}
.slide-up-enter-active,
.slide-up-leave-active {
  transition:
    transform 0.25s ease-out,
    opacity 0.25s ease-out;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
