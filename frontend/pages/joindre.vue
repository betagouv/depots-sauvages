<template>
  <main>
    <div class="hero-section fr-mb-4w fr-py-4w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">
              Rejoignez les 100 collectivités pilotes pour mieux lutter contre les dépôts sauvages.
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              Vous êtes une collectivité touchée par les dépôts sauvages et vous souhaitez agir ? La
              Gendarmerie nationale peut vous aider. Pour bénéficier d’un accompagnement
              personnalisé complétez le formulaire ci-dessous en deux minutes.
            </p>
            <div class="fr-hero__actions fr-text--center">
              <a
                class="fr-btn fr-btn--lg"
                href="#formulaire"
              >
                Je candidate pour ma collectivité
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Why Join Section -->
    <div class="fr-container">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <h2 class="fr-h2 fr-mb-4w">Pourquoi rejoindre le dispositif Protect’Envi ?</h2>
          <div class="fr-grid-row fr-grid-row--gutters fr-mb-4w">
            <div class="fr-col-12 fr-col-md-4">
              <DsfrCard
                no-arrow
                size="sm"
                title="Bénéficiez d'une aide juridique"
                description="Accompagnement par la Gendarmerie et conseils juridiques adaptés à vos besoins."
                class="fr-card--grey"
              />
            </div>
            <div class="fr-col-12 fr-col-md-4">
              <DsfrCard
                no-arrow
                size="sm"
                title="Simplifiez vos démarches"
                description="Des outils et des modèles pour accélérer et sécuriser vos démarches."
                class="fr-card--grey"
              />
            </div>
            <div class="fr-col-12 fr-col-md-4">
              <DsfrCard
                no-arrow
                size="sm"
                title="Des sanctions qui aboutissent face aux incivilités"
                description="Des procédures efficaces pour identifier et sanctionner les auteurs."
                class="fr-card--grey"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Section -->
    <div id="formulaire" class="fr-container fr-pb-4w">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <h2 class="fr-h2 fr-mb-4w">Je candidate pour ma collectivité</h2>
          <div class="fr-card">
            <div class="fr-card__body fr-px-0">
              <iframe
                src="https://grist.numerique.gouv.fr/o/cesan-investigation/forms/iDiH8ZjadFkK38hbkuAXAY/197"
                width="100%"
                height="2100"
                scrolling="no"
                style="overflow: hidden; border: none"
                title="Formulaire de candidature Protect’Envi"
                class="grist-form"
                loading="lazy"
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Section -->
    <div class="fr-container fr-pt-8w">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <h2 class="fr-h2 fr-mb-4w">Le problème</h2>
          <div class="fr-grid-row fr-grid-row--gutters fr-mb-4w">
            <div class="fr-col-12 fr-col-md-4">
              <DsfrCard
                no-arrow
                size="sm"
                title="Des coûts qui s'accumulent"
                description="Chaque année, les dépôts sauvages coûtent des milliers d'euros aux communes. (Source : ADEME)"
                class="fr-card--grey"
              />
            </div>
            <div class="fr-col-12 fr-col-md-4">
              <DsfrCard
                no-arrow
                size="sm"
                title="Des auteurs impunis"
                description="Les interventions se répètent, les auteurs sont rarement sanctionnés."
                class="fr-card--grey"
              />
            </div>
            <div class="fr-col-12 fr-col-md-4">
              <DsfrCard
                no-arrow
                size="sm"
                title="Des agents et élus démunis"
                description="Face aux incivilités et aux dégradations de l'environnement, les attentes des citoyens sont fortes"
                class="fr-card--grey"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="fr-container fr-py-4w">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-8">
          <p class="fr-text--lg fr-text--center">
            Si vous souhaitez démarrer une procédure administrative pour lutter contre les dépôts
            sauvages, rendez-vous sur :
            <a
              href="https://protect-envi.beta.gouv.fr/debuter-procedure"
              class="fr-link fr-link--lg"
            >
              https://protect-envi.beta.gouv.fr/
            </a>
          </p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { DsfrCard } from '@gouvminint/vue-dsfr';
</script>

<style scoped>
/* Smooth scroll behavior for anchor links */
html {
  scroll-behavior: smooth;
}

/* Hero section with consistent background color */
.hero-section {
  background-color: #f5f5fe;
}

/* Disable iframe scrolling */
.grist-form {
  overflow: hidden;
}
</style>
