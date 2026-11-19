import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import ConflictBanner from '../components/shared/ConflictBanner.vue'

describe('ConflictBanner', () => {
  it('affiche le bandeau quand visible est true', () => {
    const wrapper = mount(ConflictBanner, {
      props: {
        visible: true,
        updatedBy: 'Claire Lefevre',
      },
    })

    expect(wrapper.find('.conflict-banner').exists()).toBe(true)
    expect(wrapper.text()).toContain('Claire Lefevre')
    expect(wrapper.text()).toContain('Ce dossier a été modifié par un autre utilisateur')
  })

  it('ne rend rien quand visible est false', () => {
    const wrapper = mount(ConflictBanner, {
      props: {
        visible: false,
      },
    })

    expect(wrapper.find('.conflict-banner').exists()).toBe(false)
  })

  it('émet l’événement reload lors du clic sur recharger', async () => {
    const wrapper = mount(ConflictBanner, {
      props: {
        visible: true,
      },
    })

    const reloadButton = wrapper
      .findAll('button')
      .find((b) => b.text().includes('Recharger la version à jour'))
    expect(reloadButton).toBeDefined()
    await reloadButton!.trigger('click')

    expect(wrapper.emitted('reload')).toHaveLength(1)
  })

  it('émet l’événement force-save lors du clic sur écraser', async () => {
    const wrapper = mount(ConflictBanner, {
      props: {
        visible: true,
      },
    })

    const forceButton = wrapper
      .findAll('button')
      .find((b) => b.text().includes('Conserver mes saisies et écraser'))
    expect(forceButton).toBeDefined()
    await forceButton!.trigger('click')

    expect(wrapper.emitted('force-save')).toHaveLength(1)
  })

  it('émet l’événement close lors du clic sur ignorer', async () => {
    const wrapper = mount(ConflictBanner, {
      props: {
        visible: true,
        dismissible: true,
      },
    })

    const closeButton = wrapper
      .findAll('button')
      .find((b) => b.text().includes('Ignorer'))
    expect(closeButton).toBeDefined()
    await closeButton!.trigger('click')

    expect(wrapper.emitted('close')).toHaveLength(1)
  })
})
