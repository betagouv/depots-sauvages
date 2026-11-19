import { render } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import NotFoundPage from '../pages/not-found.vue'

describe('Page 404 Not Found', () => {
  it('affiche le message d’erreur DSFR et les boutons de redirection', async () => {
    ;(window as any)._paq = []
    const { findByText } = render(NotFoundPage, {
      global: {
        stubs: {
          RouterLink: {
            props: ['to'],
            template: '<a :href="to"><slot /></a>',
          },
        },
      },
    })

    await findByText('Page non trouvée')
    await findByText('Erreur 404')
    await findByText('Mes procédures')
    await findByText("Page d'accueil")

    expect((window as any)._paq).toContainEqual([
      'setDocumentTitle',
      'Page non trouvée (404) - Stop Dépôt Sauvage',
    ])
  })
})
