<template>
  <div>
    <!-- Hero Section -->
    <div class="hero-section fr-mb-6w">
      <div class="fr-container">
        <div class="fr-grid-row fr-grid-row--center">
          <div class="fr-col-12 fr-col-md-10 fr-col-lg-8">
            <h1 class="fr-hero__title fr-text--center">
              Luttez efficacement contre les dépôts sauvages dans votre commune.
            </h1>
            <p class="fr-hero__text fr-text--lg fr-text--center">
              Vous êtes une collectivité touchée par les dépôts sauvages et vous souhaitez agir ? La
              Gendarmerie nationale recherche 100 communes volontaires pour ce dispositif pilote
              d'accompagnement personnalisé.
            </p>
            <div class="fr-hero__actions fr-text--center">
              <a class="fr-btn fr-btn--lg" href="#formulaire"> Je veux être accompagné</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Section -->
    <div class="fr-container fr-py-6w">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <h2 class="fr-h2 fr-mb-4w">Le problème</h2>
          <div class="fr-grid-row fr-grid-row--gutters fr-mb-4w">
            <div class="fr-col-12 fr-col-md-4">
              <div class="fr-card fr-card--sm fr-card--grey">
                <div class="fr-card__body">
                  <h3 class="fr-card__title">Des coûts qui s'accumulent</h3>
                  <p class="fr-card__desc">
                    Chaque année, les dépôts sauvages coûtent des milliers d'euros aux communes.
                  </p>
                </div>
              </div>
            </div>
            <div class="fr-col-12 fr-col-md-4">
              <div class="fr-card fr-card--sm fr-card--grey">
                <div class="fr-card__body">
                  <h3 class="fr-card__title">Des auteurs impunis</h3>
                  <p class="fr-card__desc">
                    Les interventions se répètent, Les auteurs sont rarement sanctionnés.
                  </p>
                </div>
              </div>
            </div>
            <div class="fr-col-12 fr-col-md-4">
              <div class="fr-card fr-card--sm fr-card--grey">
                <div class="fr-card__body">
                  <h3 class="fr-card__title">Des agents et élus démunis</h3>
                  <p class="fr-card__desc">
                    Face aux incivilités et aux dégradations de l’environnement, les attentes des
                    citoyens sont fortes
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Section -->
    <div id="formulaire" class="fr-container fr-py-6w">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12">
          <h2 class="fr-h2 fr-mb-4w">Je veux être accompagné</h2>
          <div class="fr-card">
            <div class="fr-card__body fr-px-0">
              <iframe
                src="https://grist.numerique.gouv.fr/o/cesan-investigation/forms/iDiH8ZjadFkK38hbkuAXAY/197"
                width="100%"
                height="2100"
                frameborder="0"
                scrolling="no"
                style="overflow: hidden; border: none"
                title="Formulaire"
                class="grist-form"
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Information Section -->
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
  </div>
</template>

<script setup lang="ts">
// Landing page
</script>

<style scoped>
/* Smooth scroll behavior for anchor links */
html {
  scroll-behavior: smooth;
}

/* Hero section with consistent background color */
.hero-section {
  background-color: #f5f5fe;
  padding: 4rem 0;
}

/* Disable iframe scrolling */
.grist-form {
  overflow: hidden;
}

/* Ensure proper spacing from footer */
.fr-container {
  margin-bottom: 2rem;
}
</style>
