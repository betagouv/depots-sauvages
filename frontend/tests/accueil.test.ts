import { render, screen } from '@testing-library/vue'
import { axe } from 'vitest-axe'
import Accueil from '../pages/accueil.vue'
import { describe, expect, it } from 'vitest'

describe('Page Accueil', () => {
  it('vérifie l’accessibilité de la page d’accueil', async () => {
    const { container } = render(Accueil)

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('affiche la page d’accueil', async () => {
    // Given
    render(Accueil)
    expect(
      await screen.getByRole('heading', {
        level: 1,
        name: /accompagner les collectivités/i,
      })
    ).toBeInTheDocument()
  })
})

