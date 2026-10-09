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
          <div class="fr-col-12 fr-col-md-6">
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

        <DsfrButton
          v-if="nbClotures > 0 && !filtreActif"
          secondary
          :aria-expanded="afficherClotures ? 'true' : 'false'"
          @click="afficherClotures = !afficherClotures"
        >
          {{
            afficherClotures
              ? 'Masquer les dossiers clôturés'
              : `Afficher les ${nbClotures} dossier${nbClotures > 1 ? 's' : ''} clôturé${nbClotures > 1 ? 's' : ''}`
          }}
        </DsfrButton>
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

// Pendant une recherche, on n'affiche que les colonnes qui ont un résultat (clôturés compris),
// pour que le dossier trouvé soit visible sans faire défiler des colonnes vides.
const colonnesAffichees = computed(() =>
  filtreActif.value
    ? colonnes.value.filter((colonne) => colonne.items.length > 0)
    : colonnes.value.filter((colonne) => colonne.id !== 'cloture' || afficherClotures.value)
)

const resumeResultats = computed(() => {
  const total = proceduresFiltrees.value.length
  const enCours = total - nbClotures.value
  const filtre = filtreActif.value
  if (filtre && total === 0) return 'Aucun dossier ne correspond à votre recherche.'
  return `${enCours} dossier${enCours > 1 ? 's' : ''} en cours${
    nbClotures.value ? `, ${nbClotures.value} clôturé${nbClotures.value > 1 ? 's' : ''}` : ''
  }${filtre ? ' correspondant à votre recherche' : ''}`
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
