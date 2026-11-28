<template>
  <div class="fr-container--fluid fr-px-2w fr-px-md-4w fr-py-5w">
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <div class="fr-col">
        <h1>Mes procédures</h1>
        <p v-if="userStore.hasTeam && userStore.teamName" class="fr-text--lead fr-text-mention--grey fr-mb-0">
          Procédures partagées de l'organisation : <strong>{{ userStore.teamName }}</strong>
        </p>
        <p v-if="userStore.userDisplayName" class="fr-text--sm fr-text-mention--grey fr-mb-0" :class="{ 'fr-mt-1v': userStore.hasTeam }">
          Connecté en tant que : <strong>{{ userStore.userDisplayName }}</strong>
        </p>
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

        <nav
          v-if="colonnesAffichees.length > 1"
          class="tableau-de-bord-nav fr-mb-2w"
          aria-label="Accès rapide aux étapes"
        >
          <ul class="fr-tags-group">
            <li v-for="colonne in colonnesAffichees" :key="colonne.id">
              <button
                type="button"
                class="fr-tag fr-tag--sm"
                :class="{ 'tableau-de-bord-nav__tag--vide': colonne.items.length === 0 }"
                @click="allerAColonne(colonne.id)"
              >
                {{ colonne.titre }} ({{ colonne.items.length }})
              </button>
            </li>
          </ul>
        </nav>

        <div
          class="tableau-de-bord-conteneur fr-mb-3w"
          :class="{
            'tableau-de-bord-conteneur--ombre-gauche': peutDefilerGauche,
            'tableau-de-bord-conteneur--ombre-droite': peutDefilerDroite,
          }"
        >
          <button
            v-if="peutDefilerGauche"
            type="button"
            class="fr-btn fr-btn--secondary fr-btn--sm fr-icon-arrow-left-s-line tableau-de-bord-conteneur__fleche tableau-de-bord-conteneur__fleche--gauche"
            aria-label="Défiler les colonnes vers la gauche"
            @click="defilerHorizontalement(-1)"
          />

          <div
            ref="tableauRef"
            class="tableau-de-bord"
            :class="{ 'tableau-de-bord--glissement': enGlissement }"
            role="region"
            aria-label="Dossiers rangés par étape"
            tabindex="0"
            @scroll="mettreAJourEtatDefilement"
            @mousedown="demarrerGlissement"
            @wheel="gererMolette"
          >
            <ColonneProcedures
              v-for="colonne in colonnesAffichees"
              :id="colonne.id"
              :key="colonne.id"
              :titre="colonne.titre"
              :items="colonne.items"
              class="tableau-de-bord__colonne"
            />
          </div>

          <button
            v-if="peutDefilerDroite"
            type="button"
            class="fr-btn fr-btn--secondary fr-btn--sm fr-icon-arrow-right-s-line tableau-de-bord-conteneur__fleche tableau-de-bord-conteneur__fleche--droite"
            aria-label="Défiler les colonnes vers la droite"
            @click="defilerHorizontalement(1)"
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
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import AucuneProcedureBox from '../components/procedures/AucuneProcedureBox.vue'
import Chargement from '../components/procedures/Chargement.vue'
import ColonneProcedures from '../components/procedures/ColonneProcedures.vue'
import LoginInvitation from '../components/shared/LoginInvitation.vue'
import { getUserInfo, type UserInfo } from '../services/api'
import { useUserStore } from '../stores/user'
import {
  COLONNES,
  comparerDansColonne,
  correspondRecherche,
  getPlacementProcedure,
  type ColonneId,
} from '../utils/tableau-de-bord'

const userInfo = ref<UserInfo | null>(null)
const procedureStore = useProcedureStore()
const userStore = useUserStore()
const showLoading = ref(true)

const recherche = ref('')
const filtreAuteur = ref('tous')
const afficherClotures = ref(false)

const tableauRef = ref<HTMLElement | null>(null)
const peutDefilerGauche = ref(false)
const peutDefilerDroite = ref(false)
const enGlissement = ref(false)
let glissementDepartX = 0
let glissementDepartScroll = 0
let resizeObserver: ResizeObserver | null = null

const optionsFiltreAuteur = [
  { value: 'tous', text: 'Tous' },
  { value: 'identifie', text: 'Identifié' },
  { value: 'non_identifie', text: 'Non identifié' },
]

const procedures = computed(() => procedureStore.procedures)

const proceduresFiltrees = computed(() =>
  procedures.value
    .filter((p) => correspondRecherche(p, recherche.value))
    .filter((p) => {
      if (filtreAuteur.value === 'identifie') return p.auteur_identifie === true
      if (filtreAuteur.value === 'non_identifie') return p.auteur_identifie !== true
      return true
    })
    .map((procedure) => ({ procedure, placement: getPlacementProcedure(procedure) }))
)

const colonnes = computed(() => {
  const itemsParColonne = COLONNES.reduce(
    (acc, col) => {
      acc[col.id] = []
      return acc
    },
    {} as Record<string, (typeof proceduresFiltrees.value)[number][]>
  )
  for (const item of proceduresFiltrees.value) {
    itemsParColonne[item.placement.colonne]?.push(item)
  }
  return COLONNES.map((colonne) => ({
    ...colonne,
    items: (itemsParColonne[colonne.id] ?? []).sort((a, b) =>
      comparerDansColonne(colonne.id)(a.procedure, b.procedure)
    ),
  }))
})

const nbClotures = computed(
  () => colonnes.value.find((colonne) => colonne.id === 'cloture')?.items.length ?? 0
)

