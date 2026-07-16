<template>
  <div class="fr-py-8w premium-pouvoir-agir-wrapper">
    <div class="fr-container">
      <div class="header-section fr-mb-6w text-center">
        <h2 class="fr-h2 fr-mb-2w">Les collectivités peuvent agir</h2>
        <p class="fr-text fr-text--lead fr-mb-0 lead-text">
          Contrairement à une idée reçue, le maire ou le président d'intercommunalité peut agir
          directement grâce à la procédure administrative.
        </p>
      </div>

      <div class="fr-grid-row fr-grid-row--gutters">
        <div v-for="(power, index) in powers" :key="index" class="fr-col-12 fr-col-md-6">
          <div class="power-card">
            <div class="power-icon-wrapper">
              <span :class="['power-icon', power.icon]" aria-hidden="true"></span>
            </div>
            <p class="fr-text fr-m-0 power-text" v-html="power.html"></p>
          </div>
        </div>
      </div>

      <div class="text-center fr-mt-6w">
        <router-link to="/comment-agir" class="fr-btn fr-btn--secondary fr-btn--lg">
          Je souhaite savoir comment agir
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const powers = [
  {
    icon: 'fr-icon-user-search-line',
    html: 'Agir directement contre un auteur identifié, <strong>sans passer par un dépôt de plainte</strong>.',
  },
  {
    icon: 'fr-icon-checkbox-circle-line',
    html: "Obtenir <strong>le nettoyage du dépôt par l'auteur</strong>, avant même la sanction.",
  },
  {
    icon: 'fr-icon-money-euro-box-line',
    html: "Prononcer une <strong>amende administrative pouvant aller jusqu'à 15 000 €</strong>.",
  },
  {
    icon: 'fr-icon-scales-3-line',
    html: "Percevoir <strong>les recettes de l'amende au bénéfice de la collectivité</strong>.",
  },
]
</script>

<style scoped>
.premium-pouvoir-agir-wrapper {
  background: linear-gradient(135deg, var(--background-alt-blue-france) 0%, #f0f2ff 100%);
}

.header-section {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.lead-text {
  color: var(--text-mention-grey);
}

.power-card {
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-radius: 16px;
  padding: 1.5rem 2rem;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 100, 0.02);
}

.power-card:hover {
  border-color: var(--border-active-blue-france);
  box-shadow: 0 10px 30px rgba(0, 0, 145, 0.06);
  transform: translateY(-4px);
}

.power-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background-color: var(--background-contrast-info, #e3e3fd);
  border-radius: 50%;
  color: var(--text-active-blue-france, #000091);
  margin-right: 1.5rem;
  flex-shrink: 0;
}

.power-icon {
  font-size: 1.5rem;
}

.power-text {
  font-size: 1.15rem;
  line-height: 1.6;
  color: var(--text-default-grey);
}

.text-center {
  text-align: center;
}
</style>
