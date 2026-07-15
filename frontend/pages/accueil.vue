<template>
  <div>
    <!-- Bandeau Webinaire -->
    <DsfrNotice
      title="Prochain webinaire de : jeudi 23 juillet à 11h00 — une heure pour comprendre la procédure et poser vos questions."
      :closeable="false"
      class="fr-mb-0"
    >
      <template #desc>
        <router-link to="/rdv" class="fr-link fr-ml-1w"> S'inscrire au webinaire </router-link>
      </template>
    </DsfrNotice>

    <!-- Hero Section -->
    <div class="fr-container fr-py-6w">
      <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
        <div class="fr-col-12 fr-col-md-6 premium-hero-text">
          <h1 class="fr-h1 fr-mt-0 fr-mb-2w text-balance">
            Agir contre les dépôts sauvages dans votre collectivité
          </h1>
          <p class="fr-text fr-text--lead fr-mb-3w">
            Comprendre comment agir, sécuriser vos procédures et sanctionner les auteurs de dépôts
            sauvages.
          </p>
          <ul class="fr-p-0 fr-mt-2w fr-mb-0 unstyled-list">
            <li class="fr-mb-2v fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                aria-hidden="true"
              ></span>
              <span
                ><strong>Accompagnement pas à pas</strong>, accessible sans expertise
                juridique</span
              >
            </li>
            <li class="fr-mb-2v fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                aria-hidden="true"
              ></span>
              <span
                ><strong>Procédure juridiquement sécurisée</strong>, conforme au Code de
                l'environnement</span
              >
            </li>
            <li class="fr-mb-2v fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-fill fr-text-default--success fr-mr-1w"
                aria-hidden="true"
              ></span>
              <span><strong>Dispositif gratuit</strong> proposé par la Gendarmerie nationale</span>
            </li>
          </ul>
        </div>

        <div class="fr-col-12 fr-col-md-6">
          <DsfrPicture
            class="premium-rounded-image"
            legend="Constatation d'un dépôt sauvage par la police municipale"
            ratio="16x9"
            size="medium"
            src="/static/depot-de-dechet-sauvage-image-accueil.webp"
            title="Constatation d'un dépôt sauvage par la police municipale"
          />
        </div>
      </div>
    </div>

    <!-- Bloc d'orientation -->
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
              <router-link to="/simulateur" class="fr-link">
                Vérifier d'abord si je peux engager une procédure
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
              <router-link to="/rdv" class="fr-link">
                Participer au prochain webinaire
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section Pouvoir d'agir -->
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

    <!-- Section Réassurance -->
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

    <!-- Section Témoignages -->
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

    <!-- Section Chiffres clés -->
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

    <!-- Section CTA Final -->
    <div class="fr-container fr-py-8w premium-text-center">
      <div class="fr-grid-row fr-grid-row--center">
        <div class="fr-col-12 fr-col-md-8">
          <h2 class="fr-h2 fr-mb-2w">Une question sur votre situation ?</h2>
          <p class="fr-text fr-text--lead fr-mb-4w">
            Chaque semaine, l'équipe Protect'Envi répond en direct aux questions des collectivités
            lors d'un webinaire d'une heure.
          </p>
          <router-link to="/rdv" class="fr-btn fr-btn--lg">
            Participer au prochain webinaire
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTallyRoutes } from '@/composables/useTally'
import { DsfrNotice, DsfrPicture } from '@gouvminint/vue-dsfr'

useTallyRoutes({
  '/simulateur': { formId: 'A7xA8z', options: { layout: 'modal', width: 900 } },
  '/calculateur': { formId: '9qElYG', options: { layout: 'modal', width: 900 } },
})
</script>

<style scoped>
.text-balance {
  text-wrap: balance;
}

.unstyled-list {
  list-style: none;
}

.card-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
}

.quote-author {
  font-size: 0.9rem;
}

.quote-source {
  display: block;
  font-weight: normal;
  color: var(--text-mention-grey);
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

.info-bullet-box {
  background: var(--background-default-grey);
  border-left: 4px solid var(--border-active-blue-france);
  border-radius: 4px;
  box-shadow: var(--premium-shadow);
}

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