const filtreActif = computed(() => recherche.value.trim() !== '' || filtreAuteur.value !== 'tous')

// Settings are cumulative: switch toggles closed files, including during searches.
// During an active filter/search, only columns with matching items are displayed
// so the found item is immediately visible without scrolling through empty columns.
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
  return `${pluriel(enCours, 'dossier')} en cours${suffixe}`
})

const LARGEUR_DEFILEMENT = 300

const mettreAJourEtatDefilement = () => {
  const el = tableauRef.value
  if (!el) {
    peutDefilerGauche.value = false
    peutDefilerDroite.value = false
    return
  }
  peutDefilerGauche.value = el.scrollLeft > 4
  peutDefilerDroite.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 4
}

const defilerHorizontalement = (direction: -1 | 1) => {
  tableauRef.value?.scrollBy({ left: direction * LARGEUR_DEFILEMENT, behavior: 'smooth' })
}

const allerAColonne = (colonneId: ColonneId) => {
  const cible = tableauRef.value?.querySelector<HTMLElement>(`[data-colonne-id="${colonneId}"]`)
  cible?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
}

const gererDeplacementGlissement = (event: MouseEvent) => {
  if (!enGlissement.value || !tableauRef.value) return
  const deltaX = event.clientX - glissementDepartX
  tableauRef.value.scrollLeft = glissementDepartScroll - deltaX
}

const arreterGlissement = () => {
  if (!enGlissement.value) return
  enGlissement.value = false
  window.removeEventListener('mousemove', gererDeplacementGlissement)
  window.removeEventListener('mouseup', arreterGlissement)
}

const demarrerGlissement = (event: MouseEvent) => {
  if (event.button !== 0 || !tableauRef.value) return
  const cible = event.target as HTMLElement | null
  if (cible?.closest('a, button, input, select, textarea, .carte-procedure')) return
  enGlissement.value = true
  glissementDepartX = event.clientX
  glissementDepartScroll = tableauRef.value.scrollLeft
  window.addEventListener('mousemove', gererDeplacementGlissement)
  window.addEventListener('mouseup', arreterGlissement)
}

const gererMolette = (event: WheelEvent) => {
  const el = tableauRef.value
  if (!el || event.ctrlKey || Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return
  if (el.scrollWidth <= el.clientWidth) return

  const cible = event.target as HTMLElement | null
  const liste = cible?.closest<HTMLElement>('.colonne-procedures__liste')
  if (liste && liste.scrollHeight > liste.clientHeight) return

  const versDroite = event.deltaY > 0
  const peutAvancer = versDroite
    ? el.scrollLeft + el.clientWidth < el.scrollWidth - 1
    : el.scrollLeft > 1
  if (!peutAvancer) return

  event.preventDefault()
  el.scrollLeft += event.deltaY
}

watch(
  [tableauRef, colonnesAffichees],
  async () => {
    await nextTick()
    resizeObserver?.disconnect()
    if (tableauRef.value && typeof ResizeObserver !== 'undefined') {
      resizeObserver = new ResizeObserver(mettreAJourEtatDefilement)
      resizeObserver.observe(tableauRef.value)
    }
    mettreAJourEtatDefilement()
  },
  { flush: 'post' }
)

onBeforeUnmount(() => {
  arreterGlissement()
  resizeObserver?.disconnect()
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
    await nextTick()
    mettreAJourEtatDefilement()
  }
})
</script>

<style scoped>
.tableau-de-bord-nav__tag--vide {
  opacity: 0.65;
}

.tableau-de-bord-conteneur {
  position: relative;
}

.tableau-de-bord-conteneur::before,
.tableau-de-bord-conteneur::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0.75rem;
  width: 2.5rem;
  pointer-events: none;
  z-index: 1;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.tableau-de-bord-conteneur::before {
  left: 0;
  background: linear-gradient(to right, var(--background-default-grey), transparent);
}

.tableau-de-bord-conteneur::after {
  right: 0;
  background: linear-gradient(to left, var(--background-default-grey), transparent);
}

.tableau-de-bord-conteneur--ombre-gauche::before,
.tableau-de-bord-conteneur--ombre-droite::after {
  opacity: 1;
}

.tableau-de-bord-conteneur__fleche {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  background-color: var(--background-default-grey);
  box-shadow: var(--raised-shadow);
}

.tableau-de-bord-conteneur__fleche--gauche {
  left: 0.5rem;
}

.tableau-de-bord-conteneur__fleche--droite {
  right: 0.5rem;
}

.tableau-de-bord {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  height: calc(100vh - 20rem);
  min-height: 24rem;
  max-height: 48rem;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 0.75rem;
  cursor: grab;
  scrollbar-color: var(--border-default-grey) var(--background-alt-grey);
}

.tableau-de-bord--glissement {
  cursor: grabbing;
  user-select: none;
}

.tableau-de-bord__colonne {
  flex: 0 0 17rem;
  min-width: 0;
}

@media (max-width: 47.99em) {
  .tableau-de-bord-conteneur::before,
  .tableau-de-bord-conteneur::after,
  .tableau-de-bord-conteneur__fleche {
    display: none;
  }

  .tableau-de-bord {
    flex-direction: column;
    align-items: stretch;
    height: auto;
    min-height: 0;
    max-height: none;
    overflow-x: visible;
    overflow-y: visible;
    cursor: default;
  }

  .tableau-de-bord__colonne {
    flex: 1 1 auto;
  }
}
</style>
