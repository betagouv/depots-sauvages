<template>
  <div class="fr-container fr-py-8w">
    <h2 class="fr-h2 fr-mb-6w premium-text-center">
      Protect'Envi accompagne les collectivités de A à Z
    </h2>
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-4">
        <div class="reassurance-card">
          <div class="reassurance-illustration">
            <img src="/static/artwork/pictograms/document-search.svg" alt="Illustration guide" />
          </div>
          <h3 class="fr-h4 fr-mt-2w fr-mb-1w">Guide pas à pas de la procédure</h3>
          <p class="fr-text fr-mb-0 text-muted">
            Un parcours étape par étape, accessible même sans expertise juridique.
          </p>
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <div class="reassurance-card">
          <div class="reassurance-illustration">
            <img src="/static/artwork/pictograms/justice.svg" alt="Illustration justice" />
          </div>
          <h3 class="fr-h4 fr-mt-2w fr-mb-1w">Procédure juridiquement sécurisée</h3>
          <p class="fr-text fr-mb-0 text-muted">
            Des modèles de documents conformes au Code de l'environnement.
          </p>
        </div>
      </div>
      <div class="fr-col-12 fr-col-md-4">
        <div class="reassurance-card">
          <div class="reassurance-illustration">
            <img
              src="/static/artwork/pictograms/human-cooperation.svg"
              alt="Illustration coopération"
            />
          </div>
          <h3 class="fr-h4 fr-mt-2w fr-mb-1w">Service public gratuit</h3>
          <p class="fr-text fr-mb-0 text-muted">
            Développé par les équipes du CESAN de la Gendarmerie nationale.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.reassurance-card {
  border: 1px solid var(--border-default-grey);
  border-radius: 12px;
  background: var(--background-default-grey);
  box-shadow: var(--premium-shadow);
  padding: 2.5rem 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: all 0.2s ease-in-out;
}

.reassurance-card:hover {
  border-color: var(--border-active-blue-france);
  box-shadow: 0 8px 24px rgba(0, 0, 145, 0.08);
  transform: translateY(-2px);
}

.reassurance-illustration {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.reassurance-illustration img {
  height: 100%;
  width: auto;
  object-fit: contain;
}

.premium-text-center {
  text-align: center;
}
</style>
