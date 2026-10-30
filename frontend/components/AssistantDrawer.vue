<template>
  <div v-if="isOpen" class="assistant-drawer-overlay" @click.self="closeDrawer">
    <aside
      class="assistant-drawer"
      role="dialog"
      aria-modal="true"
      aria-labelledby="assistant-drawer-title"
    >
      <!-- Header du Drawer -->
      <header class="assistant-header fr-p-3w">
        <div class="assistant-header-content">
          <div class="assistant-title-group">
            <div class="assistant-avatar fr-mr-2w">
              <span class="fr-icon-question-answer-line fr-icon--md text-primary" aria-hidden="true"></span>
            </div>
            <div>
              <div class="assistant-badge-pill fr-mb-1v">Assistant IA</div>
              <h2 id="assistant-drawer-title" class="fr-h6 fr-mb-0 assistant-main-title">
                Stop Dépot Sauvage
              </h2>
              <p class="fr-text--xs fr-text-mention--grey fr-mb-0">
                Aide juridique, procédure &amp; constatation
              </p>
            </div>
          </div>
          <button
            class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-icon-close-line close-btn-round"
            title="Fermer le volet d'assistance"
            aria-label="Fermer"
            @click="closeDrawer"
          ></button>
        </div>
      </header>

      <!-- Zone des messages -->
      <section class="assistant-body fr-p-3w" ref="chatBodyRef">
        <!-- Message de bienvenue initial si aucun message -->
        <div v-if="messages.length === 0" class="welcome-box premium-box fr-p-3w fr-mb-2w">
          <div class="welcome-badge fr-text--xs fr-mb-1w">
            <span class="fr-icon-sparkling-fill fr-icon--xs fr-mr-1v"></span>
            Conseils personnalisés
          </div>
          <p class="fr-text--sm fr-mb-2w welcome-text">
            Bonjour ! Je suis à vos côtés pour vous assister dans l'application de la réglementation (Code de l'environnement, pouvoirs de police du maire) ou préparer votre procès-verbal de constatation.
          </p>
          <div class="quick-prompts-container">
            <p class="fr-text--xs fr-text-mention--grey fr-mb-1w quick-prompts-label">Suggestions rapides :</p>
            <div class="quick-prompts">
              <button
                v-for="(prompt, idx) in quickPrompts"
                :key="idx"
                class="premium-prompt-pill"
                @click="sendQuickPrompt(prompt)"
              >
                <span class="fr-icon-arrow-right-s-line fr-icon--xs fr-mr-1v" aria-hidden="true"></span>
                <span>{{ prompt }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Liste des messages -->
        <div
          v-for="message in messages"
          :key="message.id"
          class="chat-bubble-row"
          :class="{ 'user-row': message.role === 'user', 'assistant-row': message.role === 'assistant' }"
        >
          <div class="chat-bubble" :class="{ 'user-bubble': message.role === 'user', 'assistant-bubble': message.role === 'assistant' }">
            <div class="bubble-sender fr-text--xs fr-mb-1v">
              {{ message.role === 'user' ? 'Vous' : 'Stop Dépot Sauvage' }}
            </div>

            <!-- Contenu texte pour utilisateur (texte direct) ou assistant (Markdown assaini) -->
            <div
              v-if="message.role === 'user' && getMessageText(message)"
              class="user-message-content fr-text--sm"
            >
              {{ getMessageText(message) }}
            </div>
            <div
              v-else-if="getMessageText(message)"
              class="message-rendered-markdown fr-text--sm"
              v-html="renderMarkdown(getMessageText(message))"
            ></div>

            <!-- Tool Calls : Generative UI (ex: Brouillon de constatation) -->
            <template v-if="getToolCalls(message).length > 0">
              <div
                v-for="toolCall in getToolCalls(message)"
                :key="toolCall.toolCallId || toolCall.id"
                class="tool-call-container fr-mt-2w"
              >
                <!-- Carte spécifique à propose_constatation_draft -->
                <div v-if="toolCall.toolName === 'propose_constatation_draft'" class="draft-card premium-draft-card fr-p-3w">
                  <div class="draft-card-header fr-mb-2w">
                    <div class="draft-card-icon-wrap fr-mr-1w">
                      <span class="fr-icon-file-text-line fr-icon--sm text-primary"></span>
                    </div>
                    <div>
                      <strong class="fr-text--sm d-block draft-card-title">Brouillon de constatation préparé</strong>
                      <span class="fr-text--xs fr-text-mention--grey">Prêt à être finalisé sur le site</span>
                    </div>
                  </div>
                  <ul class="draft-recap-list fr-text--xs fr-mb-2w">
                    <li v-if="toolCall.input?.commune">
                      <span class="recap-label">Commune :</span> <span class="recap-value">{{ toolCall.input.commune }}</span>
                    </li>
                    <li v-if="toolCall.input?.typesDepot?.length">
                      <span class="recap-label">Déchets :</span> <span class="recap-value">{{ toolCall.input.typesDepot.join(', ') }}</span>
                    </li>
                    <li v-if="toolCall.input?.volumeDepot">
                      <span class="recap-label">Volume estimé :</span> <span class="recap-value">{{ toolCall.input.volumeDepot }}</span>
                    </li>
                    <li v-if="toolCall.input?.localisationDepot">
                      <span class="recap-label">Lieu :</span> <span class="recap-value">{{ toolCall.input.localisationDepot }}</span>
                    </li>
                  </ul>
                  <button
                    class="fr-btn fr-btn--sm fr-btn--icon-left fr-icon-checkbox-circle-line w-100 justify-center premium-draft-action-btn"
                    @click="applyDraftAndRedirect(toolCall.input)"
                  >
                    Créer mon brouillon de constatation
                  </button>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Indicateur de streaming / chargement -->
        <div v-if="status === 'streaming' || status === 'submitted'" class="loading-bubble-row">
          <div class="chat-bubble assistant-bubble loading-bubble">
            <span class="typing-indicator fr-mr-1w">
              <span></span><span></span><span></span>
            </span>
            <span class="fr-text--xs fr-text-mention--grey">L'assistant rédige sa réponse...</span>
          </div>
        </div>

        <!-- Erreur éventuelle -->
        <div v-if="error" class="fr-alert fr-alert--error fr-alert--sm fr-mt-2w">
          <p class="fr-text--xs">Une erreur est survenue lors de l'échange. Veuillez réessayer.</p>
        </div>
      </section>

      <!-- Footer : Formulaire de saisie Premium -->
      <footer class="assistant-footer fr-p-3w">
        <form @submit.prevent="handleSubmitMessage" class="chat-form">
          <div class="input-container premium-input-wrapper">
            <textarea
              v-model="inputMessage"
              class="fr-input chat-textarea premium-textarea"
              placeholder="Posez votre question ou décrivez le dépôt..."
              rows="2"
              @keydown="handleKeydown"
            ></textarea>
            <button
              type="submit"
              class="send-btn premium-send-btn"
              :disabled="!inputMessage.trim() || status === 'streaming'"
              title="Envoyer le message"
              aria-label="Envoyer"
            >
              <span class="fr-icon-arrow-right-line" aria-hidden="true"></span>
            </button>
          </div>
          <div class="footer-hint fr-text--xs fr-text-mention--grey fr-mt-1w">
            <span>Appuyez sur <strong>Entrée</strong> pour envoyer, <strong>Maj + Entrée</strong> pour aller à la ligne</span>
          </div>
        </form>
      </footer>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useChat } from '@ai-sdk/vue'
