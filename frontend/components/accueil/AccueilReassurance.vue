<template>
  <div class="fr-container fr-py-8w">
    <h2 class="fr-h2 fr-mb-6w premium-text-center">
      Protect'Envi accompagne les collectivités de A à Z
    </h2>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-4">
        <div class="reassurance-card">
          <span class="step-number">1</span>
          <h3 class="fr-h4 fr-mt-2w fr-mb-1w">Guide pas à pas de la procédure</h3>
          <p class="fr-text fr-mb-0 text-muted">
            Un parcours étape par étape, accessible même sans expertise juridique.
          </p>
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <div class="reassurance-card">
          <span class="step-number">2</span>
          <h3 class="fr-h4 fr-mt-2w fr-mb-1w">Procédure juridiquement sécurisée</h3>
          <p class="fr-text fr-mb-0 text-muted">
            Des modèles de documents conformes au Code de l'environnement.
          </p>
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <div class="reassurance-card">
          <span class="step-number">3</span>
          <h3 class="fr-h4 fr-mt-2w fr-mb-1w">Service public gratuit</h3>
          <p class="fr-text fr-mb-0 text-muted">
            Développé par les équipes du CESAN de la Gendarmerie nationale.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.reassurance-card {
  border: 1px solid var(--border-default-grey);
  border-radius: 8px;
  background: var(--background-default-grey);
  box-shadow: var(--premium-shadow);
  padding: 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.reassurance-card:hover {
  border-color: var(--border-active-blue-france);
  transform: translateY(-1px);
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--background-alt-blue-france);
  color: var(--text-active-blue-france);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
}
</style>
