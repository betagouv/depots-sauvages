import { defineStore } from 'pinia'

export const useBackofficeStore = defineStore('backoffice', {
  state: () => ({
    assignees: ['Anthony', 'Jennifer', 'Non assigné'],
    procedures: [
      {
        id: 512,
        commune: 'Montmédy',
        date_constat: '2026-06-27',
        constatant_role: 'Secrétaire de mairie',
        volume_depot: '3 m³',
        nature_terrain: ['Terrain public'],
        ceci_est_un_test: false,
        user_email: 'dgs@montmedy.fr',
        agent: 'dgs@montmedy.fr',
        auteur_identifie: false,
        suivi_procedure: {
          etape_en_cours: 1,
          preuves_fournies: false,
          constatation_signee: false,
          lettre_signe: false,
          identification_reussie: null,
          observations_internes: '',
          charge_deploiement: 'Non assigné',
          date_assigned: null,
          anomalie: '',
        },
      },
      {
        id: 511,
        commune: 'Fécamp',
        date_constat: '2026-05-27',
        constatant_role: 'Gendarme',
        volume_depot: '10 m³',
        nature_terrain: ['Terrain privé'],
        ceci_est_un_test: false,
        user_email: 'alexis.dereumaux@gendarmerie.interieur.gouv.fr',
        agent: 'alexis.dereumaux@gendarmerie.interieur.gouv.fr',
        auteur_identifie: true,
        suivi_procedure: {
          etape_en_cours: 1,
          preuves_fournies: true,
          constatation_signee: true,
          lettre_signe: false,
          identification_reussie: false,
          observations_internes: "En attente des éléments d'enquête de la gendarmerie.",
          charge_deploiement: 'Jennifer',
          date_assigned: '2026-05-28',
          anomalie: '',
        },
      },
      {
        id: 510,
        commune: 'Civray',
        date_constat: '2026-05-29',
        constatant_role: 'Garde champêtre',
        volume_depot: '1 m³',
        nature_terrain: ['Terrain public'],
        ceci_est_un_test: false,
        user_email: 'police@civray.fr',
        agent: 'police@civray.fr',
        auteur_identifie: true,
        suivi_procedure: {
          etape_en_cours: 3,
          preuves_fournies: true,
          constatation_signee: false,
          lettre_signe: true,
          identification_reussie: true,
          observations_internes: 'Relancé le 28/05 — en attente retour mairie de Gardanne',
          charge_deploiement: 'Anthony',
          date_assigned: '2026-06-01',
          anomalie: 'Lettre signée, rapport non signé',
        },
      },
      {
        id: 509,
        commune: 'Soissons',
        date_constat: '2026-06-30',
        constatant_role: 'Policier municipal',
        volume_depot: '5 m³',
        nature_terrain: ['Terrain public'],
        ceci_est_un_test: false,
        user_email: 'g.droineau@ville-soissons.fr',
        agent: 'g.droineau@ville-soissons.fr',
        auteur_identifie: true,
        suivi_procedure: {
          etape_en_cours: 2,
          preuves_fournies: true,
          constatation_signee: true,
          lettre_signe: false,
          identification_reussie: true,
          observations_internes: "Lettre d'information en cours de préparation.",
          charge_deploiement: 'Anthony',
          date_assigned: '2026-06-30',
          anomalie: '',
        },
      },
    ],
    // OKR and Weekly stats targets
    stats: {
      totalActive: 84,
      actionRequired: 12,
      arWaiting: 18,
      decisionToTake: 7,
      closedThisMonth: 23,

      // Weekly meeting tracking table (from stats-sample.md)
      weeklySnapshots: [
        {
          date: '02/06',
          procedures: 345,
          activeCollectivities: 180,
          finesCount: 42,
          amountFines: 21180.34,
          cleanedCount: 17,
          cleanedVolume: 548,
          webinarsCount: 570,
        },
        {
          date: '09/06',
          procedures: 384,
          activeCollectivities: 189,
          finesCount: 43,
          amountFines: 21330.34,
          cleanedCount: 17,
          cleanedVolume: 548,
          webinarsCount: 608,
        },
        {
          date: '16/06',
          procedures: 433,
          activeCollectivities: 196,
          finesCount: 49,
          amountFines: 25530.34,
          cleanedCount: 18,
          cleanedVolume: 548,
          webinarsCount: 648,
        },
        {
          date: '23/06',
          procedures: 491,
          activeCollectivities: 245,
          finesCount: 50,
          amountFines: 26280.0,
          cleanedCount: 19,
          cleanedVolume: 558,
          webinarsCount: 691,
        },
        {
          date: '30/06',
          procedures: 545,
          activeCollectivities: 264,
          finesCount: 50,
          amountFines: 26280.0,
          cleanedCount: 19,
          cleanedVolume: 558,
          webinarsCount: 721,
        },
      ],

      // OKR S2 2026 tracking metrics (from okr-2026.md)
      okrs: {
        kr1_1: {
          label: 'Procédures administratives engagées (LI)',
          current: 545,
          target: 1300,
          unit: 'procédures',
        },
        kr1_2: {
          label: 'Taux de complétion des constatations',
          current: 92,
          target: 90,
          unit: '%',
        },
        kr1_3: {
          label: 'Décision validée après 1 mois (Sanction/Abandon)',
          current: 48,
          target: 50,
          unit: '%',
        },
        kr2_1: {
          label: 'Participants aux webinaires (cumul)',
          current: 721,
          target: 2000,
          unit: 'participants',
        },
        kr2_2: {
          label: 'Communes actives (LI lancée 6 derniers mois)',
          current: 264,
          target: 500,
          unit: 'communes',
        },
        kr3_1: { label: 'NPS Moyen Utilisateurs', current: 42, target: 40, unit: 'NPS' },
        kr3_2: {
          label: "Taux de rétention des communes (>1 mois d'intervalle)",
          current: 28,
          target: 33,
          unit: '%',
        },
      },

      // Chart line graph history
      history: [
        { date: 'Janvier', total: 180, success: 50, abandoned: 15 },
        { date: 'Février', total: 240, success: 75, abandoned: 20 },
        { date: 'Mars', total: 310, success: 98, abandoned: 28 },
        { date: 'Avril', total: 390, success: 120, abandoned: 32 },
        { date: 'Mai', total: 470, success: 150, abandoned: 45 },
        { date: 'Juin', total: 545, success: 180, abandoned: 50 },
      ],
    },
  }),
  getters: {
    getProcedureById: (state) => (id) => {
      return state.procedures.find((p) => p.id === parseInt(id))
    },
    proceduresRequiringAction: (state) => {
      return state.procedures.filter((p) => {
        const status = p.suivi_procedure.etape_en_cours
        return status < 5
      })
    },
  },
  actions: {
    assignCharge(procedureId, chargeName) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.charge_deploiement = chargeName
        procedure.suivi_procedure.date_assigned =
          chargeName === 'Non assigné' ? null : new Date().toISOString().split('T')[0]
      }
    },
    updateNotes(procedureId, notes) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.observations_internes = notes
      }
    },
    toggleSuiviField(procedureId, field) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        if (field === 'preuves') {
          procedure.suivi_procedure.preuves_fournies = !procedure.suivi_procedure.preuves_fournies
        } else if (field === 'rapportSigne') {
          procedure.suivi_procedure.constatation_signee =
            !procedure.suivi_procedure.constatation_signee
        } else if (field === 'lettreSignee') {
          procedure.suivi_procedure.lettre_signe = !procedure.suivi_procedure.lettre_signe
        } else if (field === 'auteurIdentifie') {
          const current = procedure.suivi_procedure.identification_reussie
          procedure.suivi_procedure.identification_reussie =
            current === true ? false : current === false ? null : true
        }
      }
    },
  },
})
