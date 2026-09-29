import '@testing-library/jest-dom'
import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import AccesRestreint from '../pages/acces-restreint.vue'
import * as api from '../services/api'

vi.mock('../services/api', () => ({
  getProConnectRejectedInfo: vi.fn(),
  submitProConnectAccessRequest: vi.fn(),
}))

describe('Page AccesRestreint', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('doit être accessible (A11y)', async () => {
    vi.mocked(api.getProConnectRejectedInfo).mockResolvedValueOnce({
      organization_label: 'Mairie Exemple',
      siren: '123456789',
      siret: '12345678900012',
      name: 'Jean Dupont',
      email: 'jean.dupont@exemple.fr',
    })

    const { container } = render(AccesRestreint, {
      global: {
        stubs: {
          RouterLink: {
            props: ['to'],
            template: `<a :href="to"><slot /></a>`,
          },
        },
      },
    })

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('pré-remplit le formulaire avec les données de la session de rejet', async () => {
    vi.mocked(api.getProConnectRejectedInfo).mockResolvedValueOnce({
      organization_label: 'Académie de Paris',
      siren: '123456789',
      siret: '12345678900012',
      name: 'Alice Martin',
      email: 'alice@ac-paris.fr',
    })

    render(AccesRestreint, {
      global: {
        stubs: {
          RouterLink: {
            props: ['to'],
            template: `<a :href="to"><slot /></a>`,
          },
        },
      },
    })

    expect(await screen.findByDisplayValue('Académie de Paris')).toBeInTheDocument()
    expect(screen.getByDisplayValue('123456789')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Alice Martin')).toBeInTheDocument()
    expect(screen.getByDisplayValue('alice@ac-paris.fr')).toBeInTheDocument()
  })

  it('soumet la demande d’accès et affiche le message de succès', async () => {
    vi.mocked(api.getProConnectRejectedInfo).mockResolvedValueOnce({
      organization_label: 'Académie de Paris',
      siren: '123456789',
      siret: '12345678900012',
      name: 'Alice Martin',
      email: 'alice@ac-paris.fr',
    })
    vi.mocked(api.submitProConnectAccessRequest).mockResolvedValueOnce({
      success: true,
      message: 'Votre demande a été transmise à notre équipe.',
    })

    render(AccesRestreint, {
      global: {
        stubs: {
          RouterLink: {
            props: ['to'],
            template: `<a :href="to"><slot /></a>`,
          },
        },
      },
    })

    await screen.findByDisplayValue('Académie de Paris')

    const submitBtn = screen.getByRole('button', { name: /Demander l'ouverture d'accès/i })
    await fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(api.submitProConnectAccessRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          organization_label: 'Académie de Paris',
          siren: '123456789',
          email: 'alice@ac-paris.fr',
        })
      )
    })

    expect(await screen.findByText(/Demande d'accès transmise avec succès/i)).toBeInTheDocument()
  })
})
