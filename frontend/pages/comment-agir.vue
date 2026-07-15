<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Comment agir contre les dépôts sauvages ?</h1>
        <p class="fr-text fr-text--lead">
          Les maires et les présidents d'intercommunalité disposent d'un levier efficace pour agir
          contre les dépôts sauvages. Grâce à la procédure administrative, ils peuvent obtenir le
          nettoyage d'un dépôt ou sanctionner son auteur lorsqu'il est identifié.
        </p>

        <p class="fr-text fr-text--bold fr-mb-1w">Sur cette page, vous découvrirez :</p>
        <ul class="fr-raw-list fr-mb-2w">
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span
              >les avantages de la procédure administrative pour lutter contre les dépôts
              sauvages</span
            >
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>les grandes étapes de la procédure</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>les réponses aux questions les plus fréquentes</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>
              comment aller plus loin grâce à notre webinaire d'accompagnement (
              <router-link to="/rdv" class="fr-link"
                >Je m'inscris au prochain wébinaire</router-link
              >
              )
            </span>
          </li>
        </ul>
        <p class="fr-text--sm fr-hint-text fr-mb-0">
          <span class="fr-icon-time-line fr-mr-1w" aria-hidden="true"></span>
          Lecture : 5 minutes
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <section class="fr-mb-7w">
        <h2 class="fr-h3 fr-mb-3w">
          <span class="fr-icon-shield-line fr-mr-1w" aria-hidden="true"></span>
          <span>Les collectivités peuvent agir</span>
        </h2>
        <p class="fr-text fr-text--bold">
          Les collectivités disposent d'un véritable pouvoir d'action grâce à la procédure
          administrative.
        </p>
        <p class="fr-text">
          Contrairement à une idée reçue, il n'est pas toujours nécessaire de déposer plainte pour
          agir contre un dépôt sauvage.
        </p>
        <p class="fr-text fr-mb-1w">Grâce à la procédure administrative, la collectivité peut :</p>
        <ul class="fr-raw-list fr-mb-0">
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>agir directement contre un auteur identifié</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>obtenir le nettoyage du dépôt par l'auteur</span>
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span
              >prononcer une amende administrative jusqu'à <strong>15&nbsp;000&nbsp;€</strong> et
              éviter les classements sans suite</span
            >
          </li>
          <li class="fr-mb-1w fr-display-flex">
            <span
              class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
              aria-hidden="true"
            ></span>
            <span>percevoir les recettes de cette amende</span>
          </li>
        </ul>
      </section>

      <section class="fr-mb-7w">
        <h2 class="fr-h3 fr-mb-1w">
          <span class="fr-icon-road-map-line fr-mr-1w" aria-hidden="true"></span>
          <span>Les grandes étapes pour traiter un dépôt sauvage</span>
        </h2>
        <p class="fr-text fr-mb-4w">
          Comment une collectivité peut engager une procédure administrative.
        </p>

        <div class="fr-grid-row fr-grid-row--gutters">
          <div v-for="step in steps" :key="step.badge" class="fr-col-12 fr-col-md-6">
            <article
              class="fr-card fr-card--shadow fr-card--no-arrow fr-p-3w fr-mb-0 card-full-height"
            >
              <div class="fr-card__body">
                <h3 class="fr-h5 fr-mb-2w fr-display-flex fr-flex-wrap fr-gap-1w">
                  <DsfrBadge class="fr-mr-1w" :label="step.badge" type="info" :small="false" />
                  <span>{{ step.title }}</span>
                </h3>
                <p class="fr-text fr-mb-0">{{ step.description }}</p>
              </div>
            </article>
          </div>
        </div>

        <DsfrCallout
          class="fr-mt-4w fr-mb-0"
          title="Vous souhaitez comprendre chaque étape en détail ?"
        >
          <router-link to="/comprendre-la-procedure" class="fr-link">
            Consulter le guide complet de la procédure administrative
          </router-link>
        </DsfrCallout>
      </section>

      <section class="fr-mb-7w">
        <h2 class="fr-h3 fr-mb-3w">
          <span class="fr-icon-question-line fr-mr-1w" aria-hidden="true"></span>
          <span>Les questions les plus fréquentes</span>
        </h2>
        <ul class="fr-raw-list fr-mb-3w">
          <li v-for="item in faqItems" :key="item.slug" class="fr-mb-2w">
            <router-link :to="`/faq/${item.slug}`" class="fr-link fr-text--bold">
              {{ item.question }}
            </router-link>
          </li>
        </ul>
        <router-link to="/faq" class="fr-link fr-link--icon-right fr-icon-arrow-right-line">
          Consulter toutes les questions fréquentes
        </router-link>
      </section>

      <section>
        <article class="fr-card fr-card--shadow fr-card--no-arrow fr-p-4w">
          <div class="fr-card__body">
            <h2 class="fr-h3 fr-mb-1w">
              <span class="fr-icon-live-line fr-mr-1w" aria-hidden="true"></span>
              <span>Participez à notre prochain webinaire</span>
            </h2>
            <p class="fr-text fr-text--bold">
              En moins de 60 minutes, découvrez comment les collectivités peuvent agir concrètement
              contre les dépôts sauvages.
            </p>
            <p class="fr-text">
              Chaque semaine, les équipes de Protect'Envi présentent la procédure administrative,
              expliquent des cas concrets et répondent aux questions des collectivités sur leurs
              moyens d'agir contre les dépôts sauvages.
            </p>
            <p class="fr-text fr-text--bold fr-mb-1w">À l'issue du webinaire, vous saurez :</p>
            <ul class="fr-raw-list fr-mb-3w">
              <li class="fr-mb-1w fr-display-flex">
                <span
                  class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                  aria-hidden="true"
                ></span>
                <span>quand utiliser la procédure administrative</span>
              </li>
              <li class="fr-mb-1w fr-display-flex">
                <span
                  class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                  aria-hidden="true"
                ></span>
                <span>comment traiter votre premier dépôt sauvage</span>
              </li>
              <li class="fr-mb-1w fr-display-flex">
                <span
                  class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                  aria-hidden="true"
                ></span>
                <span>les bonnes pratiques à appliquer et les erreurs à éviter</span>
              </li>
              <li class="fr-mb-1w fr-display-flex">
                <span
                  class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                  aria-hidden="true"
                ></span>
                <span>comment répondre aux situations les plus fréquentes</span>
              </li>
            </ul>
            <p class="fr-text--sm fr-hint-text fr-mb-4w">
              Toutes vos questions pourront être posées en direct à un membre de notre équipe.
            </p>

            <router-link
              to="/rdv"
              class="fr-btn fr-btn--lg fr-mb-4w fr-icon-video-chat-line fr-btn--icon-left"
            >
              Je m'inscris au prochain webinaire
            </router-link>

            <div class="fr-pt-4w border-top">
              <h3 class="fr-h6 fr-mb-1w">Vous ne pouvez pas participer ?</h3>
              <p class="fr-text fr-mb-2w">
                Recevez un récapitulatif des informations essentielles ainsi que les prochaines
                dates de webinaire.
              </p>
              <TallyPopupButton
                form-id="Pdyay0"
                label="Je souhaite recevoir les ressources clés et les prochaines dates par e-mail"
                variant="secondary"
                to="/comment-agir/etre-informe"
                icon="fr-icon-mail-line"
              />
            </div>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import TallyPopupButton from '@/components/shared/TallyPopupButton.vue'
