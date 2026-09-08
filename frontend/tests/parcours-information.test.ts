import '@testing-library/jest-dom'
import { fireEvent, render, screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import { defineComponent } from 'vue'
import ClarteFeedback from '../components/shared/ClarteFeedback.vue'
import { useScrollDepth } from '../composables/useScrollDepth'

const trackEvent = vi.fn()
vi.mock('@/services/matomo', () => ({
  trackEvent: (...args: unknown[]) => trackEvent(...args),
}))

const routerLinkStub = {
  props: ['to'],
  template: `<a :href="to"><slot /></a>`,
}

/** Pretends the document is `height` pixels tall and the viewport 800px. */
const setPageHeight = (height: number) => {
  Object.defineProperty(document.documentElement, 'scrollHeight', {
    value: height,
    configurable: true,
  })
  Object.defineProperty(window, 'innerHeight', { value: 800, configurable: true })
}

const scrollTo = async (y: number) => {
  Object.defineProperty(window, 'scrollY', { value: y, configurable: true })
  window.dispatchEvent(new Event('scroll'))
  // The listener defers its work to requestAnimationFrame.
  await new Promise((resolve) => requestAnimationFrame(() => setTimeout(resolve, 0)))
}

const Host = defineComponent({
  setup() {
    useScrollDepth('Comprendre la procédure')
  },
  template: '<div />',
})

describe('Mesure du parcours information (KR2.3)', () => {
  beforeEach(() => {
    trackEvent.mockClear()
  })

  describe('useScrollDepth', () => {
    it("signale l'entrée dans le parcours dès l'affichage", () => {
      setPageHeight(4000)
      render(Host)

      expect(trackEvent).toHaveBeenCalledWith(
        'Parcours information',
        'Entrée parcours',
        'Comprendre la procédure'
      )
    })

    it('émet chaque palier de lecture une seule fois', async () => {
      setPageHeight(4000)
      render(Host)
      trackEvent.mockClear()

      // 2000 + 800 = 2800 / 4000 = 70 % : les paliers 25 et 50 sont franchis.
      await scrollTo(2000)
      // Rejouer le même scroll ne doit rien réémettre.
      await scrollTo(2000)

      const actions = trackEvent.mock.calls.map((call) => call[1])
      expect(actions).toEqual(['Lecture 25%', 'Lecture 50%'])
    })

    it('compte la lecture comme aboutie au-delà de 75 %', async () => {
      setPageHeight(4000)
      render(Host)
      trackEvent.mockClear()

      await scrollTo(3200)

      const actions = trackEvent.mock.calls.map((call) => call[1])
      expect(actions).toContain('Lecture 75%')
      expect(actions).toContain('Lecture 100%')
    })

    it('considère une page plus courte que la fenêtre comme entièrement lue', () => {
      setPageHeight(500)
      render(Host)

      const actions = trackEvent.mock.calls.map((call) => call[1])
      expect(actions).toContain('Lecture 100%')
    })
  })

  describe('ClarteFeedback', () => {
    const renderFeedback = () =>
      render(ClarteFeedback, {
        props: { pageName: 'Comprendre la procédure' },
        global: { stubs: { RouterLink: routerLinkStub } },
      })

    it('doit être accessible (A11y)', async () => {
      const { container } = renderFeedback()
      const results = await axe(container)
      expect(results.violations).toEqual([])
    })

    it('remonte la réponse à Matomo', async () => {
      renderFeedback()

      await fireEvent.click(screen.getByRole('button', { name: /Oui, c’est clair/ }))

      expect(trackEvent).toHaveBeenCalledWith(
        'Parcours information',
        'Clarté - Oui',
        'Comprendre la procédure'
      )
    })

    it('propose webinaire et contact quand la procédure reste floue', async () => {
      renderFeedback()

      await fireEvent.click(screen.getByRole('button', { name: 'En partie' }))

      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(screen.getByRole('link', { name: /webinaire/i })).toBeInTheDocument()
      expect(screen.getByRole('link', { name: /question à l'équipe/i })).toBeInTheDocument()
    })

    it('ne propose pas de rattrapage quand la réponse est positive', async () => {
      renderFeedback()

      await fireEvent.click(screen.getByRole('button', { name: /Oui, c’est clair/ }))

      expect(screen.queryByRole('link', { name: /webinaire/i })).not.toBeInTheDocument()
    })
  })
})
