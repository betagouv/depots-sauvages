import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/vue'
import Metadata from '../components/procedures/Metadata.vue'

describe('Composant Metadata', () => {
  it('affiche la date et l’auteur de création du constat initial', () => {
    render(Metadata, {
      props: {
        procedure: {
          id: 201,
          date_creation: '2026-11-17T09:37:00Z',
          created_by_name: 'Jean DUPONT',
          date_constat: '2026-11-17',
          heure_constat: '12:59',
          localisation_depot: 'Chemin de la Motte',
        },
      },
    })

    expect(screen.getByText(/Constat initial créé le/i)).toBeInTheDocument()
    expect(screen.getByText('Jean DUPONT')).toBeInTheDocument()
    expect(screen.getByText('Chemin de la Motte')).toBeInTheDocument()
    expect(screen.queryByText(/Constatation modifiée le/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/Dernière action de suivi le/i)).not.toBeInTheDocument()
  })

  it('affiche la modification de la constatation si elle diffère de la création', () => {
    render(Metadata, {
      props: {
        procedure: {
          id: 201,
          date_creation: '2026-11-17T09:37:00Z',
          date_modification: '2026-11-17T11:15:00Z',
          created_by_name: 'Jean DUPONT',
          updated_by_name: 'Alice MARTIN',
        },
      },
    })

    expect(screen.getByText(/Constat initial créé le/i)).toBeInTheDocument()
    expect(screen.getByText('Jean DUPONT')).toBeInTheDocument()
    expect(screen.getByText(/Constatation modifiée le/i)).toBeInTheDocument()
    expect(screen.getByText('Alice MARTIN')).toBeInTheDocument()
  })

  it('affiche la dernière action de suivi avec son auteur si le suivi a été modifié ultérieurement', () => {
    render(Metadata, {
      props: {
        procedure: {
          id: 201,
          date_creation: '2026-11-17T09:37:00Z',
          created_by_name: 'Jean DUPONT',
        },
        suivi: {
          modified: '2026-11-17T16:04:00Z',
          updated_by_name: 'Paul DURAND',
        },
      },
    })

    expect(screen.getByText(/Constat initial créé le/i)).toBeInTheDocument()
    expect(screen.getByText('Jean DUPONT')).toBeInTheDocument()
    expect(screen.getByText(/Dernière action de suivi le/i)).toBeInTheDocument()
    expect(screen.getByText('Paul DURAND')).toBeInTheDocument()
  })
})