import { useTallyRoutes } from '@/composables/useTally'
import { DsfrBadge, DsfrCallout } from '@gouvminint/vue-dsfr'

useTallyRoutes({
  '/comment-agir/etre-informe': {
    formId: 'Pdyay0',
    options: { layout: 'modal', width: 900 },
    returnPath: '/comment-agir',
  },
})

const steps = [
  {
    badge: 'Étape 1',
    title: 'Identification',
    description: "Rechercher les éléments permettant d'identifier un auteur présumé.",
  },
  {
    badge: 'Étape 2',
    title: 'Constatation',
    description: 'Une personne habilitée établit le rapport de constatation.',
  },
  {
    badge: 'Étape 3',
    title: 'Information',
    description:
      "L'auteur présumé est informé par courrier et dispose d'un délai pour présenter ses observations.",
  },
  {
    badge: 'Étape 4',
    title: 'Décision',
    description:
      "Le maire ou le président d'intercommunalité décide de sanctionner l'auteur ou non.",
  },
  {
    badge: 'Étape 5',
    title: 'Exécution',
    description:
      'La procédure peut aboutir au retrait des déchets et/ou à une amende administrative recouvrée au profit de la mairie.',
  },
]

const faqItems = [
  {
    question: 'Dois-je obligatoirement déposer plainte ?',
    slug: 'dois-je-obligatoirement-deposer-plainte-pour-engager-une-procedure-contre-un-depot-sauvage',
  },
  {
    question: 'Est-ce que je peux retirer le dépôt sauvage immédiatement ?',
    slug: 'peut-on-retirer-un-depot-sauvage-immediatement',
  },
  {
    question: 'Comment identifier un auteur ?',
    slug: 'comment-identifier-lauteur',
  },
  {
    question:
      'Faut-il une délibération du conseil municipal pour lancer une procédure administrative ?',
    slug: 'faut-il-une-deliberation-du-conseil-municipal-pour-demarrer-une-procedure-administrative',
  },
  {
    question: 'Puis-je agir sur un terrain privé ?',
    slug: 'peut-on-engager-une-procedure-si-le-depot-est-sur-un-terrain-prive',
  },
]
</script>

<style scoped>
.card-full-height {
  height: 100%;
}

.border-top {
  border-top: 1px solid var(--border-default-grey);
}
</style>
