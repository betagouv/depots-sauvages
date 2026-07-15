<template>
  <div class="fr-container fr-pb-8w">
    <h2 class="fr-h2 fr-mb-1w">Quel est votre besoin aujourd'hui ?</h2>
    <p class="fr-text fr-mb-4w">
      Deux situations, deux parcours : choisissez celui qui correspond à la vôtre.
    </p>

    <div class="fr-grid-row fr-grid-row--gutters">
      <!-- Box gauche (Action) -->
      <div class="fr-col-12 fr-col-md-6">
        <div class="orientation-card orientation-card--active">
          <h3 class="fr-h3 fr-mb-2w">J'ai un dépôt sauvage et je veux agir maintenant</h3>
          <p class="fr-text fr-mb-4w text-muted" style="flex-grow: 1">
            Vous avez un cas concret et souhaitez engager une action.
          </p>
          <div class="card-actions">
            <router-link to="/demarrer-constatation" class="fr-btn fr-btn--lg">
              Démarrer une procédure
            </router-link>
          </div>
        </div>
      </div>

      <!-- Box droite (Comprendre/Webinaire) -->
      <div class="fr-col-12 fr-col-md-6">
        <div class="orientation-card orientation-card--info">
          <h3 class="fr-h3 fr-mb-2w">Je veux savoir comment agir contre les dépôts sauvages</h3>
          <p class="fr-text fr-mb-4w text-muted" style="flex-grow: 1">
            Découvrez les solutions à disposition des collectivités et les étapes de la procédure.
          </p>
          <div class="card-actions">
            <router-link
              to="/comment-agir"
              class="fr-btn fr-btn--secondary fr-btn--lg"
            >
              Comment agir
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.card-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}

.orientation-card {
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 12px;
  padding: 2.5rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease-in-out;
  box-shadow: var(--premium-shadow);
}

.orientation-card:hover {
  border-color: var(--border-active-blue-france);
  box-shadow: 0 8px 24px rgba(0, 0, 145, 0.08);
  transform: translateY(-2px);
}

.orientation-card--active {
  border-top: 4px solid var(--border-active-blue-france);
}

.orientation-card--info {
  border-top: 4px solid #6a6af4;
}
</style>
