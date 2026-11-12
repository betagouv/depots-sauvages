<template>
  <div class="fr-tabs__panel fr-tabs__panel--selected" role="tabpanel">
    <!-- Entête avec statistiques clés -->
    <div class="bo-header-row fr-mb-3w">
      <div class="bo-header-row__title">
        <h2 class="fr-h3 fr-mb-0-5v">
          <span class="fr-icon-discuss-line fr-text-title-blue-france fr-mr-1w" aria-hidden="true"></span>
          Suivi des conversations Chatbot
        </h2>
        <p class="fr-text--sm fr-text-mention-grey fr-mb-0">
          Consultez et analysez les questions et besoins exprimés par les agents et élus via l'Assistant IA.
        </p>
      </div>

      <div class="bo-header-row__actions">
        <button
          type="button"
          class="fr-btn fr-btn--secondary fr-btn--sm"
          :disabled="isLoading"
          @click="fetchConversations"
        >
          <span :class="isLoading ? 'fr-icon-refresh-line' : 'fr-icon-refresh-line'" class="fr-mr-1w" aria-hidden="true"></span>
          Actualiser
        </button>
      </div>
    </div>

    <!-- Tuiles d'indicateurs rapides (KPIs) -->
    <div class="fr-grid-row fr-grid-row--gutters fr-mb-3w">
      <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
        <div class="fr-card fr-p-2w kpi-card">
          <span class="fr-text--xs fr-text-mention-grey fr-mb-1v">Total conversations</span>
          <strong class="fr-h4 fr-mb-0 text-primary">{{ stats.total_conversations }}</strong>
        </div>
      </div>
      <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
        <div class="fr-card fr-p-2w kpi-card">
          <span class="fr-text--xs fr-text-mention-grey fr-mb-1v">Brouillons de constat créés</span>
          <strong class="fr-h4 fr-mb-0 text-success">{{ stats.drafts_count }}</strong>
        </div>
      </div>
      <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
        <div class="fr-card fr-p-2w kpi-card">
          <span class="fr-text--xs fr-text-mention-grey fr-mb-1v">Avis utiles (👍)</span>
          <strong class="fr-h4 fr-mb-0 text-success">{{ stats.positive_count }}</strong>
        </div>
      </div>
      <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
        <div class="fr-card fr-p-2w kpi-card">
          <span class="fr-text--xs fr-text-mention-grey fr-mb-1v">À améliorer (👎)</span>
          <strong class="fr-h4 fr-mb-0 text-danger">{{ stats.negative_count }}</strong>
        </div>
      </div>
    </div>

    <!-- Barre de filtres et recherche -->
    <div class="bo-filter-bar-container fr-mb-3w">
      <div class="bo-search-row">
        <label class="bo-filter-label" for="conv-search-input">Rechercher</label>
        <input
          id="conv-search-input"
          v-model="filters.search"
          type="text"
          class="fr-input bo-w-full"
          placeholder="🔍 Rechercher par email, contenu de message, page..."
          @keyup.enter="applyFilters"
        />
      </div>

      <div class="bo-filters-grid">
        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-draft">Brouillon proposé</label>
          <select id="filter-draft" v-model="filters.hasDraft" class="fr-select" @change="applyFilters">
            <option value="">Tous</option>
            <option value="true">Oui (Brouillon généré)</option>
            <option value="false">Non</option>
          </select>
        </div>

        <div class="bo-filter-group-vertical">
          <label class="bo-filter-label" for="filter-feedback">Appréciation usager</label>
          <select id="filter-feedback" v-model="filters.feedback" class="fr-select" @change="applyFilters">
            <option value="">Tous les retours</option>
            <option value="up">👍 Utile</option>
            <option value="down">👎 À améliorer</option>
            <option value="none">Sans avis</option>
          </select>
        </div>

        <div class="bo-filter-group-vertical d-flex align-items-end">
          <button
            type="button"
            class="fr-btn fr-btn--secondary fr-btn--sm"
            @click="resetFilters"
          >
            Réinitialiser
          </button>
        </div>
      </div>
    </div>

    <!-- Barre d'état & Pagination -->
    <div class="fr-mb-2w bo-info-bar d-flex justify-content-between align-items-center flex-wrap" style="gap: 1rem">
      <span class="fr-text--sm fr-text-mention--grey fr-mb-0">
        <strong>{{ totalCount }}</strong> conversation(s) trouvée(s)
      </span>

      <div v-if="totalPages > 1" class="d-flex align-items-center" style="gap: 0.5rem">
        <button
          class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm"
          :disabled="page <= 1"
          @click="changePage(page - 1)"
        >
          Précédent
        </button>
        <span class="fr-text--xs fr-text-mention--grey">Page {{ page }} / {{ totalPages }}</span>
        <button
          class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm"
          :disabled="page >= totalPages"
          @click="changePage(page + 1)"
        >
          Suivant
        </button>
      </div>
    </div>

    <!-- Tableau des conversations -->
    <div class="bo-table-container">
      <table class="bo-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Utilisateur</th>
            <th>Page d'origine</th>
            <th>Premier message (question usager)</th>
            <th>Nb échanges</th>
            <th>Brouillon</th>
            <th>Avis</th>
            <th class="text-right">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td colspan="8" class="text-center fr-py-3w">
              Chargement des conversations...
            </td>
          </tr>
          <tr v-else-if="conversations.length === 0">
            <td colspan="8" class="text-center fr-py-3w fr-text-mention-grey">
              Aucune conversation trouvée pour ces critères.
            </td>
          </tr>
          <tr
            v-for="conv in conversations"
            :key="conv.id"
            class="cursor-pointer hover-row"
            @click="openDetail(conv.id)"
          >
            <td class="fr-text--xs whitespace-nowrap">
              <strong>{{ formatDate(conv.updated_at) }}</strong>
            </td>
            <td>
              <div class="fr-text--xs font-weight-bold">{{ conv.user_name || 'Agent' }}</div>
              <div class="fr-text--xs fr-text-mention--grey">{{ conv.user_email }}</div>
            </td>
            <td class="fr-text--xs">
              <code>{{ conv.current_path || '/' }}</code>
            </td>
            <td class="fr-text--xs message-preview-cell" :title="conv.first_user_message">
              {{ conv.first_user_message || '—' }}
            </td>
            <td class="fr-text--xs text-center">
              <span class="fr-badge fr-badge--sm fr-badge--no-icon">{{ conv.messages_count }}</span>
            </td>
            <td class="fr-text--xs text-center">
              <span
                v-if="conv.has_draft_proposed"
                class="fr-badge fr-badge--sm fr-badge--success fr-badge--no-icon"
              >
                Oui
              </span>
              <span v-else class="fr-text-mention--grey">—</span>
            </td>
            <td class="fr-text--xs text-center">
              <span v-if="conv.feedback === 'up'" title="Utile">👍</span>
              <span v-else-if="conv.feedback === 'down'" title="À améliorer">👎</span>
              <span v-else class="fr-text-mention--grey">—</span>
            </td>
            <td class="text-right whitespace-nowrap" @click.stop>
              <button
                type="button"
                class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-icon-eye-line"
                title="Consulter le fil complet"
                @click="openDetail(conv.id)"
              ></button>
              <button
                type="button"
                class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-icon-delete-line text-danger"
                title="Supprimer la conversation"
                @click="confirmDelete(conv.id)"
              ></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modale de détail / Lecture du fil de discussion -->
    <div
      v-if="selectedConversation"
      class="conversation-modal-backdrop"
      @click.self="selectedConversation = null"
    >
      <div class="conversation-modal-dialog">
        <header class="conversation-modal-header fr-p-3w">
          <div>
            <h3 class="fr-h5 fr-mb-1v">Conversation Chatbot</h3>
            <p class="fr-text--xs fr-text-mention-grey fr-mb-0">
              Utilisateur : <strong>{{ selectedConversation.user_email }}</strong> |
              Page : <code>{{ selectedConversation.current_path || '/' }}</code> |
              Dernier message : {{ formatDate(selectedConversation.updated_at) }}
            </p>
          </div>
          <button
            class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-icon-close-line"
            title="Fermer"
            @click="selectedConversation = null"
          ></button>
        </header>

        <div class="conversation-modal-body fr-p-3w">
          <div
            v-for="(msg, idx) in selectedConversation.messages"
            :key="idx"
            class="dialog-bubble fr-mb-2w"
            :class="msg.role === 'user' ? 'dialog-bubble--user' : 'dialog-bubble--assistant'"
          >
            <div class="dialog-bubble__header fr-text--xs fr-mb-1v">
              <strong>{{ msg.role === 'user' ? (selectedConversation.user_name || 'Usager') : 'Assistant IA' }}</strong>
              <span class="fr-ml-1w fr-text-mention-grey">{{ formatTime(msg.timestamp) }}</span>
              <span v-if="msg.feedback === 'up'" class="fr-ml-1w" title="Avis usager positif">👍</span>
              <span v-if="msg.feedback === 'down'" class="fr-ml-1w" title="Avis usager négatif">👎</span>
            </div>
            <div
              v-if="msg.role === 'assistant'"
              class="dialog-bubble__content dialog-bubble__content--markdown fr-text--sm"
              v-html="renderMarkdown(msg.content)"
            ></div>
            <div
              v-else
              class="dialog-bubble__content dialog-bubble__content--user fr-text--sm"
            >
              {{ msg.content }}
            </div>
            <div v-if="msg.tool_calls && msg.tool_calls.length > 0" class="dialog-tool-call fr-mt-1w fr-p-2w">
              <span class="fr-badge fr-badge--sm fr-badge--info fr-mb-1v">Proposition de brouillon</span>
              <pre class="fr-text--xs fr-mb-0">{{ JSON.stringify(msg.tool_calls, null, 2) }}</pre>
            </div>
          </div>
        </div>

        <footer class="conversation-modal-footer fr-p-2w d-flex justify-content-end">
          <button
            type="button"
            class="fr-btn fr-btn--secondary fr-btn--sm"
            @click="selectedConversation = null"
          >
            Fermer
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  getChatbotConversations,
  getChatbotConversationDetail,
  deleteChatbotConversation,
  type ChatbotConversationSummary,
  type ChatbotConversationDetail,
} from '@/services/api'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const isLoading = ref(true)
const conversations = ref<ChatbotConversationSummary[]>([])
const totalCount = ref(0)
const page = ref(1)
const pageSize = ref(20)
const stats = reactive({
  total_conversations: 0,
  drafts_count: 0,
  positive_count: 0,
  negative_count: 0,
})

