<template>
  <div class="fr-py-6w stats-bar">
    <div class="fr-container">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="stat-item">
            <div class="stat-number">600 m³</div>
            <p class="stat-label">de déchets retirés par les auteurs</p>
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="stat-item">
            <div class="stat-number">500</div>
            <p class="stat-label">procédures engagées</p>
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="stat-item">
            <div class="stat-number">26 000 €</div>
            <p class="stat-label">d'amendes prononcées</p>
          </div>
        </div>
        <div class="fr-col-12 fr-col-sm-6 fr-col-md-3">
          <div class="stat-item">
            <div class="stat-number">300+</div>
            <p class="stat-label">collectivités accompagnées</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.stats-bar {
  background-color: var(--background-flat-blue-france);
  color: var(--text-inverted-blue-france);
}

.stat-item {
  padding-left: 1.5rem;
  border-left: 2px solid #6a6af4;
}

.stat-number {
  font-size: 2.5rem;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-inverted-blue-france);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 0;
  color: var(--text-inverted-blue-france);
}
</style>
