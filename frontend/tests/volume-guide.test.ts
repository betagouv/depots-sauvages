import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import VolumeGuideGrid from '@/components/shared/VolumeGuideGrid.vue'
import VolumeGuideModal from '@/components/shared/VolumeGuideModal.vue'
import VolumeGuideAccordion from '@/components/forms/constatation/VolumeGuideAccordion.vue'

describe('VolumeGuideGrid.vue', () => {
  it('affiche les catégories de volume de référence', () => {
    const wrapper = mount(VolumeGuideGrid)
    expect(wrapper.text()).toContain('Petits contenants & ménager')
    expect(wrapper.text()).toContain('Mobilier & Électroménager')
    expect(wrapper.text()).toContain('Véhicules légers')
    expect(wrapper.text()).toContain('Gros volumes & Bennes')
  })

  it('émet select-volume avec la valeur numérique et le libellé lors du clic', async () => {
    const wrapper = mount(VolumeGuideGrid)
    const button = wrapper.findAll('.volume-tag').find((btn) => btn.text().includes('0.1 m³'))
    expect(button).toBeDefined()
    await button!.trigger('click')

    expect(wrapper.emitted('select-volume')).toBeTruthy()
    expect(wrapper.emitted('select-volume')![0]).toEqual([0.1, 'Sac poubelle standard'])
  })

  it('applique la classe sélectionnée sur la valeur courante', () => {
    const wrapper = mount(VolumeGuideGrid, {
      props: {
        currentVolumeM3: 1.5,
      },
    })
    const selectedButton = wrapper.find('.volume-tag--selected')
    expect(selectedButton.exists()).toBe(true)
    expect(selectedButton.text()).toContain('1.5 m³')
  })
})

describe('VolumeGuideModal.vue', () => {
  it('transmet les props et gère la sélection d\'un volume', async () => {
    const wrapper = mount(VolumeGuideModal, {
      props: {
        opened: true,
        currentVolumeM3: 0.5,
      },
      global: {
        stubs: {
          DsfrModal: {
            template: '<div class="dsfr-modal-stub" v-if="opened"><slot /></div>',
            props: ['opened', 'title', 'size'],
          },
        },
      },
    })

    const grid = wrapper.findComponent(VolumeGuideGrid)
    expect(grid.exists()).toBe(true)
    expect(grid.props('currentVolumeM3')).toBe(0.5)

    // Simuler sélection
    grid.vm.$emit('select-volume', 2, 'Remorque de voiture')

    expect(wrapper.emitted('select-volume')).toBeTruthy()
    expect(wrapper.emitted('select-volume')![0]).toEqual([2, 'Remorque de voiture'])
    expect(wrapper.emitted('close')).toBeTruthy()
  })
})

describe('VolumeGuideAccordion.vue', () => {
  it('intègre VolumeGuideGrid et relaie l\'événement select-volume', async () => {
    const wrapper = mount(VolumeGuideAccordion, {
      props: {
        currentVolumeM3: 3,
      },
      global: {
        stubs: {
          DsfrAccordion: {
            template: '<div class="dsfr-accordion-stub"><slot /></div>',
            props: ['title', 'titleTag'],
          },
        },
      },
    })

    const grid = wrapper.findComponent(VolumeGuideGrid)
    expect(grid.exists()).toBe(true)
    expect(grid.props('currentVolumeM3')).toBe(3)

    grid.vm.$emit('select-volume', 3, 'Utilitaire léger')
    expect(wrapper.emitted('select-volume')).toBeTruthy()
    expect(wrapper.emitted('select-volume')![0]).toEqual([3])
  })
})
