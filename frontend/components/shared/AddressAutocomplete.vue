<template>
  <div class="fr-input-group address-autocomplete" :class="{ 'fr-input-group--error': errorMessage }">
    <label class="fr-label" :for="id">{{ label }}</label>
    <p v-if="hint" class="fr-hint-text">{{ hint }}</p>
    <div class="input-wrapper">
      <input
        :id="id"
        class="fr-input"
        :class="{ 'fr-input--error': errorMessage }"
        type="text"
        v-model="query"
        @input="onInput"
        @keydown.down.prevent="onArrowDown"
        @keydown.up.prevent="onArrowUp"
        @keydown.enter.prevent="onEnter"
        placeholder="Rechercher une adresse..."
        autocomplete="off"
      />
      <ul v-if="suggestions.length > 0" class="suggestions-list">
        <li
          v-for="(suggestion, index) in suggestions"
          :key="suggestion.properties.id"
          :class="{ 'is-selected': index === selectedIndex }"
          @click="selectSuggestion(suggestion)"
        >
          {{ suggestion.properties.label }}
        </li>
      </ul>
    </div>
    <p v-if="errorMessage" class="fr-error-text">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  id: string
  label: string
  modelValue: string
  errorMessage?: string
  hint?: string
}>()

const emit = defineEmits(['update:modelValue', 'select'])

const query = ref(props.modelValue)
const suggestions = ref<any[]>([])
const selectedIndex = ref(-1)

const onInput = async () => {
  if (query.value.length < 3) {
    suggestions.value = []
    return
  }

  try {
    const response = await fetch(`https://api-adresse.data.gouv.fr/search/?q=${encodeURIComponent(query.value)}&limit=5`)
    const data = await response.json()
    suggestions.value = data.features
    selectedIndex.value = -1
  } catch (error) {
    console.error('Error fetching addresses:', error)
  }
}

const selectSuggestion = (suggestion: any) => {
  const label = suggestion.properties.label
  const city = suggestion.properties.city
  query.value = label
  suggestions.value = []
  emit('update:modelValue', label)
  emit('select', { label, city, full: suggestion })
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
</script>

<style scoped>
.input-wrapper {
  position: relative;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background: white;
  border: 1px solid #ddd;
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.suggestions-list li {
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid var(--border-default-grey);
}

.suggestions-list li:last-child {
  border-bottom: none;
}

.suggestions-list li:hover,
.suggestions-list li.is-selected {
  background-color: var(--background-alt-blue-france);
}
</style>
