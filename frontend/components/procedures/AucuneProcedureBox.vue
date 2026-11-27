<template>
  <section aria-labelledby="aucune-procedure-titre">
    <h2 id="aucune-procedure-titre" class="fr-h3 fr-mb-4w">Aucune procédure en cours</h2>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card">
          <div class="fr-card__body">
            <div class="fr-card__content">
              <h3 class="fr-card__title">J'ai un dépôt à traiter</h3>
              <p class="fr-card__desc">
                Constatez le dépôt : Stop Dépôt Sauvage génère automatiquement vos documents de
                procédure et vous guide pas à pas.
              </p>
            </div>
            <div class="fr-card__footer">
              <ul class="fr-btns-group fr-btns-group--inline-md fr-btns-group--icon-left">
                <li>
                  <router-link
                    to="/demarrer-constatation"
                    class="fr-btn fr-icon-add-line fr-btn--icon-left"
                    @click="track('Clic Démarrer une constatation')"
                  >
                    Démarrer une constatation
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <div class="fr-card">
          <div class="fr-card__body">
            <div class="fr-card__content">
              <h3 class="fr-card__title">Pas encore de cas ?</h3>
              <p class="fr-card__desc">
                Préparez votre collectivité pour prévenir les dépôts et être prêt le jour où un
                dépôt arrive.
              </p>
            </div>
            <div class="fr-card__footer">
              <ul class="fr-btns-group fr-btns-group--inline-md fr-btns-group--icon-right">
                <li>
                  <router-link
                    to="/se-preparer"
                    class="fr-btn fr-btn--secondary fr-icon-arrow-right-line fr-btn--icon-right"
                    @click="track('Clic Se préparer')"
                  >
                    Se préparer
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { trackEvent } from '@/services/matomo'

const track = (action: string) => trackEvent('Mes procédures', action, 'Aucune procédure')
</script>
