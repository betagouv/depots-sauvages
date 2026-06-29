import { defineStore } from 'pinia'
import { API_URLS, createResource, fetchResource, updateResource } from '../services/api'
import type { Constatation } from '../types/constatation'
import {
  ConstatantOptions,
  createEmptyConstatation,
  fromApiFormat,
  toApiFormat,
} from '../types/constatation'

import {
  toNumOrNull,
  validateRequiredPositiveNumber,
  validateOptionalPositiveNumber,
} from '../utils/validation'

export const useConstatationStore = defineStore('constatation', {
  state: () => ({
    currentId: null as number | null,
    errors: {} as Record<string, string>,
    formData: createEmptyConstatation(),
    hasBeenSubmitted: false,
  }),

  actions: {
    resetStore() {
      this.currentId = null
      this.formData = createEmptyConstatation()
      this.errors = {}
      this.hasBeenSubmitted = false
    },

    clearFieldError(field: string) {
      delete this.errors[field]
    },

    updateBooleanField(field: keyof Constatation, value: string) {
      if (typeof this.formData[field] === 'boolean') {
        this.formData[field] = (value === 'oui') as any
      }
    },

    async saveFormData() {
      const data = { ...this.formData }
      if (data.constatantRole === 'autre') {
        data.constatantRole = data.constatantRoleAutre as any
      }

      if (data.plainteEtat === 'Aucune') {
        data.prejudiceMontantConnu = false
        data.prejudiceMontant = null as any
        data.prejudiceNombrePersonnes = null as any
        data.prejudiceNombreHeures = null as any
        data.prejudiceNombreVehicules = null as any
        data.prejudiceKilometrage = null as any
        data.prejudiceAutresCouts = null as any
      } else {
        if (data.prejudiceMontantConnu === true) {
          data.prejudiceMontant = toNumOrNull(data.prejudiceMontant) as any
          data.prejudiceNombrePersonnes = null as any
          data.prejudiceNombreHeures = null as any
          data.prejudiceNombreVehicules = null as any
          data.prejudiceKilometrage = null as any
          data.prejudiceAutresCouts = null as any
        } else {
          data.prejudiceMontant = null as any
          data.prejudiceNombrePersonnes = (toNumOrNull(data.prejudiceNombrePersonnes) ?? 0) as any
          data.prejudiceNombreHeures = (toNumOrNull(data.prejudiceNombreHeures) ?? 0) as any
          data.prejudiceNombreVehicules = (toNumOrNull(data.prejudiceNombreVehicules) ?? 0) as any
          data.prejudiceKilometrage = (toNumOrNull(data.prejudiceKilometrage) ?? 0) as any
          data.prejudiceAutresCouts = (toNumOrNull(data.prejudiceAutresCouts) ?? 0) as any
        }
      }

      const dataToSend = toApiFormat(data)

      if (this.currentId) {
        return await updateResource(`${API_URLS.constatations}${this.currentId}/`, dataToSend)
      } else {
        const data = await createResource(API_URLS.constatations, dataToSend)
        this.currentId = data.id
        return data
      }
    },

    async loadConstatation(id: number) {
      try {
        const data = await fetchResource(`${API_URLS.constatations}${id}/`)
        this.currentId = id
        const formData = fromApiFormat(data)

        // Handle 'autre' function on load
        const standardValues = ConstatantOptions.map((o) => o.value).filter((v) => v !== 'autre')
        if (formData.constatantRole && !standardValues.includes(formData.constatantRole as any)) {
          formData.constatantRoleAutre = formData.constatantRole
          formData.constatantRole = 'autre'
        }

        // Default null prejudice values to 0
        formData.prejudiceNombrePersonnes = formData.prejudiceNombrePersonnes ?? 0
        formData.prejudiceNombreHeures = formData.prejudiceNombreHeures ?? 0
        formData.prejudiceNombreVehicules = formData.prejudiceNombreVehicules ?? 0
        formData.prejudiceKilometrage = formData.prejudiceKilometrage ?? 0
        formData.prejudiceAutresCouts = formData.prejudiceAutresCouts ?? 0

        this.formData = formData
      } catch (error) {
        console.error('Error loading constatation:', error)
        throw error
      }
    },

    validate(onlyExisting = false): boolean {
      this.hasBeenSubmitted = true
      const previousErrors = { ...this.errors }
      this.errors = {}
      const data = this.formData

      // Localisation
      if (!data.localisationDepot) this.errors.localisationDepot = "L'adresse est obligatoire"
      if (!data.commune) this.errors.commune = 'La commune est obligatoire'
      const natureTerrain = data.natureTerrain || []
      if (natureTerrain.length === 0)
        this.errors.natureTerrain = 'La nature du terrain est obligatoire'
      if (natureTerrain.includes('Terrain privé') && !data.proprietaireTerrainPrive) {
        this.errors.proprietaireTerrainPrive = 'La situation du propriétaire est obligatoire'
      }

      // Constatation
      if (!data.constatantRole)
        this.errors.constatantRole = 'La fonction du constatant est obligatoire'
      if (data.constatantRole === 'autre' && !data.constatantRoleAutre)
        this.errors.constatantRoleAutre = 'Veuillez préciser la fonction'

      if (!data.constatantEstUtilisateurConnecte) {
        if (!data.constatantNom) this.errors.constatantNom = 'Le nom est obligatoire'
        if (!data.constatantPrenom) this.errors.constatantPrenom = 'Le prénom est obligatoire'
      }

      if (!data.dateConstat) this.errors.dateConstat = 'La date est obligatoire'
      if (!data.heureConstat) this.errors.heureConstat = "L'heure est obligatoire"

      // Description
      if (!data.volumeDepot) this.errors.volumeDepot = 'Le volume est obligatoire'

      const typesDepot = data.typesDepot || []
      if (typesDepot.length === 0) this.errors.typesDepot = 'Le type de dépôt est obligatoire'
      if (!data.precisionsDepot)
        this.errors.precisionsDepot = 'La description du dépôt est obligatoire'

      // Responsable (Conditional)
      if (data.auteurIdentifie === null) {
        this.errors.auteurIdentifie = "Veuillez préciser si l'auteur présumé est identifié"
      } else if (data.auteurIdentifie === true) {
        if (!data.statutAuteur)
          this.errors.statutAuteur = "Le statut de l'auteur présumé est obligatoire"

        const hasInfo = (val: string) =>
          data.informationsAuteur && data.informationsAuteur.includes(val as any)

        if (data.statutAuteur === 'particulier') {
          const informationsAuteur = data.informationsAuteur || []
          if (informationsAuteur.length === 0) {
            this.errors.informationsAuteur = 'Veuillez cocher au moins une option'
          }
          if (hasInfo('Nom et prénom')) {
            if (!data.auteurNom) this.errors.auteurNom = 'Le nom de famille est obligatoire'
            if (!data.auteurPrenom) this.errors.auteurPrenom = 'Le prénom est obligatoire'
            if (!data.auteurCivilite) this.errors.auteurCivilite = 'La civilité est obligatoire'
          }
          if (hasInfo('Adresse postale') && !data.auteurAdresse) {
            this.errors.auteurAdresse = "L'adresse postale est obligatoire"
          }
        }

        if (data.statutAuteur === 'entreprise') {
          if (data.entrepriseFrancaise === null) {
            this.errors.entrepriseFrancaise =
              "Veuillez préciser s'il s'agit d'une entreprise française"
          }
          if (data.entrepriseFrancaise === true) {
            if (!data.auteurSiret) {
              this.errors.auteurSiret =
                'Le numéro SIRET est obligatoire pour une entreprise française'
            }
            if (!data.auteurNom) {
              this.errors.auteurNom = "Le nom de l'entreprise est obligatoire"
            }
            if (!data.auteurAdresse) {
              this.errors.auteurAdresse = "L'adresse de l'entreprise est obligatoire"
            }
          }
          if (data.entrepriseFrancaise === false) {
            if (!data.auteurNom) {
              this.errors.auteurNom = "Le nom de l'entreprise est obligatoire"
            }
            if (!data.auteurAdresse) {
              this.errors.auteurAdresse =
                "L'adresse complète de l'entreprise étrangère est obligatoire"
            }
          }
        }

        // Plainte validation logic (replicated from SectionAuteurDepot.vue)
        let showPlainte = false
        if (data.statutAuteur === 'particulier') {
          const info = data.informationsAuteur || []
          if (info.length === 0) {
            showPlainte = false
          } else if (
            info.includes('Nom et prénom' as any) &&
            info.includes('Adresse postale' as any)
          ) {
            showPlainte = false
          } else {
            showPlainte = true
          }
        } else if (data.statutAuteur === 'entreprise') {
          if (data.entrepriseFrancaise === true) {
            showPlainte = !data.auteurSiret || !data.auteurNom || !data.auteurAdresse
          } else if (data.entrepriseFrancaise === false) {
            showPlainte = !data.auteurAdresse || !data.auteurNom
          } else {
            showPlainte = false
          }
        }

        if (showPlainte && !data.plainteEtat) {
          this.errors.plainteEtat = 'Le statut de la plainte est obligatoire'
        }
      } else if (data.auteurIdentifie === false) {
        // Author not identified at all
        if (!data.plainteEtat) this.errors.plainteEtat = 'Le statut de la plainte est obligatoire'
      }

      if (data.auteurIdentifie !== null) {
        const indicesDisponibles = data.indicesDisponibles || []
        if (indicesDisponibles.length === 0) {
          this.errors.indicesDisponibles = 'Veuillez cocher au moins une option'
        }
        if (!data.precisionsIndices) {
          this.errors.precisionsIndices = "Veuillez ajouter les éléments d'identification"
        }
      }

      // Prejudice (Conditional)
      if (['Déposée', 'Sera déposée'].includes(data.plainteEtat)) {
        if (data.prejudiceMontantConnu === null) {
          this.errors.prejudiceMontantConnu =
            'Veuillez préciser si le montant du préjudice est connu'
        } else if (data.prejudiceMontantConnu === true) {
          validateRequiredPositiveNumber(
            data.prejudiceMontant,
            'prejudiceMontant',
            this.errors,
            'Le montant du préjudice est obligatoire'
          )
        } else if (data.prejudiceMontantConnu === false) {
          validateOptionalPositiveNumber(
            data.prejudiceNombrePersonnes,
            'prejudiceNombrePersonnes',
            this.errors
          )
          validateOptionalPositiveNumber(
            data.prejudiceNombreHeures,
            'prejudiceNombreHeures',
            this.errors
          )
          validateOptionalPositiveNumber(
            data.prejudiceNombreVehicules,
            'prejudiceNombreVehicules',
            this.errors
          )
          validateOptionalPositiveNumber(
            data.prejudiceKilometrage,
            'prejudiceKilometrage',
            this.errors
          )
          validateOptionalPositiveNumber(
            data.prejudiceAutresCouts,
            'prejudiceAutresCouts',
            this.errors
          )
        }
      }

      // Finalisation
      if (data.ceciEstUnTest === null)
        this.errors.ceciEstUnTest = "Veuillez préciser s'il s'agit d'un test ou d'un cas réel"
      if (!data.accepteAccompagnement)
        this.errors.accepteAccompagnement = "Vous devez accepter d'être recontacté"

      if (onlyExisting) {
        const filteredErrors: Record<string, string> = {}
        for (const key in this.errors) {
          if (previousErrors[key]) {
            filteredErrors[key] = this.errors[key]
          }
        }
        this.errors = filteredErrors
      }

      return Object.keys(this.errors).length === 0
    },
  },
})

export type ConstatationStore = ReturnType<typeof useConstatationStore>