import { DefaultChatTransport } from 'ai'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { API_URL, getCSRFToken } from '../services/api'
import { useConstatationStore } from '../stores/constatation'

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const router = useRouter()
const route = useRoute()
const constatationStore = useConstatationStore()

const inputMessage = ref('')
const chatBodyRef = ref<HTMLElement | null>(null)

// Transport configured for Django chatbot API with CSRF token
const transport = new DefaultChatTransport({
  api: `${API_URL}/chatbot/chat/`,
  credentials: 'include',
  headers: () => {
    const csrfToken = getCSRFToken()
    return csrfToken ? { 'X-CSRFToken': csrfToken } : {}
  },
})

// useChat composable
const { messages, status, error, sendMessage } = useChat({
  transport,
})

// Suggestions rapides contextuelles selon la route
const quickPrompts = computed(() => {
  const currentPath = route.path
  if (currentPath.includes('constatation')) {
    return [
      'Quels sont les éléments obligatoires du constat ?',
      'Quelle différence entre domaine public et privé ?',
      'Comment qualifier le volume des déchets ?',
    ]
  }
  if (currentPath.includes('procedure')) {
    return [
      'Quels sont les délais d’une mise en demeure ?',
      'Comment ordonner une astreinte journalière ?',
      'Quel recours si le contrevenant refuse de payer ?',
    ]
  }
  return [
    'J\'ai constaté un dépôt de gravats sur ma commune',
    'Quelle est la procédure légale contre un dépôt sauvage ?',
    'Quels sont les pouvoirs de police du maire ?',
  ]
})

