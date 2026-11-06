<template>
  <div
    class="fr-tabs__panel fr-tabs__panel--selected chatbot-config-panel"
    role="tabpanel"
    tabindex="0"
  >
    <div class="bo-header-row fr-mb-3w">
      <div class="bo-header-row__title">
        <h2 class="fr-h3 fr-mb-0-5v">
          <span
            class="fr-icon-chat-3-line fr-text-title-blue-france fr-mr-1w"
            aria-hidden="true"
          ></span>
          Configuration de l’Assistant IA (Chatbot)
        </h2>
        <p class="fr-text--sm fr-text-mention-grey fr-mb-0">
          Personnalisez le fournisseur LLM, le modèle, la clé d'API et le prompt système officiel
          sans avoir à redémarrer les conteneurs ou modifier les fichiers d’environnement.
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
          Annuler
        </button>
        <button
          type="button"
          class="fr-btn fr-btn--primary fr-btn--sm"
          :class="{ 'fr-btn--secondary': !hasUnsavedChanges }"
          :disabled="isSaving || isLoading || !hasUnsavedChanges"
          @click="saveConfig"
        >
          <span
            :class="isSaving ? 'fr-icon-refresh-line' : 'fr-icon-checkbox-circle-line'"
            class="fr-mr-1w"
            aria-hidden="true"
          ></span>
          {{ isSaving ? 'Enregistrement...' : hasUnsavedChanges ? 'Enregistrer les modifications' : 'À jour' }}
        </button>
      </div>
    </div>

    <!-- Alertes Feedback -->
    <div v-if="successMessage" class="fr-alert fr-alert--success fr-mb-3w">
      <p>{{ successMessage }}</p>
    </div>

    <div v-if="errorMessage" class="fr-alert fr-alert--error fr-mb-3w">
      <p>{{ errorMessage }}</p>
    </div>

    <div v-if="isLoading" class="fr-py-4w text-center">
      <p class="fr-text--lead">Chargement de la configuration du Chatbot...</p>
    </div>

    <div v-else class="fr-grid-row fr-grid-row--gutters">
      <!-- Section 1 : Paramètres du Modèle & API -->
      <div class="fr-col-12 fr-col-lg-5 fr-mb-3w">
        <div class="fr-card fr-p-3w bo-rule-card h-100">
          <h3 class="fr-h4 fr-mb-2w">
            <span class="fr-icon-settings-5-line fr-mr-1w fr-text-title-blue-france" aria-hidden="true"></span>
            Moteur d’inférence LLM
          </h3>

          <!-- Fournisseur -->
          <div class="fr-select-group fr-mb-2w">
            <label class="fr-label" for="chatbot-provider">
              Fournisseur d'IA
              <span class="fr-hint-text">Plateforme hébergeant l'API du modèle</span>
            </label>
            <select
              id="chatbot-provider"
              v-model="form.provider"
              class="fr-select"
              @change="onProviderChange"
            >
              <option value="mock">Mock (Simulateur local - sans coût d'API)</option>
              <option value="openrouter">OpenRouter (DeepSeek, Llama, Claude, etc.)</option>
              <option value="mistral">Mistral AI (Plateforme officielle)</option>
              <option value="albert">Albert API (Étalab / DINUM - Souverain)</option>
              <option value="custom">Compatible OpenAI personnalisé</option>
            </select>
          </div>

          <!-- Modèle -->
          <div class="fr-input-group fr-mb-2w" v-if="form.provider !== 'mock'">
            <label class="fr-label" for="chatbot-model">
              Modèle
              <span class="fr-hint-text">Nom technique du modèle (ex: deepseek/deepseek-v4-flash-latest)</span>
            </label>
            <input
              id="chatbot-model"
              v-model="form.model"
              type="text"
              class="fr-input"
              :placeholder="suggestedModelPlaceholder"
            />
          </div>

          <!-- URL de Base API -->
          <div class="fr-input-group fr-mb-2w" v-if="form.provider !== 'mock'">
            <label class="fr-label" for="chatbot-base-url">
              URL de base (Base URL)
              <span class="fr-hint-text">URL du point d'entrée de l'API OpenAI-compatible</span>
            </label>
            <input
              id="chatbot-base-url"
              v-model="form.base_url"
              type="text"
              class="fr-input"
              :placeholder="suggestedBaseUrlPlaceholder"
            />
            <!-- Hints d'URL fréquentes cliquables -->
            <div class="fr-mt-1w">
              <span class="fr-text--xs fr-text-mention-grey fr-mr-1w">Exemples fréquents :</span>
              <div class="d-flex flex-wrap" style="gap: 0.35rem; margin-top: 0.25rem;">
                <button
                  type="button"
                  class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon cursor-pointer"
                  title="Appliquer l'URL OpenRouter"
                  @click="setBaseUrl('https://openrouter.ai/api/v1')"
                >
                  OpenRouter
                </button>
                <button
                  type="button"
                  class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon cursor-pointer"
                  title="Appliquer l'URL Albert (DINUM)"
                  @click="setBaseUrl('https://albert.api.etalab.gouv.fr/v1')"
                >
                  Albert (DINUM)
                </button>
                <button
                  type="button"
                  class="fr-badge fr-badge--sm fr-badge--info fr-badge--no-icon cursor-pointer"
                  title="Appliquer l'URL Mistral AI"
                  @click="setBaseUrl('https://api.mistral.ai/v1')"
                >
                  Mistral AI
                </button>
              </div>
            </div>
          </div>

          <!-- Clé d'API -->
          <div class="fr-input-group fr-mb-2w" v-if="form.provider !== 'mock'">
            <label class="fr-label" for="chatbot-api-key">
              Clé d'API
              <span class="fr-hint-text">
                <template v-if="initialConfig?.has_api_key">
                  Une clé est active (<strong>{{ initialConfig.api_key_masked }}</strong>). Renseignez ce champ uniquement pour la remplacer.
                </template>
                <template v-else>
                  Aucune clé enregistrée en base.
                </template>
              </span>
            </label>
            <div class="d-flex" style="gap: 0.5rem">
              <input
                id="chatbot-api-key"
                v-model="form.api_key"
                :type="showApiKey ? 'text' : 'password'"
                class="fr-input"
                placeholder="Nouvelle clé d'API (laisser vide pour ne pas modifier)"
                autocomplete="off"
              />
              <button
                type="button"
                class="fr-btn fr-btn--secondary fr-btn--sm"
                :title="showApiKey ? 'Masquer la clé' : 'Afficher la clé'"
                @click="showApiKey = !showApiKey"
              >
                <span :class="showApiKey ? 'fr-icon-eye-off-line' : 'fr-icon-eye-line'" aria-hidden="true"></span>
              </button>
            </div>
            <div v-if="initialConfig?.has_api_key" class="fr-mt-1w">
              <button
                type="button"
                class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-text--xs text-danger"
                style="padding: 0"
                @click="triggerClearApiKey"
              >
                <span class="fr-icon-delete-line fr-mr-0-5v" aria-hidden="true"></span>
                Effacer la clé d'API enregistrée
              </button>
            </div>
          </div>

          <!-- Timeout -->
          <div class="fr-input-group fr-mb-2w" v-if="form.provider !== 'mock'">
            <label class="fr-label" for="chatbot-timeout">
              Timeout (secondes)
              <span class="fr-hint-text">Délai d'attente maximum d'une réponse de l'API LLM (défaut : 40s)</span>
            </label>
            <input
              id="chatbot-timeout"
              v-model.number="form.timeout"
              type="number"
              min="5"
              max="300"
              class="fr-input"
            />
          </div>

          <!-- Bouton Test de Connexion API -->
          <div class="fr-mt-3w" v-if="form.provider !== 'mock'">
            <button
              type="button"
              class="fr-btn fr-btn--secondary fr-btn--sm w-100 justify-content-center"
              :disabled="isTestingConnection || isSaving"
              @click="handleTestConnection"
            >
              <span
                :class="isTestingConnection ? 'fr-icon-refresh-line' : 'fr-icon-checkbox-circle-line'"
                class="fr-mr-1w"
                aria-hidden="true"
              ></span>
              {{ isTestingConnection ? 'Test de connexion en cours...' : 'Tester la connexion à l’API' }}
            </button>
          </div>

          <!-- Feedback du test de connexion -->
          <div v-if="testResult" class="fr-mt-2w">
            <div
              v-if="testResult.success"
              class="fr-alert fr-alert--success fr-alert--sm"
            >
              <p class="fr-text--xs fr-mb-0">
                <strong>Connexion réussie !</strong> {{ testResult.message }}
              </p>
              <p v-if="testResult.sample_reply" class="fr-text--xs fr-mt-1v fr-mb-0 fr-text-mention-grey">
                Réponse du modèle : <em>"{{ testResult.sample_reply }}"</em>
              </p>
            </div>
            <div
              v-else
              class="fr-alert fr-alert--error fr-alert--sm"
            >
              <p class="fr-text--xs fr-mb-0">
                <strong>Échec du test :</strong> {{ testResult.error }}
              </p>
            </div>
          </div>

          <!-- Note sur le Mock -->
          <div v-if="form.provider === 'mock'" class="fr-alert fr-alert--info fr-alert--sm fr-mt-2w">
            <p>
              En mode <strong>Mock</strong>, les réponses sont simulées localement en streaming avec génération de propositions de constatation réalistes, sans consommer de crédit d'API externe.
            </p>
          </div>
        </div>
      </div>

      <!-- Section 2 : Prompt Système -->
      <div class="fr-col-12 fr-col-lg-7 fr-mb-3w">
        <div class="fr-card fr-p-3w bo-rule-card h-100 d-flex flex-column">
          <div class="d-flex justify-content-between align-items-center fr-mb-2w">
            <h3 class="fr-h4 fr-mb-0">
              <span class="fr-icon-quote-line fr-mr-1w fr-text-title-blue-france" aria-hidden="true"></span>
              Prompt Système
            </h3>
            <button
              type="button"
              class="fr-btn fr-btn--secondary fr-btn--sm"
              @click="restoreDefaultPrompt"
            >
              <span class="fr-icon-refresh-line fr-mr-1w" aria-hidden="true"></span>
              Restaurer prompt initial
            </button>
          </div>

          <p class="fr-text--sm fr-text-mention-grey fr-mb-2w">
            Consignes directes transmises au LLM à chaque message. Définit le périmètre juridique (Code de l'environnement, Zero-PII, directives opérationnelles maires/agents).
          </p>

          <div class="fr-input-group flex-grow-1 d-flex flex-column fr-mb-0">
            <label class="fr-label sr-only" for="chatbot-system-prompt">Prompt Système</label>
            <textarea
              id="chatbot-system-prompt"
              v-model="form.system_prompt"
              class="fr-input prompt-textarea"
              rows="22"
              placeholder="Contenu du prompt système..."
            ></textarea>
          </div>

          <div class="fr-mt-2w d-flex justify-content-between align-items-center">
            <span class="fr-text--xs fr-text-mention-grey">
              {{ (form.system_prompt || '').length }} caractères
            </span>
            <span class="fr-badge fr-badge--sm fr-badge--info">
              RAG & Contexte de session injectés automatiquement
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  getChatbotConfig,
  updateChatbotConfig,
  testChatbotConnection,
  type ChatbotConfigData,
  type ChatbotTestConnectionResponse,
} from '@/services/api'

const isLoading = ref(true)
const isSaving = ref(false)
const isTestingConnection = ref(false)
const showApiKey = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const clearApiKeyFlag = ref(false)
const testResult = ref<ChatbotTestConnectionResponse | null>(null)

const initialConfig = ref<ChatbotConfigData | null>(null)

const form = reactive({
  provider: 'mock',
  model: '',
  base_url: '',
  api_key: '',
  timeout: 40,
  system_prompt: '',
})

const suggestedModelPlaceholder = computed(() => {
  switch (form.provider) {
    case 'openrouter':
      return 'ex: deepseek/deepseek-v4-flash-latest ou anthropic/claude-3.5-sonnet'
    case 'mistral':
      return 'ex: mistral-large-latest ou mistral-small-latest'
    case 'albert':
      return 'ex: mistral-small-3-2-24b-instruct-2506'
    default:
      return 'Nom du modèle'
  }
})

const suggestedBaseUrlPlaceholder = computed(() => {
  switch (form.provider) {
    case 'openrouter':
      return 'https://openrouter.ai/api/v1 (défaut)'
    case 'mistral':
      return 'https://api.mistral.ai/v1 (défaut)'
    case 'albert':
      return 'https://albert.api.etalab.gouv.fr/v1 (défaut)'
    default:
      return 'https://...'
  }
})

const hasUnsavedChanges = computed(() => {
  if (!initialConfig.value) return false
  return (
    form.provider !== initialConfig.value.provider ||
    form.model !== initialConfig.value.model ||
    form.base_url !== (initialConfig.value.base_url || '') ||
    form.timeout !== initialConfig.value.timeout ||
    form.system_prompt !== initialConfig.value.system_prompt ||
    Boolean(form.api_key.trim()) ||
    clearApiKeyFlag.value
  )
})

const setBaseUrl = (url: string) => {
  form.base_url = url
}

const onProviderChange = () => {
  testResult.value = null
  if (form.provider === 'openrouter') {
    if (!form.model) form.model = 'deepseek/deepseek-v4-flash-latest'
    if (!form.base_url) form.base_url = 'https://openrouter.ai/api/v1'
  } else if (form.provider === 'mistral') {
    if (!form.model) form.model = 'mistral-large-latest'
    if (!form.base_url) form.base_url = 'https://api.mistral.ai/v1'
  } else if (form.provider === 'albert') {
    if (!form.model) form.model = 'mistral-small-3-2-24b-instruct-2506'
    if (!form.base_url) form.base_url = 'https://albert.api.etalab.gouv.fr/v1'
  }
}

const handleTestConnection = async () => {
  isTestingConnection.value = true
  testResult.value = null
  errorMessage.value = ''

  try {
    const payload: Partial<ChatbotConfigData> = {
      provider: form.provider,
      model: form.model.trim(),
      base_url: form.base_url.trim(),
      timeout: form.timeout,
    }
    if (form.api_key.trim()) {
      payload.api_key = form.api_key.trim()
    }

    const res = await testChatbotConnection(payload)
    testResult.value = res
  } catch (err: any) {
    testResult.value = {
      success: false,
      error: err?.message || 'Erreur lors du test de connexion.',
    }
  } finally {
    isTestingConnection.value = false
  }
}

const restoreDefaultPrompt = () => {
  if (initialConfig.value?.default_system_prompt) {
    form.system_prompt = initialConfig.value.default_system_prompt
  }
}

const triggerClearApiKey = () => {
  if (confirm('Voulez-vous vraiment effacer la clé d’API configurée en base ?')) {
    form.api_key = ''
    clearApiKeyFlag.value = true
  }
}

const loadConfig = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const data = await getChatbotConfig()
    initialConfig.value = data
    form.provider = data.provider || 'mock'
    form.model = data.model || ''
    form.base_url = data.base_url || ''
    form.api_key = ''
    form.timeout = data.timeout || 40
    form.system_prompt = data.system_prompt || data.default_system_prompt || ''
    clearApiKeyFlag.value = false
  } catch (err: any) {
    errorMessage.value =
      err?.message || 'Erreur lors du chargement de la configuration du Chatbot.'
  } finally {
    isLoading.value = false
  }
}

