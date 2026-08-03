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
          DsfrAlert: true,
          RouterLink: {
            props: ['to'],
            template: `<a :href="to"><slot /></a>`,
          },
        },
      },
    })

    expect(screen.getByText('Constatation enregistrée !')).toBeInTheDocument()
    expect(
      screen.getByText(/Vos documents de procédure ont été pré-remplis automatiquement/)
    ).toBeInTheDocument()
    expect(
      screen.getByText('Accéder aux documents sur mon suivi de procédure')
    ).toBeInTheDocument()

    const modifyLink = screen.getByText('Modifier la constatation')
    expect(modifyLink).toBeInTheDocument()
    expect(modifyLink.closest('a')).toHaveAttribute('href', '/constatation/42')
  })
})