const closeDrawer = () => {
  emit('close')
}

const sendQuickPrompt = (prompt: string) => {
  inputMessage.value = prompt
  handleSubmitMessage()
}

const handleKeydown = (event: KeyboardEvent) => {
  // Support standard ChatGPT / Gemini behavior:
  // - Enter alone (no Shift, Ctrl, Alt, Meta) => Submit message
  // - Shift + Enter or Ctrl + Enter => Insert newline
  // - Ignore while composing in IME
  if (
    event.key === 'Enter' &&
    !event.shiftKey &&
    !event.ctrlKey &&
    !event.altKey &&
    !event.metaKey &&
    !event.isComposing
  ) {
    event.preventDefault()
    handleSubmitMessage()
  }
}

const handleSubmitMessage = () => {
  const text = inputMessage.value.trim()
  if (!text || status.value === 'streaming') return

  inputMessage.value = ''
  sendMessage({ text })
  scrollToBottom()
}

const getMessageText = (message: any): string => {
  if (typeof message.content === 'string') {
    return message.content
  }
  if (Array.isArray(message.parts)) {
    return message.parts
      .filter((p: any) => p.type === 'text')
      .map((p: any) => p.text)
      .join('')
  }
  return ''
}

const getToolCalls = (message: any): any[] => {
  const tools: any[] = []
  if (Array.isArray(message.parts)) {
    for (const part of message.parts) {
      if (part.type === 'tool-input-available' || part.type?.startsWith('tool-')) {
        tools.push(part)
      }
    }
  }
  return tools
}

const renderMarkdown = (content: string): string => {
  if (!content) return ''
  const rawHtml = marked.parse(content, { breaks: true, gfm: true }) as string
  return DOMPurify.sanitize(rawHtml)
}

const applyDraftAndRedirect = (inputData: any) => {
  if (!inputData) return

  if (inputData.commune) {
    constatationStore.formData.commune = inputData.commune
  }
  if (inputData.localisationDepot) {
    constatationStore.formData.localisationDepot = inputData.localisationDepot
  }
  if (inputData.volumeDepot) {
    constatationStore.formData.volumeDepot = inputData.volumeDepot
  }
  if (Array.isArray(inputData.typesDepot) && inputData.typesDepot.length > 0) {
    constatationStore.formData.typesDepot = inputData.typesDepot
  }
  if (Array.isArray(inputData.natureTerrain) && inputData.natureTerrain.length > 0) {
    constatationStore.formData.natureTerrain = inputData.natureTerrain
  }
  if (inputData.precisionsDepot) {
    constatationStore.formData.precisionsDepot = inputData.precisionsDepot
  }
  if (typeof inputData.auteurIdentifie === 'boolean') {
    constatationStore.formData.auteurIdentifie = inputData.auteurIdentifie
  }

  closeDrawer()
  router.push('/commencer-constatation')
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight
    }
  })
}

