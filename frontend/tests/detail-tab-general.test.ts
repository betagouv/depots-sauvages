import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import DetailTabGeneral from '../components/backoffice/DetailTabGeneral.vue'

const baseProcedure = {
  id: 42,
  commune: 'Lyon',
  agent: 'Jean Dupont',
  date_constat: '2026-10-01',
  heure_constat: '10:00',
  contact_prenom: '',
  contact_nom: '',
  contact_email: '',
  contact_telephone: '',
  user_email: 'agent@mairie.fr',
  besoin_accompagnement: true,
}

describe('DetailTabGeneral', () => {
  it("doit afficher l'email du compte et « Non renseigné » si le téléphone est vide", () => {
    render(DetailTabGeneral, { props: { procedure: baseProcedure } })

    expect(screen.getByTestId('contact-email')).toHaveTextContent('agent@mairie.fr')
    expect(screen.getByRole('link', { name: 'agent@mairie.fr' })).toHaveAttribute(
      'href',
      'mailto:agent@mairie.fr'
    )
    expect(screen.getByTestId('contact-telephone')).toHaveTextContent('Non renseigné')
  })

  it('doit afficher le téléphone quand il est renseigné', () => {
    render(DetailTabGeneral, {
      props: { procedure: { ...baseProcedure, contact_telephone: '0612345678' } },
    })

    expect(screen.getByRole('link', { name: '0612345678' })).toHaveAttribute(
      'href',
      'tel:0612345678'
    )
  })

  it("doit afficher « Non renseigné » si aucun email n'est disponible", () => {
    render(DetailTabGeneral, { props: { procedure: { ...baseProcedure, user_email: '' } } })

    expect(screen.getByTestId('contact-email')).toHaveTextContent('Non renseigné')
  })
})
