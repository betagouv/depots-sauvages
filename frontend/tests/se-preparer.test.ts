import '@testing-library/jest-dom'
import VueDsfr from '@gouvminint/vue-dsfr'
import { fireEvent, render, screen } from '@testing-library/vue'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import { PREPARATION_SECTIONS } from '../constants/preparation-steps'
import SePreparer from '../pages/se-preparer.vue'
import * as api from '../services/api'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual('../services/api')
  return {
    ...actual,
    getUserInfo: vi.fn(),
  }
})

const renderPage = () =>
  render(SePreparer, {
    global: {
      plugins: [VueDsfr],
      stubs: {
        RouterLink: { props: ['to'], template: '<a :href="to"><slot /></a>' },
        VIcon: true,
      },
    },
  })

const mockUser = (isAuthenticated: boolean) =>
  (api.getUserInfo as any).mockResolvedValue({
    is_authenticated: isAuthenticated,
    proconnect_enabled: true,
  })

describe('Page Se préparer', () => {
  beforeEach(() => localStorage.clear())
  afterEach(() => vi.clearAllMocks())

  it('affiche toutes les sections et étapes pour un utilisateur connecté', async () => {
    mockUser(true)
    renderPage()

    for (const section of PREPARATION_SECTIONS) {
      expect(
        await screen.findByRole('heading', { level: 2, name: section.title })
      ).toBeInTheDocument()
      for (const step of section.steps) {
        expect(screen.getByLabelText(step.label)).toBeInTheDocument()
      }
    }
    expect(screen.getByText(/0 action faite sur/)).toBeInTheDocument()
  })

  it('invite à se connecter si l’utilisateur n’est pas connecté', async () => {
    mockUser(false)
    renderPage()

    expect(await screen.findByText('Se connecter via ProConnect')).toBeInTheDocument()
    expect(screen.queryByLabelText(PREPARATION_SECTIONS[0].steps[0].label)).not.toBeInTheDocument()
  })

  it('garde les étapes cochées après un rechargement', async () => {
    mockUser(true)
    const firstStep = PREPARATION_SECTIONS[0].steps[0]
    const { unmount } = renderPage()

    await fireEvent.click(await screen.findByLabelText(firstStep.label))
    expect(screen.getByText(/1 action faite sur/)).toBeInTheDocument()
    unmount()

    renderPage()
    expect(await screen.findByLabelText(firstStep.label)).toBeChecked()
  })

  it('présente les réponses rassurantes sans case à cocher', async () => {
    mockUser(true)
    renderPage()

    expect(await screen.findByText('Bon à savoir')).toBeInTheDocument()
    expect(screen.getByText(/Pas besoin de délibération/)).toBeInTheDocument()
    expect(screen.queryByLabelText(/délibération/)).not.toBeInTheDocument()
  })

  it('affiche le guide comme « Bientôt disponible » tant que son adresse manque', async () => {
    mockUser(true)
    renderPage()

    expect(await screen.findByLabelText("Je consulte le guide d'utilisation")).toBeInTheDocument()
    expect(screen.getByText('Bientôt disponible')).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Ouvrir le guide/ })).not.toBeInTheDocument()
  })

  it('ignore les étapes cochées qui n’existent plus', async () => {
    localStorage.setItem('se-preparer-etapes-faites', JSON.stringify(['ancienne-etape']))
    mockUser(true)
    renderPage()

    expect(await screen.findByText(/0 action faite sur/)).toBeInTheDocument()
  })

  it('félicite l’utilisateur quand toutes les actions sont faites', async () => {
    const allIds = PREPARATION_SECTIONS.flatMap((section) => section.steps.map((step) => step.id))
    localStorage.setItem('se-preparer-etapes-faites', JSON.stringify(allIds))
    mockUser(true)
    renderPage()

    expect(await screen.findByText('Votre collectivité est prête')).toBeInTheDocument()
  })

  it('ne félicite pas tant qu’une action reste à faire', async () => {
    mockUser(true)
    renderPage()

    await screen.findByText(/0 action faite sur/)
    expect(screen.queryByText('Votre collectivité est prête')).not.toBeInTheDocument()
  })

  it('ne présente pas de problème d’accessibilité détectable', async () => {
    mockUser(true)
    const { container } = renderPage()
    await screen.findByLabelText(PREPARATION_SECTIONS[0].steps[0].label)

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })
})
