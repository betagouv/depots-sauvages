import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick, reactive } from 'vue'
import Cloture from '../components/steps/Cloture.vue'
import ListeActions from '../components/steps/ListeActions.vue'
import Notification from '../components/steps/Notification.vue'
import SuiviActions from '../components/steps/SuiviActions.vue'
import { trackUserAction } from '../services/tracking'
import { createEmptySuivi } from '../stores/suivi-procedure'

vi.mock('../services/matomo', () => ({
  trackAndOpenLink: vi.fn(),
  trackEvent: vi.fn(),
}))

vi.mock('../services/tracking', () => ({
  trackUserAction: vi.fn(),
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() }),
}))

const stubs = {
  DsfrAlert: { template: '<div><slot /></div>' },
  DsfrButton: true,
  DsfrInput: { props: ['label'], template: '<label class="input-stub">{{ label }}</label>' },
  DsfrSelect: { props: ['label'], template: '<label class="input-stub">{{ label }}</label>' },
  DsfrCheckbox: true,
  StepLockBanner: true,
}

const trackCalls = (event: string) =>
  vi.mocked(trackUserAction).mock.calls.filter(([name]) => name === event)

beforeEach(() => {
  vi.mocked(trackUserAction).mockClear()
})

describe('ListeActions', () => {
  it('affiche les champs complémentaires même si la case n’est pas cochée', () => {
    const wrapper = mount(ListeActions, {
      props: {
        stepId: 'test',
        actions: [{ id: 'a', label: 'Action', completed: false }],
      },
      slots: { 'extra-a': '<p class="extra">Champ</p>' },
      global: { stubs },
    })
    expect(wrapper.find('.extra').exists()).toBe(true)
  })
})

describe('Notification : auto-cochage', () => {
  const mountNotification = () => {
    const suivi = reactive(createEmptySuivi())
    const wrapper = mount(Notification, {
      props: { suivi, lettreInfoUrl: '/lettre', constatationId: 1 },
      global: { stubs },
    })
    return { suivi, wrapper }
  }

  it('montre la date d’envoi et le statut AR sans cochage préalable', () => {
    const { wrapper } = mountNotification()
    expect(wrapper.text()).toContain("Date d'envoi du courrier")
    expect(wrapper.text()).toContain("Quel est le statut de l'accusé réception ?")
  })

  it('coche « lettre envoyée » à la saisie de la date et envoie un seul événement', async () => {
    const { suivi } = mountNotification()
    suivi.lettre_envoyee_date = '2026-11-02'
    await nextTick()
    expect(suivi.lettre_envoyee).toBe(true)
    expect(trackCalls('notification_auteur_envoyee')).toHaveLength(1)
  })

  it('coche « lettre envoyée » à la saisie du numéro de suivi', async () => {
    const { suivi } = mountNotification()
    suivi.numero_suivi_lettre = '1A00915820380'
    await nextTick()
    expect(suivi.lettre_envoyee).toBe(true)
    expect(trackCalls('notification_auteur_envoyee')).toHaveLength(1)
  })

  it('coche « AR reçu » au choix du statut et envoie un seul événement', async () => {
    const { suivi } = mountNotification()
    suivi.ar_statut = 'npai'
    await nextTick()
    expect(suivi.ar_recu).toBe(true)
    expect(trackCalls('accuse_reception_enregistre')).toHaveLength(1)
  })

  it('ne décoche jamais la case quand on vide le champ', async () => {
    const { suivi } = mountNotification()
    suivi.lettre_envoyee_date = '2026-11-02'
    await nextTick()
    suivi.lettre_envoyee_date = ''
    await nextTick()
    expect(suivi.lettre_envoyee).toBe(true)
  })
})

describe('Sanctionner : montant et calculateur', () => {
  const mountSanction = () => {
    const suivi = reactive({ ...createEmptySuivi(), decision_poursuite: 'sanction' })
    const wrapper = mount(SuiviActions, {
      props: { suivi, modifyUrl: '/constatation/1', constatationId: 1 },
      global: { stubs },
    })
    return { suivi, wrapper }
  }

  it('montre le montant et le calculateur avant de cocher « Fixer le montant »', () => {
    const { wrapper } = mountSanction()
    expect(wrapper.text()).toContain("Montant de l'amende (€)")
    expect(wrapper.text()).toContain('utilisez notre calculateur')
  })

  it('coche « Fixer le montant » à la saisie et envoie un seul événement', async () => {
    const { suivi } = mountSanction()
    suivi.montant_amende = 500
    await nextTick()
    expect(suivi.montant_fixe).toBe(true)
    expect(trackCalls('sanction_decidee')).toHaveLength(1)
  })

  it('garde le montant saisi si l’agent décoche la case', async () => {
    const { suivi, wrapper } = mountSanction()
    suivi.montant_amende = 500
    await nextTick()
    wrapper
      .findComponent(ListeActions)
      .vm.$emit('update-case', { id: 'fixer_montant', label: '' }, false)
    await nextTick()
    expect(suivi.montant_fixe).toBe(false)
    expect(suivi.montant_amende).toBe(500)
  })
})

describe('Clôturer : recouvrement', () => {
  it('montre la date de recouvrement et coche la case à la saisie', async () => {
    const suivi = reactive({ ...createEmptySuivi(), decision_poursuite: 'sanction' })
    const wrapper = mount(Cloture, {
      props: { suivi, constatationId: 1 },
      global: { stubs },
    })
    expect(wrapper.text()).toContain('Date de recouvrement')

    suivi.date_recouvrement_effective = '2026-11-02'
    await nextTick()
    expect(suivi.montant_recouvre).toBe(true)
    expect(trackCalls('recouvrement_confirme')).toHaveLength(1)
  })
})
