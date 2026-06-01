<template>
  <div
    class="fr-input-group company-autocomplete"
    :class="{ 'fr-input-group--error': errorMessage }"
  >
    <label class="fr-label" :for="id">
      {{ label }}
      <span v-if="required" class="fr-req"> *</span>
    </label>
    <p v-if="hint" class="fr-hint-text">{{ hint }}</p>
    <div class="input-wrapper">
      <input
        :id="id"
        class="fr-input"
        :class="{ 'fr-input--error': errorMessage, 'has-loading': isLoading }"
        type="text"
        v-model="query"
        @input="onInput"
        @keydown.down.prevent="onArrowDown"
        @keydown.up.prevent="onArrowUp"
        @keydown.enter.prevent="onEnter"
        @keydown.esc="onEsc"
        placeholder="Rechercher par nom, SIRET ou SIREN..."
        autocomplete="off"
        :required="required"
      />
      <div v-if="isLoading" class="spinner-loader"></div>
      <ul v-if="suggestions.length > 0" class="suggestions-list" role="listbox">
        <li
          v-for="(suggestion, index) in suggestions"
          :key="suggestion.siren"
          :class="{ 'is-selected': index === selectedIndex }"
          @click="selectSuggestion(suggestion)"
          role="option"
        >
          <div class="company-suggestion-header">
            <span class="company-name">{{ suggestion.nom_complet }}</span>
            <span v-if="suggestion.siege && suggestion.siege.siret" class="company-badge-siret">
              SIRET : {{ formatSiret(suggestion.siege.siret) }}
            </span>
          </div>
          <div v-if="suggestion.siege && suggestion.siege.adresse" class="company-address">
            {{ suggestion.siege.adresse }}
          </div>
        </li>
      </ul>
      <div
        v-if="hasSearched && suggestions.length === 0 && !isLoading && query.trim().length >= 3"
        class="no-results"
      >
        Aucune entreprise trouvée
      </div>
    </div>
    <p v-if="errorMessage" class="fr-error-text">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  id: string
  label: string
  modelValue: string
  errorMessage?: string
  hint?: string
  required?: boolean
}>()

const emit = defineEmits(['update:modelValue', 'select'])

const query = ref(props.modelValue)
const suggestions = ref<any[]>([])
const selectedIndex = ref(-1)
const isLoading = ref(false)
const hasSearched = ref(false)

watch(
  () => props.modelValue,
  (newVal) => {
    query.value = newVal
  }
)

let debounceTimer: any = null

const onInput = () => {
  hasSearched.value = false
  if (debounceTimer) clearTimeout(debounceTimer)

  const trimmedQuery = query.value.trim()
  if (trimmedQuery.length < 3) {
    suggestions.value = []
    return
  }

  debounceTimer = setTimeout(async () => {
    isLoading.value = true
    try {
      const response = await fetch(
        `https://recherche-entreprises.api.gouv.fr/search?q=${encodeURIComponent(trimmedQuery)}&limit=5`
      )
      if (!response.ok) {
        suggestions.value = []
        return
      }
      const data = await response.json()
      suggestions.value = data.results || []
      selectedIndex.value = -1
      hasSearched.value = true
    } catch (error) {
      console.error('Error fetching companies:', error)
      suggestions.value = []
    } finally {
      isLoading.value = false
    }
  }, 300)
}

const selectSuggestion = (suggestion: any) => {
  const name = suggestion.nom_complet
  const siret = suggestion.siege?.siret || ''
  const address = suggestion.siege?.adresse || ''
  query.value = name
  suggestions.value = []
  hasSearched.value = false
  emit('update:modelValue', name)
  emit('select', { name, siret, address, full: suggestion })
}

const onArrowDown = () => {
  if (selectedIndex.value < suggestions.value.length - 1) {
    selectedIndex.value++
  }
}

const onArrowUp = () => {
  if (selectedIndex.value > 0) {
    selectedIndex.value--
  }
}

const onEnter = () => {
  if (selectedIndex.value >= 0) {
    selectSuggestion(suggestions.value[selectedIndex.value])
  }
}

const onEsc = () => {
  suggestions.value = []
}

const formatSiret = (siret: string) => {
  if (!siret) return ''
  return siret.replace(/(\d{3})(\d{3})(\d{3})(\d{5})/, '$1 $2 $3 $4')
}
</script>

<style scoped>
.input-wrapper {
  position: relative;
}

.has-loading {
  padding-right: 2.5rem;
}

.spinner-loader {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid var(--border-default-grey);
  border-top-color: var(--background-active-blue-france);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  pointer-events: none;
}

@keyframes spin {
  to {
    transform: translateY(-50%) rotate(360deg);
  }
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background: white;
  border: 1px solid var(--border-default-grey);
  border-top: none;
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

.suggestions-list li {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--border-default-grey);
  transition:
    background-color 0.2s ease,
    border-left-color 0.2s ease;
  border-left: 3px solid transparent;
}

.suggestions-list li:last-child {
  border-bottom: none;
}

.suggestions-list li:hover,
.suggestions-list li.is-selected {
  background-color: var(--background-alt-blue-france);
  border-left-color: var(--background-active-blue-france);
}

.company-suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.25rem;
}

.company-name {
  font-weight: bold;
  color: var(--text-title-grey);
  font-size: 0.95rem;
}

.company-badge-siret {
  font-size: 0.75rem;
  background-color: var(--background-contrast-info);
  color: var(--text-label-info-text);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
  white-space: nowrap;
}

.company-address {
  font-size: 0.8rem;
  color: var(--text-mention-grey);
}

.no-results {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background: white;
  border: 1px solid var(--border-default-grey);
  border-top: none;
  width: 100%;
  padding: 0.75rem 1rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  font-style: italic;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}
</style>
