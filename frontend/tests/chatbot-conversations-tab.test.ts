import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import ChatbotConversationsTab from '../components/backoffice/ChatbotConversationsTab.vue'
import * as api from '../services/api'

vi.mock('../services/api', () => ({
  getChatbotConversations: vi.fn(),
  getChatbotConversationDetail: vi.fn(),
  deleteChatbotConversation: vi.fn(),
}))

describe('ChatbotConversationsTab.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('affiche les conversations et gère les retours à la ligne et le Markdown dans le détail', async () => {
    vi.mocked(api.getChatbotConversations).mockResolvedValue({
      count: 1,
      total_pages: 1,
      current_page: 1,
      stats: {
        total_conversations: 1,
        drafts_count: 0,
        positive_count: 1,
        negative_count: 0,
      },
      results: [
        {
          id: 'test-conv-1',
          user_email: 'agent@test.fr',
          user_name: 'Agent Test',
          current_path: '/demarrer-constatation',
          messages_count: 2,
          first_user_message: 'Bonjour\nJ’ai un problème de dépôt sauvage.',
          last_user_message: 'Bonjour\nJ’ai un problème de dépôt sauvage.',
          has_draft_proposed: false,
          feedback: 'up',
          created_at: '2026-03-01T10:00:00Z',
          updated_at: '2026-03-01T10:05:00Z',
        },
      ],
    })

    vi.mocked(api.getChatbotConversationDetail).mockResolvedValue({
      id: 'test-conv-1',
      user_email: 'agent@test.fr',
      user_name: 'Agent Test',
      current_path: '/demarrer-constatation',
      messages_count: 2,
      first_user_message: 'Bonjour\nJ’ai un problème de dépôt sauvage.',
      last_user_message: 'Bonjour\nJ’ai un problème de dépôt sauvage.',
      has_draft_proposed: false,
      feedback: 'up',
      created_at: '2026-03-01T10:00:00Z',
      updated_at: '2026-03-01T10:05:00Z',
      messages: [
        {
          role: 'user',
          content: 'Bonjour\nJ’ai un problème de dépôt sauvage.\nDeuxième ligne.',
          timestamp: '2026-03-01T10:00:00Z',
        },
        {
          role: 'assistant',
          content: 'Voici les étapes à suivre :\n- Notifier le maire\n- Rédiger le rapport\n\nFin du message.',
          timestamp: '2026-03-01T10:01:00Z',
          feedback: 'up',
        },
      ],
    })

    const wrapper = mount(ChatbotConversationsTab)

    // Attendre le chargement
    await vi.waitFor(() => {
      expect(wrapper.text()).toContain('agent@test.fr')
    })

    // Clic pour ouvrir le détail
    await wrapper.find('.hover-row').trigger('click')

    await vi.waitFor(() => {
      expect(wrapper.find('.conversation-modal-backdrop').exists()).toBe(true)
    })

    // Vérifier le message de l'utilisateur avec la classe user
    const userMsg = wrapper.find('.dialog-bubble__content--user')
    expect(userMsg.exists()).toBe(true)
    expect(userMsg.text()).toContain('Bonjour\nJ’ai un problème de dépôt sauvage.\nDeuxième ligne.')

    // Vérifier le message assistant rendu en HTML markdown avec listes / retours à la ligne
    const assistantMsg = wrapper.find('.dialog-bubble__content--markdown')
    expect(assistantMsg.exists()).toBe(true)
    expect(assistantMsg.html()).toContain('<ul>')
    expect(assistantMsg.html()).toContain('<li>Notifier le maire</li>')
    expect(assistantMsg.html()).toContain('<li>Rédiger le rapport</li>')
    expect(assistantMsg.html()).toContain('<p>Fin du message.</p>')
  })
})