const resetChanges = () => {
  if (!initialConfig.value) return
  form.provider = initialConfig.value.provider || 'mock'
  form.model = initialConfig.value.model || ''
  form.base_url = initialConfig.value.base_url || ''
  form.api_key = ''
  form.timeout = initialConfig.value.timeout || 40
  form.system_prompt = initialConfig.value.system_prompt || ''
  clearApiKeyFlag.value = false
  successMessage.value = ''
  errorMessage.value = ''
}

const saveConfig = async () => {
  isSaving.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const payload: Partial<ChatbotConfigData> & { clear_api_key?: boolean } = {
      provider: form.provider,
      model: form.model.trim(),
      base_url: form.base_url.trim(),
      timeout: form.timeout,
      system_prompt: form.system_prompt,
    }

    if (clearApiKeyFlag.value) {
      payload.clear_api_key = true
    } else if (form.api_key.trim()) {
      payload.api_key = form.api_key.trim()
    }

    const updated = await updateChatbotConfig(payload)
    initialConfig.value = updated
    form.api_key = ''
    clearApiKeyFlag.value = false
    successMessage.value = 'La configuration du Chatbot a été enregistrée avec succès.'
  } catch (err: any) {
    errorMessage.value =
      err?.message || 'Erreur lors de la sauvegarde de la configuration.'
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.prompt-textarea {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.85rem;
  line-height: 1.5;
  resize: vertical;
}

.bo-rule-card {
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 4px;
}

.bo-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.bo-header-row__actions {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

.d-flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}

.flex-grow-1 {
  flex-grow: 1;
}

.justify-content-between {
  justify-content: space-between;
}

.align-items-center {
  align-items: center;
}

.h-100 {
  height: 100%;
}

.text-danger {
  color: var(--text-default-error);
}

.w-100 {
  width: 100%;
}

.justify-content-center {
  justify-content: center;
}
</style>