const filters = reactive({
  search: '',
  hasDraft: '',
  feedback: '',
})

const selectedConversation = ref<ChatbotConversationDetail | null>(null)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value) || 1)

const formatDate = (isoString: string) => {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const formatTime = (isoString?: string) => {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

const renderMarkdown = (content?: string): string => {
  if (!content || typeof content !== 'string') return ''
  const rawHtml = marked.parse(content, { breaks: true, gfm: true }) as string
  return DOMPurify.sanitize(rawHtml)
}

const fetchConversations = async () => {
  isLoading.value = true
  try {
    const res = await getChatbotConversations({
      page: page.value,
      page_size: pageSize.value,
      search: filters.search.trim() || undefined,
      has_draft: filters.hasDraft || undefined,
      feedback: filters.feedback || undefined,
    })
    conversations.value = res.results || []
    totalCount.value = res.count || 0
    if (res.stats) {
      stats.total_conversations = res.stats.total_conversations || 0
      stats.drafts_count = res.stats.drafts_count || 0
      stats.positive_count = res.stats.positive_count || 0
      stats.negative_count = res.stats.negative_count || 0
    }
  } catch (err) {
    console.error('Error fetching chatbot conversations:', err)
  } finally {
    isLoading.value = false
  }
}

const applyFilters = () => {
  page.value = 1
  fetchConversations()
}

const resetFilters = () => {
  filters.search = ''
  filters.hasDraft = ''
  filters.feedback = ''
  page.value = 1
  fetchConversations()
}

const changePage = (newPage: number) => {
  page.value = newPage
  fetchConversations()
}

const openDetail = async (id: string) => {
  try {
    const detail = await getChatbotConversationDetail(id)
    selectedConversation.value = detail
  } catch (err) {
    console.error('Error fetching conversation detail:', err)
  }
}

const confirmDelete = async (id: string) => {
  if (confirm('Voulez-vous supprimer cette conversation ?')) {
    try {
      await deleteChatbotConversation(id)
      fetchConversations()
      if (selectedConversation.value?.id === id) {
        selectedConversation.value = null
      }
    } catch (err) {
      console.error('Error deleting conversation:', err)
    }
  }
}

onMounted(() => {
  fetchConversations()
})
</script>

<style scoped>
.kpi-card {
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.text-primary {
  color: var(--text-action-high-blue-france, #000091);
}

.text-success {
  color: var(--text-default-success, #18753c);
}

.text-danger {
  color: var(--text-default-error, #ce0500);
}

.hover-row:hover {
  background-color: #f6f6f6;
}

.cursor-pointer {
  cursor: pointer;
}

.whitespace-nowrap {
  white-space: nowrap;
}

.message-preview-cell {
  max-width: 320px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 18, 0.5);
  backdrop-filter: blur(2px);
  z-index: 1100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.conversation-modal-dialog {
  background: #ffffff;
  border-radius: 12px;
  width: 760px;
  max-width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.conversation-modal-header {
  border-bottom: 1px solid var(--border-default-grey, #e5e5e5);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fafbfe;
}

.conversation-modal-body {
  flex: 1;
  overflow-y: auto;
  background-color: #f9f9fb;
}

.conversation-modal-footer {
  border-top: 1px solid var(--border-default-grey, #e5e5e5);
  background-color: #ffffff;
}

.dialog-bubble {
  padding: 0.85rem 1rem;
  border-radius: 8px;
  max-width: 85%;
}

.dialog-bubble--user {
  background-color: #e8edff;
  border: 1px solid #d0d7ff;
  margin-left: auto;
}

.dialog-bubble--assistant {
  background-color: #ffffff;
  border: 1px solid var(--border-default-grey, #e5e5e5);
  margin-right: auto;
}

.dialog-bubble__content {
  line-height: 1.5;
  word-break: break-word;
}

.dialog-bubble__content--user {
  white-space: pre-wrap;
}

.dialog-bubble__content--markdown {
  word-break: break-word;
}

.dialog-bubble__content--markdown :deep(p) {
  margin-bottom: 0.5rem;
}

.dialog-bubble__content--markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.dialog-bubble__content--markdown :deep(ul),
.dialog-bubble__content--markdown :deep(ol) {
  padding-left: 1.25rem;
  margin-bottom: 0.5rem;
  margin-top: 0.25rem;
}

.dialog-bubble__content--markdown :deep(li) {
  margin-bottom: 0.25rem;
}

.dialog-bubble__content--markdown :deep(pre) {
  background-color: #f0f2f8;
  padding: 0.5rem;
  border-radius: 4px;
  overflow-x: auto;
  white-space: pre-wrap;
}

.dialog-bubble__content--markdown :deep(code) {
  background-color: #f0f2f8;
  padding: 0.1rem 0.25rem;
  border-radius: 3px;
  font-size: 0.875em;
}

.dialog-tool-call {
  background-color: #f0f2f8;
  border-radius: 4px;
  border-left: 3px solid var(--text-action-high-blue-france, #000091);
}
</style>
