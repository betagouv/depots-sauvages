import { defineStore } from 'pinia'
import { API_URLS, createResource, fetchResource, updateResource } from '../services/api'
import type { Constatation } from '../types/constatation'
import { ConstatantOptions, createEmptyConstatation, fromApiFormat, toApiFormat } from '../types/constatation'

export const useConstatationStore = defineStore('constatation', {
  state: () => ({
    currentId: null as number | null,
    errors: {} as Record<string, string>,
    formData: createEmptyConstatation(),
  }),

  actions: {
    resetStore() {
      this.currentId = null
      this.formData = createEmptyConstatation()
      this.errors = {}
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

      const dataToSend = toApiFormat(data)
      console.log('Sending data to API:', dataToSend)

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
        const standardValues = ConstatantOptions.map(o => o.value).filter(v => v !== 'autre')
        if (formData.constatantRole && !standardValues.includes(formData.constatantRole as any)) {
          formData.constatantRoleAutre = formData.constatantRole
          formData.constatantRole = 'autre'
        }
        
        this.formData = formData
      } catch (error) {
        console.error('Error loading constatation:', error)
        throw error
      }
    },

    validate(): boolean {
      this.errors = {}
      const data = this.formData

      // Localisation
      if (!data.localisationDepot) this.errors.localisationDepot = "L'adresse est obligatoire"
      if (!data.commune)
        this.errors.commune = 'La commune est obligatoire'
      if (data.natureTerrain.length === 0)
        this.errors.natureTerrain = 'La nature du terrain est obligatoire'

      // Constatation
      if (!data.constatantRole)
        this.errors.constatantRole = 'La fonction du constatant est obligatoire'
      if (data.constatantRole === 'autre' && !data.constatantRoleAutre)
        this.errors.constatantRoleAutre = 'Veuillez préciser la fonction'
      
      if (!data.constatantEstUtilisateurConnecte) {
        if (!data.constatantNom)
          this.errors.constatantNom = 'Le nom est obligatoire'
        if (!data.constatantPrenom)
          this.errors.constatantPrenom = 'Le prénom est obligatoire'
        if (!data.constatantCivilite)
          this.errors.constatantCivilite = 'La civilité est obligatoire'
      }

      if (!data.dateConstat) this.errors.dateConstat = 'La date est obligatoire'
      if (!data.heureConstat) this.errors.heureConstat = "L'heure est obligatoire"

      // Description
      if (!data.volumeDepot) this.errors.volumeDepot = 'Le volume est obligatoire'
      if (data.typesDepot.length === 0) this.errors.typesDepot = 'Le type de dépôt est obligatoire'

      // Responsable (Conditional)
      if (data.auteurIdentifie) {
        if (!data.statutAuteur)
          this.errors.statutAuteur = "Le statut de l'auteur présumé est obligatoire"

        const hasInfo = (val: string) =>
          data.informationsAuteur && data.informationsAuteur.includes(val as any)

        if (data.statutAuteur === 'Particulier') {
          if (hasInfo('Nom et prénom')) {
            if (!data.auteurNom) this.errors.auteurNom = 'Le nom de famille est obligatoire'
            if (!data.auteurPrenom) this.errors.auteurPrenom = 'Le prénom est obligatoire'
            if (!data.auteurCivilite) this.errors.auteurCivilite = 'La civilité est obligatoire'
          }
          if (hasInfo('Adresse postale') && !data.auteurAdresse) {
            this.errors.auteurAdresse = "L'adresse postale est obligatoire"
          }
        }

        if (data.statutAuteur === 'Entreprise') {
          if (data.entrepriseFrancaise === null) {
            this.errors.entrepriseFrancaise =
              "Veuillez préciser s'il s'agit d'une entreprise française"
          }
          if (data.entrepriseFrancaise === true) {
            if (!data.auteurSiret) {
              this.errors.auteurSiret = 'Le numéro SIRET est obligatoire pour une entreprise française'
            }
          }
          if (data.entrepriseFrancaise === false) {
            if (!data.auteurNom) {
              this.errors.auteurNom = "Le nom de l'entreprise est obligatoire"
            }
            if (!data.auteurAdresse) {
              this.errors.auteurAdresse = "L'adresse complète de l'entreprise étrangère est obligatoire"
            }
          }
        }

        // Plainte validation logic (replicated from SectionAuteurDepot.vue)
        let showPlainte = false
        if (data.statutAuteur === 'Particulier') {
          const info = data.informationsAuteur || []
          if (info.includes('Aucune' as any) || info.length === 0) {
            showPlainte = true
          } else {
            showPlainte = !hasInfo('Nom et prénom') || !hasInfo('Adresse postale')
          }
        } else if (data.statutAuteur === 'Entreprise') {
          if (data.entrepriseFrancaise === true) {
            showPlainte = !data.auteurSiret
          } else if (data.entrepriseFrancaise === false) {
            showPlainte = !data.auteurAdresse
          } else {
            showPlainte = true
          }
        } else {
          showPlainte = true
        }

        if (showPlainte && !data.plainteEtat) {
          this.errors.plainteEtat = 'Le statut de la plainte est obligatoire'
        }
      } else {
        // Author not identified at all
        if (!data.plainteEtat) this.errors.plainteEtat = 'Le statut de la plainte est obligatoire'
      }

      // Prejudice (Conditional)
      if (data.prejudiceMontantConnu && !data.prejudiceMontant) {
        this.errors.prejudiceMontant = 'Le montant du préjudice est obligatoire'
      }

      // Finalisation
      if (data.ceciEstUnTest === null)
        this.errors.ceciEstUnTest = "Veuillez préciser s'il s'agit d'un test ou d'un cas réel"
      if (!data.accepteAccompagnement)
        this.errors.accepteAccompagnement = "Vous devez accepter d'être recontacté"

      return Object.keys(this.errors).length === 0
    },
  },
})

export type ConstatationStore = ReturnType<typeof useConstatationStore>
