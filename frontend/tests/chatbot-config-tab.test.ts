import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import ChatbotConfigTab from '../components/backoffice/ChatbotConfigTab.vue'
import * as api from '../services/api'

vi.mock('../services/api', () => ({
  getChatbotConfig: vi.fn(),
  updateChatbotConfig: vi.fn(),
  testChatbotConnection: vi.fn(),
}))

describe('ChatbotConfigTab.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('affiche les données chargées depuis l’API', async () => {
    vi.mocked(api.getChatbotConfig).mockResolvedValue({
      id: 1,
      provider: 'openrouter',
      model: 'deepseek/deepseek-chat',
      base_url: 'https://openrouter.ai/api/v1',
      timeout: 40,
      system_prompt: 'Prompt de test initial',
      has_api_key: true,
      api_key_masked: 'sk-o••••••••6789',
      default_system_prompt: 'Prompt par défaut officiel',
    })

    const wrapper = mount(ChatbotConfigTab)

    // Attente du chargement
    await vi.waitFor(() => {
      expect(wrapper.find('#chatbot-provider').exists()).toBe(true)
    })

    const select = wrapper.find('#chatbot-provider').element as HTMLSelectElement
    expect(select.value).toBe('openrouter')

    const modelInput = wrapper.find('#chatbot-model').element as HTMLInputElement
    expect(modelInput.value).toBe('deepseek/deepseek-chat')

    const textarea = wrapper.find('#chatbot-system-prompt').element as HTMLTextAreaElement
    expect(textarea.value).toBe('Prompt de test initial')
  })

  it('permet de restaurer le prompt par défaut', async () => {
    vi.mocked(api.getChatbotConfig).mockResolvedValue({
      id: 1,
      provider: 'mock',
      model: '',
      timeout: 40,
      system_prompt: 'Prompt modifié',
      default_system_prompt: 'Prompt par défaut officiel',
    })

    const wrapper = mount(ChatbotConfigTab)
    await vi.waitFor(() => {
      expect(wrapper.find('#chatbot-system-prompt').exists()).toBe(true)
    })

    const restoreBtn = wrapper.findAll('button').find((b) => b.text().includes('Restaurer prompt initial'))
    expect(restoreBtn).toBeDefined()
    await restoreBtn!.trigger('click')

    const textarea = wrapper.find('#chatbot-system-prompt').element as HTMLTextAreaElement
    expect(textarea.value).toBe('Prompt par défaut officiel')
  })

  it('appelle updateChatbotConfig lors de la sauvegarde', async () => {
    vi.mocked(api.getChatbotConfig).mockResolvedValue({
      id: 1,
      provider: 'mock',
      model: '',
      timeout: 40,
      system_prompt: 'Prompt original',
      default_system_prompt: 'Prompt original',
    })
    vi.mocked(api.updateChatbotConfig).mockResolvedValue({
      id: 1,
      provider: 'mistral',
      model: 'mistral-large-latest',
      timeout: 50,
      system_prompt: 'Prompt mis à jour',
    })

    const wrapper = mount(ChatbotConfigTab)
    await vi.waitFor(() => {
      expect(wrapper.find('#chatbot-provider').exists()).toBe(true)
    })

    await wrapper.find('#chatbot-provider').setValue('mistral')
    await wrapper.find('#chatbot-system-prompt').setValue('Prompt mis à jour')

    const saveBtn = wrapper.findAll('button').find((b) => b.text().includes('Enregistrer'))
    expect(saveBtn).toBeDefined()
    await saveBtn!.trigger('click')

    expect(api.updateChatbotConfig).toHaveBeenCalledWith(
      expect.objectContaining({
        provider: 'mistral',
        system_prompt: 'Prompt mis à jour',
      })
    )
  })

  it('appelle testChatbotConnection lors du clic sur le bouton de test', async () => {
    vi.mocked(api.getChatbotConfig).mockResolvedValue({
      id: 1,
      provider: 'openrouter',
      model: 'deepseek/deepseek-chat',
      timeout: 40,
      system_prompt: 'Prompt',
      has_api_key: true,
      api_key_masked: 'sk-o••••••••',
    })
    vi.mocked(api.testChatbotConnection).mockResolvedValue({
      success: true,
      message: 'Connexion réussie',
      latency_ms: 120,
      sample_reply: 'pong',
    })

    const wrapper = mount(ChatbotConfigTab)
    await vi.waitFor(() => {
      expect(wrapper.find('#chatbot-provider').exists()).toBe(true)
    })

    const testBtn = wrapper.findAll('button').find((b) => b.text().includes('Tester la connexion'))
    expect(testBtn).toBeDefined()
    await testBtn!.trigger('click')

    expect(api.testChatbotConnection).toHaveBeenCalledWith(
      expect.objectContaining({
        provider: 'openrouter',
        model: 'deepseek/deepseek-chat',
      })
    )

    await vi.waitFor(() => {
      expect(wrapper.text()).toContain('Connexion réussie !')
    })
  })
})
