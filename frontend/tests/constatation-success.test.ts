import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import ConstatationSuccess from '../components/forms/constatation/ConstatationSuccess.vue'

describe('ConstatationSuccess.vue', () => {
  it('doit afficher le message de succès et le bouton de suivi', () => {
    render(ConstatationSuccess, {
      props: {
        constatationId: 42,
      },
      global: {
        stubs: {
          DsfrButton: {
            template: `<button @click="$emit('click')"><slot /><span class="label">{{ label }}</span></button>`,
            props: ['label'],
          },
          DsfrCallout: true,
          RouterLink: {
            props: ['to'],
            template: `<a :href="to"><slot /></a>`,
          },
        },
      },
    })

    expect(screen.getByText('Constatation enregistrée !')).toBeInTheDocument()
    expect(
      screen.getByText(/La constatation du dépôt sauvage a bien été enregistrée/)
    ).toBeInTheDocument()
    expect(
      screen.getByText('Consulter les prochaines étapes sur mon suivi de procédure')
    ).toBeInTheDocument()

    const modifyLink = screen.getByText('Modifier la constatation')
    expect(modifyLink).toBeInTheDocument()
    expect(modifyLink.closest('a')).toHaveAttribute('href', '/constatation/42')
  })
})
