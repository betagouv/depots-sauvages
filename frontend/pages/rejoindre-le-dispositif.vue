<template>
  <main>
    <div>
      <p class="fr-sr-only" id="formulaire-protectenvi-description">
      Formulaire de candidature à remplir pour postuler au dispositif Protect’Envi, intégré depuis la plateforme Grist.
      </p>
      <iframe
        src="https://grist.numerique.gouv.fr/o/cesan-investigation/forms/iDiH8ZjadFkK38hbkuAXAY/197"
        width="100%"
        height="2100"
        scrolling="no"
        style="overflow: hidden; border: none"
        title="Formulaire de candidature Protect’Envi"
        class="grist-form"
        loading="lazy"
        aria-describedby="formulaire-protectenvi-description"
      ></iframe>
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
              aria-label="Ouvrir Protect-Envi pour démarrer la procédure"
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
// Landing page
</script>

<style scoped>
.grist-form {
  overflow: hidden;
}
</style>