// Auto-scroll on new message / streaming updates
watch(
  () => [messages.value, status.value],
  () => {
    scrollToBottom()
  },
  { deep: true }
)

// Scroll on drawer open
watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      scrollToBottom()
    }
  }
)
</script>

<style scoped>
.assistant-drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 18, 0.45);
  backdrop-filter: blur(4px);
  z-index: 1050;
  display: flex;
  justify-content: flex-end;
  animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 1rem;
}

.assistant-drawer {
  width: 520px;
  max-width: 100%;
  height: calc(100vh - 2rem);
  background-color: var(--background-default-grey, #ffffff);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 145, 0.08);
  box-shadow: 0 12px 40px rgba(0, 0, 145, 0.16);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.assistant-header {
  border-bottom: 1px solid var(--border-default-grey, #e5e5e5);
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fe 100%);
}

.assistant-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assistant-title-group {
  display: flex;
  align-items: center;
}

.assistant-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #eef0fc 0%, #dfe4fd 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 145, 0.1);
  border: 1px solid var(--border-default-blue-france, #d0d7ff);
}

.assistant-badge-pill {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-action-high-blue-france, #000091);
  background-color: #e8edff;
  padding: 0.15rem 0.5rem;
  border-radius: 20px;
}

.assistant-main-title {
  font-weight: 700;
  color: var(--text-title-grey, #161616);
}

.close-btn-round {
  width: 36px;
  height: 36px;
  border-radius: 50% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-alt-grey, #f6f6f6);
  transition: all 0.2s ease;
}

.close-btn-round:hover {
  background-color: #e5e5e5;
  transform: rotate(90deg);
}

.text-primary {
  color: var(--text-action-high-blue-france, #000091);
}

.assistant-body {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  background-color: #fafbfe;
}

/* Welcome Box & Suggestions */
.welcome-box {
  border-radius: 14px;
}

.welcome-badge {
  display: inline-flex;
  align-items: center;
  color: var(--text-action-high-blue-france, #000091);
  font-weight: 600;
}

.welcome-text {
  line-height: 1.5;
  color: var(--text-default-grey, #2b2b2b);
}

.quick-prompts-label {
  font-weight: 600;
}

.quick-prompts {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.premium-prompt-pill {
  background-color: #ffffff;
  border: 1px solid var(--border-default-blue-france, #cdd6ff);
  border-radius: 10px;
  padding: 0.55rem 0.75rem;
  font-size: 0.8rem;
  text-align: left;
  color: var(--text-action-high-blue-france, #000091);
  font-weight: 500;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0, 0, 145, 0.04);
  transition: all 0.2s ease;
  cursor: pointer;
}

.premium-prompt-pill:hover {
  background-color: #f0f3ff;
  border-color: var(--border-active-blue-france, #000091);
  transform: translateX(3px);
  box-shadow: 0 4px 10px rgba(0, 0, 145, 0.08);
}

/* Bulles de discussion */
.chat-bubble-row {
  display: flex;
  width: 100%;
}

.chat-bubble-row.user-row {
  justify-content: flex-end;
}

.chat-bubble-row.assistant-row {
  justify-content: flex-start;
}

.chat-bubble {
  max-width: 86%;
  border-radius: 16px;
  padding: 0.65rem 1rem;
  word-break: break-word;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.user-bubble {
  background: linear-gradient(135deg, #000091 0%, #1e1eaf 100%);
  color: #ffffff;
  border-bottom-right-radius: 4px;
  min-width: 90px;
}

.user-bubble .bubble-sender {
  color: rgba(255, 255, 255, 0.75);
  font-weight: 600;
  font-size: 0.7rem;
  margin-bottom: 0.2rem;
}

.user-bubble .user-message-content {
  line-height: 1.35;
  word-break: break-word;
}

.assistant-bubble {
  background-color: #ffffff;
  color: var(--text-default-grey, #161616);
  border-bottom-left-radius: 4px;
  border: 1px solid rgba(0, 0, 145, 0.08);
}

.assistant-bubble .bubble-sender {
  color: var(--text-action-high-blue-france, #000091);
  font-weight: 600;
  font-size: 0.7rem;
  margin-bottom: 0.25rem;
}

.message-rendered-markdown {
  line-height: 1.45;
}

.message-rendered-markdown :deep(p) {
  margin-bottom: 0.45rem;
}

.message-rendered-markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.message-rendered-markdown :deep(ul),
.message-rendered-markdown :deep(ol) {
  padding-left: 1.25rem;
  margin-bottom: 0.45rem;
  margin-top: 0.2rem;
}

.message-rendered-markdown :deep(li) {
  margin-bottom: 0.25rem;
}

/* Carte de brouillon Premium */
.premium-draft-card {
  background: linear-gradient(135deg, #f5f6fd 0%, #eef0fc 100%);
  border: 1px solid var(--border-default-blue-france, #cdd6ff);
  border-left: 4px solid var(--border-active-blue-france, #000091);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 145, 0.08);
}

.draft-card-header {
  display: flex;
  align-items: center;
}

.draft-card-icon-wrap {
  width: 34px;
  height: 34px;
  background-color: #ffffff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 145, 0.08);
}

.draft-card-title {
  color: var(--text-action-high-blue-france, #000091);
}

.draft-recap-list {
  list-style: none;
  padding: 0.75rem;
  background-color: #ffffff;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 145, 0.06);
}

.draft-recap-list li {
  margin-bottom: 0.35rem;
  display: flex;
  justify-content: space-between;
}

.draft-recap-list li:last-child {
  margin-bottom: 0;
}

.recap-label {
  color: var(--text-label-grey, #666);
  font-weight: 500;
}

.recap-value {
  font-weight: 600;
  color: var(--text-title-grey, #161616);
  text-align: right;
}

.premium-draft-action-btn {
  border-radius: 8px !important;
  font-weight: 600;
  padding: 0.65rem 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.18);
  transition: all 0.2s ease;
}

.premium-draft-action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 145, 0.25);
}

/* Animation Typing */
.typing-indicator {
  display: inline-flex;
  gap: 4px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: var(--text-action-high-blue-france, #000091);
  border-radius: 50%;
  animation: typingBounce 1.2s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typingBounce {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.loading-bubble {
  display: flex;
  align-items: center;
  padding: 0.65rem 1rem;
}

/* Footer & Formulaire Premium */
.assistant-footer {
  border-top: 1px solid var(--border-default-grey, #e5e5e5);
  background-color: #ffffff;
}

.premium-input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  background-color: var(--background-default-grey, #ffffff);
  border: 1px solid var(--border-default-grey, #ddd);
  border-radius: 14px;
  padding: 0.6rem 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 145, 0.04);
  transition: all 0.2s ease;
}

.premium-input-wrapper:focus-within {
  border-color: var(--border-active-blue-france, #000091);
  box-shadow: 0 0 0 1px var(--border-active-blue-france, #000091), 0 4px 16px rgba(0, 0, 145, 0.1);
}

.premium-textarea {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  resize: none;
  margin-bottom: 0;
  padding: 0.25rem 0.25rem !important;
  min-height: 72px !important;
  max-height: 180px;
  font-size: 0.95rem;
  line-height: 1.45;
}

.premium-send-btn {
  height: 46px;
  width: 46px;
  border-radius: 12px;
  border: none;
  background-color: var(--background-action-high-blue-france, #000091);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-bottom: 4px;
}

.premium-send-btn:hover:not(:disabled) {
  background-color: #1212ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(0, 0, 145, 0.25);
}

.premium-send-btn:disabled {
  background-color: #e5e5e5;
  color: #929292;
  cursor: not-allowed;
}

.footer-hint {
  text-align: right;
  font-size: 0.72rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

@media (max-width: 576px) {
  .assistant-drawer-overlay {
    padding: 0;
  }
  .assistant-drawer {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
  }
}
</style>
