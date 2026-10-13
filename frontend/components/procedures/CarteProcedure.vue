<template>
  <!--
    Carte DSFR entièrement cliquable (fr-enlarge-link) : un seul lien, sur le nom, qui couvre
    toute la carte. La flèche en bas à droite est fournie par le DSFR ; le verbe d'action
    n'apparaît à côté que quand l'utilisateur doit agir.
  -->
  <div class="carte-procedure fr-card fr-card--sm fr-enlarge-link">
    <div class="fr-card__body">
      <div class="fr-card__content">
        <h3 class="fr-card__title">
          <router-link :to="placement.action.to">
            <span
              :class="['carte-procedure__icone', identite.icone, 'fr-icon--sm', 'fr-mr-1v']"
              aria-hidden="true"
            ></span>
            <span v-if="identite.libelle" class="fr-sr-only">{{ identite.libelle }} :</span
            >{{ ` ${titre}` }}<span class="fr-sr-only">{{ complementLien }}</span>
          </router-link>
        </h3>

        <div class="fr-card__desc carte-procedure__desc">
          <ul v-if="procedure.is_draft" class="fr-tags-group fr-mb-0">
            <li><p class="fr-tag fr-tag--sm">Brouillon</p></li>
          </ul>
          <p class="fr-text--xs fr-text-mention--grey fr-mb-0">
            n°{{ procedure.id
            }}<template v-if="procedure.date_constat"> · Constat du {{ dateConstat }}</template>
          </p>
          <p v-if="lieu" class="carte-procedure__lieu fr-text--xs fr-text-mention--grey fr-mb-0">
            Dépôt : {{ lieu }}
          </p>

          <p v-if="placement.info" class="fr-text--sm fr-mt-1w fr-mb-0">
            <span class="fr-icon-time-line fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
            {{ placement.info }}
          </p>

          <ul v-if="placement.alertes.length" class="carte-procedure__alertes fr-text--sm fr-mt-1w">
            <li v-for="alerte in placement.alertes" :key="alerte" class="fr-text-default--warning">
              <span class="fr-icon-warning-fill fr-icon--sm fr-mr-1v" aria-hidden="true"></span>
              <span class="fr-sr-only">Attention : </span>{{ alerte }}
            </li>
          </ul>

          <p v-if="placement.issue" class="fr-mt-1w fr-mb-0">
            <span class="fr-tag fr-tag--sm">Issue : {{ placement.issue }}</span>
          </p>
        </div>

        <!-- Déjà lu par les lecteurs d'écran dans le nom du lien : masqué pour eux ici -->
        <div v-if="placement.action.label" class="fr-card__end" aria-hidden="true">
          <p class="carte-procedure__verbe fr-text--sm fr-text--bold fr-mb-0">
            {{ placement.action.label }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import dayjs from 'dayjs'
import { computed } from 'vue'
import type { ProcedureOverview } from '../../services/api'
import { getNomContrevenant, type PlacementProcedure } from '../../utils/tableau-de-bord'

const props = defineProps<{
  procedure: ProcedureOverview
  placement: PlacementProcedure
}>()

const nom = computed(() => getNomContrevenant(props.procedure))

/** Le titre est toujours une personne : son nom, ou « Auteur non identifié » */
const titre = computed(() => {
  if (!props.procedure.auteur_identifie) return 'Auteur non identifié'
  return nom.value || 'Nom à compléter'
})

/** Icône d'identité, doublée d'un texte pour les lecteurs d'écran */
const identite = computed(() => {
  if (!props.procedure.auteur_identifie) {
    // Le titre dit déjà « Auteur non identifié »
    return { icone: 'fr-icon-user-search-line', libelle: '' }
  }
  if (props.procedure.statut_auteur === 'entreprise') {
    return { icone: 'fr-icon-building-line', libelle: 'Entreprise' }
  }
  return { icone: 'fr-icon-user-line', libelle: 'Particulier' }
})

/** Fin du nom du lien pour les lecteurs d'écran : n° du dossier et verbe d'action éventuel */
const complementLien = computed(() => {
  const verbe = props.placement.action.label
  return `, dossier n°${props.procedure.id}${verbe ? `. ${verbe}` : ''}`
})

const dateConstat = computed(() => dayjs(props.procedure.date_constat).format('DD/MM/YYYY'))

/** « lieu du dépôt – commune » : la commune à la fin, la plupart des comptes n'en ont qu'une */
const lieu = computed(() =>
  [props.procedure.localisation_depot, props.procedure.commune]
    .map((part) => (part ?? '').trim())
    .filter(Boolean)
    .join(' – ')
)
</script>

<style scoped>
.carte-procedure {
  /* Ancre les textes réservés aux lecteurs d'écran dans la zone de défilement */
  position: relative;
}

.carte-procedure__icone::before {
  vertical-align: -0.2rem;
}

.carte-procedure__desc {
  /* Le DSFR prévoit une description en un seul paragraphe : on y empile plusieurs lignes */
  display: block;
}

.carte-procedure__lieu {
  /* Jusqu'à 2 lignes, pour que la commune (en fin de ligne) reste visible le plus souvent */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.carte-procedure__alertes {
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
}

.carte-procedure__alertes li {
  padding-bottom: 0.25rem;
}

.carte-procedure__verbe {
  color: var(--text-action-high-blue-france);
}
</style>
