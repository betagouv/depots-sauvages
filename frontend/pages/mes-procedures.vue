<template>
  <div class="fr-container--fluid fr-px-2w fr-px-md-4w fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <div class="fr-col">
        <h1>Mes procédures</h1>
      </div>
      <div v-if="userInfo?.is_authenticated && procedures.length > 0" class="fr-col-auto">
        <router-link to="/demarrer-constatation" class="fr-btn">
          <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
          Démarrer une constatation
        </router-link>
      </div>
    </div>

    <Chargement v-if="showLoading" message="Récupération de vos procédures..." />

    <div v-else-if="userInfo?.is_authenticated">
      <p v-if="userInfo.first_name && userInfo.last_name" class="fr-text--sm fr-mb-3w">
        Utilisateur connecté :
        <strong>{{ userInfo.first_name }} {{ userInfo.last_name }}</strong>
        <span v-if="userInfo.email"> - {{ userInfo.email }}</span>
      </p>

      <template v-if="procedures.length > 0">
        <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--bottom fr-mb-2w">
          <div class="fr-col-12 fr-col-md-5">
            <DsfrSearchBar
              id="recherche-procedures"
              v-model="recherche"
              label="Rechercher un dossier"
              placeholder="Nom du contrevenant, n° de dossier ou commune"
              button-text="Rechercher"
              @search="(valeur: string) => (recherche = valeur)"
            />
          </div>
          <div class="fr-col-12 fr-col-md-3">
            <DsfrSelect
              select-id="filtre-auteur"
              v-model="filtreAuteur"
              label="Auteur identifié"
              :options="optionsFiltreAuteur"
            />
          </div>
          <div class="fr-col-12 fr-col-md-4">
            <DsfrToggleSwitch
              v-model="afficherClotures"
              input-id="afficher-clotures"
              :label="`Afficher les dossiers clôturés (${nbClotures})`"
            />
          </div>
        </div>

        <p class="fr-text--bold fr-mb-2w" aria-live="polite">
          {{ resumeResultats }}
        </p>

        <div
          class="tableau-de-bord fr-mb-3w"
          role="region"
          aria-label="Dossiers rangés par étape"
          tabindex="0"
        >
          <ColonneProcedures
            v-for="colonne in colonnesAffichees"
            :id="colonne.id"
            :key="colonne.id"
            :titre="colonne.titre"
            :items="colonne.items"
            :afficher-commune="afficherCommune"
            class="tableau-de-bord__colonne"
          />
        </div>
      </template>

      <AucuneProcedureBox v-else class="fr-mt-5w" />
    </div>
    <LoginInvitation v-else />
  </div>
</template>

<script setup lang="ts">
import { useProcedureStore } from '@/stores/procedure'
import { computed, onMounted, ref } from 'vue'
import AucuneProcedureBox from '../components/procedures/AucuneProcedureBox.vue'
import Chargement from '../components/procedures/Chargement.vue'
import ColonneProcedures from '../components/procedures/ColonneProcedures.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import {
  COLONNES,
  comparerProcedures,
  correspondRecherche,
  getPlacementProcedure,
} from '../utils/tableau-de-bord'

const userInfo = ref<UserInfo | null>(null)
const procedureStore = useProcedureStore()
const showLoading = ref(true)

const recherche = ref('')
const filtreAuteur = ref('tous')
const afficherClotures = ref(false)

const optionsFiltreAuteur = [
  { value: 'tous', text: 'Tous' },
  { value: 'identifie', text: 'Identifié' },
  { value: 'non_identifie', text: 'Non identifié' },
]

const procedures = computed(() => procedureStore.procedures)

// La commune n'est utile que si l'utilisateur a des dossiers sur plusieurs communes
const afficherCommune = computed(
  () => new Set(procedures.value.map((p) => p.commune).filter(Boolean)).size > 1
)

const proceduresFiltrees = computed(() =>
  procedures.value
    .filter((p) => correspondRecherche(p, recherche.value))
    .filter((p) => {
      if (filtreAuteur.value === 'identifie') return p.auteur_identifie === true
      if (filtreAuteur.value === 'non_identifie') return p.auteur_identifie !== true
      return true
    })
    .slice()
    .sort(comparerProcedures)
    .map((procedure) => ({ procedure, placement: getPlacementProcedure(procedure) }))
)

const colonnes = computed(() =>
  COLONNES.map((colonne) => ({
    ...colonne,
    items: proceduresFiltrees.value.filter((item) => item.placement.colonne === colonne.id),
  }))
)

const nbClotures = computed(
  () => colonnes.value.find((colonne) => colonne.id === 'cloture')?.items.length ?? 0
)

const filtreActif = computed(() => recherche.value.trim() !== '' || filtreAuteur.value !== 'tous')

// Les réglages se cumulent : l'interrupteur décide si les clôturés sont affichés, y compris
// pendant une recherche. Pendant une recherche ou un filtre, on n'affiche que les colonnes qui
// ont un résultat, pour que le dossier trouvé soit visible sans faire défiler des colonnes vides.
const colonnesAffichees = computed(() =>
  colonnes.value
    .filter((colonne) => colonne.id !== 'cloture' || afficherClotures.value)
    .filter((colonne) => !filtreActif.value || colonne.items.length > 0)
)

const pluriel = (nombre: number, mot: string) => `${nombre} ${mot}${nombre > 1 ? 's' : ''}`

const resumeResultats = computed(() => {
  const enCours = proceduresFiltrees.value.length - nbClotures.value
  const clotures = nbClotures.value
  const suffixe = filtreActif.value ? ' correspondant à votre recherche' : ''

  if (afficherClotures.value) {
    if (filtreActif.value && enCours + clotures === 0) {
      return 'Aucun dossier ne correspond à votre recherche.'
    }
    return `${pluriel(enCours, 'dossier')} en cours, ${pluriel(clotures, 'clôturé')}${suffixe}`
  }

  if (filtreActif.value && enCours === 0) {
    return clotures
      ? `Aucun dossier en cours ne correspond à votre recherche. ${pluriel(clotures, 'dossier')} ${
          clotures > 1 ? 'clôturés correspondent' : 'clôturé correspond'
        } : activez « Afficher les dossiers clôturés » pour ${clotures > 1 ? 'les' : 'le'} voir.`
      : 'Aucun dossier ne correspond à votre recherche.'
  }
  // Le nombre de clôturés masqués figure déjà dans le libellé de l'interrupteur
  return `${pluriel(enCours, 'dossier')} en cours${suffixe}`
})

onMounted(async () => {
  try {
    userInfo.value = await getUserInfo()
    if (userInfo.value?.is_authenticated) {
      await procedureStore.fetchProcedures(true)
    }
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    showLoading.value = false
  }
})
</script>

<style scoped>
.tableau-de-bord {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.tableau-de-bord__colonne {
  flex: 0 0 17rem;
  min-width: 0;
}

/* Sur mobile, les colonnes s'empilent : pas de défilement horizontal */
@media (max-width: 47.99em) {
  .tableau-de-bord {
    flex-direction: column;
    overflow-x: visible;
  }

  .tableau-de-bord__colonne {
    flex: 1 1 auto;
  }
}
</style>
