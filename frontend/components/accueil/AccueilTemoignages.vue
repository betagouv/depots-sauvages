<template>
  <div class="fr-background-alt--blue-france fr-py-8w">
    <div class="fr-container">
      <h2 class="fr-h2 fr-mb-6w premium-text-center">Ils ont agi avec Protect'Envi</h2>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <blockquote class="fr-quote quote-custom">
            <span class="quote-icon">“</span>
            <p class="fr-text fr-mb-3w">
              Protect'Envi permet de générer des courriers parfaitement structurés, que nous
              envoyons aux auteurs présumés des dépôts. Sur les trois derniers courriers envoyés,
              j'ai obtenu un retour en moins d'une semaine à chaque fois.
            </p>
            <cite class="fr-quote__author quote-author">
              <strong>Philippe Barneron</strong>
              <span class="fr-quote__source quote-source">
                Maire de Peyrins (26) — commune de 2 700 habitants
              </span>
            </cite>
          </blockquote>
        </div>
        <div class="fr-col-12 fr-col-md-6">
          <blockquote class="fr-quote quote-custom">
            <span class="quote-icon">“</span>
            <p class="fr-text fr-mb-3w">
              Travaillant seul, sans véritable soutien juridique en interne, cet accompagnement a
              été un véritable soulagement. Il m'a permis d'avancer dans une procédure qui
              stagnait depuis plus d'un an : l'auteur des faits a commencé à retirer ses déchets.
            </p>
            <cite class="fr-quote__author quote-author">
              <strong>Ludovic Caramel</strong>
              <span class="fr-quote__source quote-source">
                Police municipale de Saint-Sulpice-de-Royan (17) — commune de 3 450 habitants
              </span>
            </cite>
          </blockquote>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.quote-custom {
  background: var(--background-default-grey);
  box-shadow: var(--premium-shadow);
  border-radius: 8px;
  padding: 2.5rem 2rem 2rem 2rem;
  position: relative;
  margin: 0;
  height: 100%;
}

.quote-icon {
  font-family: Marianne, Arial, sans-serif;
  font-size: 5rem;
  color: var(--background-active-blue-france);
  opacity: 0.2;
  position: absolute;
  top: -10px;
  left: 15px;
  line-height: 1;
}

.quote-author {
  font-size: 0.9rem;
}

.quote-source {
  display: block;
  font-weight: normal;
  color: var(--text-mention-grey);
}
</style>
