<template>
  <div class="fr-container--sm fr-py-5w">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <h1 class="fr-h1 fr-mb-3w">
          Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.
        </h1>
        <p class="fr-text fr-mb-2w">Simplifier le signalement des dépôts sauvages</p>
        <p>
          Protect’Envi est l'outil qui vous accompagne et vous aide à produire des rapports pour
          faciliter la procédure administrative et judiciaire.
        </p>
        <p>
          Notre objectif : améliorer l’efficacité des services publics, faciliter les procédures et
          contribuer à la réduction durable des dépôts sauvages sur le territoire.
        </p>
        <a
          v-if="useExternalLink"
          :href="demarcheNumeriqueUrl"
          class="fr-btn fr-mt-3w"
          target="_blank"
          rel="noopener noreferrer"
          >Débuter une procédure
        </a>
        <RouterLink v-else to="/debuter-procedure" class="fr-btn fr-mt-3w"
          >Débuter une procédure
        </RouterLink>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrPicture
          legend="Dépôt sauvage"
          ratio="16x9"
          size="medium"
          src="/static/depot-de-dechet-sauvage-image-accueil.webp"
          title="Dépôt sauvage"
        />
      </div>

      <section>
        <h2>Le fléau des dépôts sauvages</h2>
        <p>
          Les dépôts sauvages dégradent notre environnement et représentent un coût important pour
          les communes.
        </p>
        <p>
          Malgré leur engagement, les collectivités manquent souvent de ressources, de temps et
          d’accompagnement pour agir efficacement.
        </p>
        <p>
          La procédure administrative donne des pouvoirs importants aux Maires (et permet à la
          collectivité de verbaliser) mais elle est très mal connue et peu utilisée.
        </p>
        <p>
          La procédure judiciaire génère de la frustration car les plaintes sont très souvent
          classées sans suite.
        </p>
        <p>
          Protect’Envi vous accompagne dans ces procédures en vous guidant pas à pas et en vous
          fournissant des documents conformes pré-remplis.
        </p>
      </section>

      <section class="fr-container fr-my-6w">
        <h2 class="fr-h2 fr-mb-4w">Comment fonctionne Protect’Envi ?</h2>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div
            class="fr-col-12 fr-col-md-6 fr-col-lg-3"
            v-for="(card, index) in cardsFonctionnement"
            :key="index"
          >
            <DsfrCard no-arrow :title="card.titre" :description="card.description" enlarge-link />
          </div>
        </div>
      </section>

      <section class="fr-container fr-my-6w">
        <h2 class="fr-h2 fr-mb-4w">Des documents pour constituer votre démarche</h2>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div
            class="fr-col-12 fr-col-md-6 fr-col-lg-3"
            v-for="(card, index) in cardsDocuments"
            :key="index"
          >
            <DsfrCard no-arrow :title="card.titre" :description="card.description" enlarge-link />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrPicture } from '@gouvminint/vue-dsfr'

const isDemarcheNumeriqueEnabled = import.meta.env.VITE_DN_ENABLED === 'true'
const demarcheNumeriqueUrl = import.meta.env.VITE_DN_URL

const useExternalLink = isDemarcheNumeriqueEnabled && demarcheNumeriqueUrl

const cardsFonctionnement = [
  {
    titre: 'Déclarer le dépôt sauvage',
    description:
      'Un formulaire simple et rapide à remplir pour identifier le dépôt sauvage (lieu, type de déchets, photos...).',
  },
  {
    titre: 'Récupérer mes documents de procédure',
    description:
      'À partir de ces informations, Protect’Envi génère des documents pré-remplis, conformes aux exigences administratives (lettre d’information, rapport de constatation).',
  },
  {
    titre: 'Compléter mes documents et initier la procédure',
    description:
      'Personnaliser vos documents, signez si besoin, et envoyez -les aux interlocuteurs concernés pour démarrer la procédure.',
  },
  {
    titre: "Bénéficier d'un accompagnement personnalisé",
    description:
      "Vous avez des questions supplémentaires ? Vous avez besoin d'aide sur un cas spécifique ? Notre équipe répond à toutes vos questions et vous accompagne.",
  },
]

const cardsDocuments = [
  {
    titre: 'Le rapport de constatation',
    description:
      'Ajoutez et personnaliser votre rapport, signez si besoin, et envoyez le rapport aux interlocuteurs compétents (propriétaire, préfecture, etc.).',
  },
  {
    titre: "La lettre d'information",
    description:
      "Un courrier de la commune signé par le maire qui informe l'auteur des faits qui lui sont reprochés. Il indique les sanctions encourues et donne un délai pour formuler ses observations.",
  },
]
</script>
