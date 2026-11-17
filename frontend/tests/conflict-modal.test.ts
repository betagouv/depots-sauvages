import { describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ConflictResolutionModal from '../components/shared/ConflictResolutionModal.vue'

describe('ConflictResolutionModal', () => {
  it('affiche les détails du conflit', () => {
    const wrapper = mount(ConflictResolutionModal, {
      props: {
        opened: true,
        updatedBy: 'Alice Dupont',
        message: 'Ce dossier a été modifié par Alice Dupont.',
      },
    })

    expect(wrapper.text()).toContain('Attention : Conflit de modification')
    expect(wrapper.text()).toContain('Alice Dupont')
  })

  it('émet un évènement reload lors du clic sur le bouton recharger', async () => {
    const wrapper = mount(ConflictResolutionModal, {
      props: {
        opened: true,
        updatedBy: 'Alice Dupont',
      },
    })

    const buttons = wrapper.findAll('button')
    const reloadBtn = buttons.find((b) => b.text().includes('Recharger'))
    expect(reloadBtn).toBeDefined()
    if (reloadBtn) {
      await reloadBtn.trigger('click')
      expect(wrapper.emitted('reload')).toBeTruthy()
    }
  })

  it('émet un évènement force-save lors du clic sur le bouton écraser', async () => {
    const wrapper = mount(ConflictResolutionModal, {
      props: {
        opened: true,
        updatedBy: 'Alice Dupont',
      },
    })

    const buttons = wrapper.findAll('button')
    const forceBtn = buttons.find((b) => b.text().includes('écraser') || b.text().includes('Conserver'))
    expect(forceBtn).toBeDefined()
    if (forceBtn) {
      await forceBtn.trigger('click')
      expect(wrapper.emitted('force-save')).toBeTruthy()
    }
  })
})
