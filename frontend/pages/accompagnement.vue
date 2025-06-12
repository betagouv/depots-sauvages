<template>
  <main class="fr-container--sm fr-py-5w">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <h1 class="fr-h1 fr-mb-3w">Un accompagnement personnalisé pour mieux agir</h1>
        <p class="fr-text fr-mb-2w">Simplifier le signalement des dépôts sauvages</p>
        <p>
          Notre équipe vous accompagne pour vous guider dans chaque étape du traitement des dépôts sauvages.
        </p>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <DsfrPicture
          legend="Dépot de déchets sauvage"
          ratio="16x9"
          size="medium"
          src="/static/depot-de-dechet-sauvage-image-accueil.webp"
          title="Dépot de déchets sauvage"
        />
      </div>

      <div class="fr-container">
        <h2>Contactez-nous</h2>
        <p class="fr-mb-4w">
          Choisissez votre mode de contact préféré pour démarrer votre démarche :
        </p>
        <div class="fr-grid-row fr-grid-row--gutters">
          <div class="fr-col-12 fr-col-md-6">
            <a
              :href="`mailto:${contactEmail}`"
              class="fr-btn fr-mb-2w"
              aria-label="Envoyer un e-mail"
            >
              Envoyer un e-mail
            </a>
            <p class="fr-text--bold">Besoin d’aide ou d’informations détaillées ?</p>
            <p>
              Envoyez-nous un e-mail en cliquant sur le bouton ci-dessus. Vous pouvez poser vos questions, joindre des documents et expliquer votre situation en détail. Notre équipe vous répondra dans les meilleurs délais.
            </p>
          </div>

          <div class="fr-col-12 fr-col-md-6">
            <a
              :href="whatsappLink"
              target="_blank"
              rel="noopener noreferrer"
              class="fr-btn fr-btn--secondary fr-mb-2w"
              aria-label="Contacter via WhatsApp"
            >
            Démarrer une conversation WhatsApp
            </a>
            <p class="fr-text--bold">Pour une réponse rapide et un échange direct</p>
            <p>
              Discutez directement avec notre équipe sur WhatsApp pour obtenir une aide rapide et personnalisée.
            </p>
            <p>Vous serez redirigé vers un groupe WhatsApp d’accueil, où un conseiller vous répondra rapidement.</p>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
const contactEmail = import.meta.env.VITE_CONTACT_EMAIL;
const whatsappLink = import.meta.env.VITE_WHATSAPP_LINK;
</script>
