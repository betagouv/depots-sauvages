<template>
  <div class="fr-py-8w fr-background-alt--grey">
    <div class="fr-container">
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col-12 fr-col-md-5">
          <h2 class="fr-h2 fr-mb-2w">
            Les collectivités peuvent agir contre les dépôts sauvages
          </h2>
          <p class="fr-text fr-text--lead fr-mb-4w">
            Contrairement à une idée reçue, le maire ou le président d'intercommunalité peut agir
            directement grâce à la procédure administrative.
          </p>
          <router-link to="/comment-agir" class="fr-btn fr-btn--secondary">
            Je souhaite savoir comment agir
          </router-link>
        </div>
        <div class="fr-col-12 fr-col-md-7">
          <ul class="fr-p-0 fr-m-0 unstyled-list">
            <li class="fr-p-3w fr-mb-2w info-bullet-box">
              Agir directement contre un auteur identifié,
              <strong>sans passer par un dépôt de plainte</strong>
            </li>
            <li class="fr-p-3w fr-mb-2w info-bullet-box">
              Obtenir <strong>le nettoyage du dépôt par l'auteur</strong>, avant même la sanction
            </li>
            <li class="fr-p-3w fr-mb-2w info-bullet-box">
              Prononcer une <strong>amende administrative pouvant aller jusqu'à 15 000 €</strong>
            </li>
            <li class="fr-p-3w info-bullet-box">
              Percevoir <strong>les recettes de l'amende au bénéfice de la collectivité</strong>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.unstyled-list {
  list-style: none;
}

.info-bullet-box {
  background: var(--background-default-grey);
  border-left: 4px solid var(--border-active-blue-france);
  border-radius: 4px;
  box-shadow: var(--premium-shadow);
}
</style>
