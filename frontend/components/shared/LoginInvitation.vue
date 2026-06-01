<template>
  <PremiumBox
    :title="title"
    :description="description"
    iconClass="fr-icon-account-circle-line"
  >
    <template #actions>
      <DsfrButton @click="goToLogin">
        <span class="fr-icon-lock-line fr-mr-1w" aria-hidden="true"></span>
        Se connecter via ProConnect
      </DsfrButton>
    </template>

    <template #footer>
      <p class="fr-text--sm fr-mb-0">
        ProConnect est la solution de connexion sécurisée pour les agents de l'État et des
        collectivités. Si vous rencontrez des difficultés,
        <a
          href="https://proconnect.crisp.help/fr/article/utiliser-proconnect-au-sein-dune-collectivite-ou-dune-mairie-1mobnb6"
          target="_blank"
          rel="noopener"
          >consultez cette aide en ligne</a
        >.
      </p>
    </template>
  </PremiumBox>
</template>

<script setup lang="ts">
import { DsfrButton } from '@gouvminint/vue-dsfr'
import PremiumBox from '@/components/shared/PremiumBox.vue'
import { LOGIN_URL } from '@/services/urls'

const props = defineProps({
  title: {
    type: String,
    default: 'Consultez vos procédures',
  },
  description: {
    type: String,
    default:
      "Pour accéder à la liste de vos dossiers et suivre l'avancement de vos procédures, vous devez être connecté.",
  },
  redirectTo: {
    type: String,
    default: '',
  },
})

const goToLogin = () => {
  if (props.redirectTo) {
    window.location.href = `${LOGIN_URL}?next=${encodeURIComponent(props.redirectTo)}`
  } else {
    window.location.href = LOGIN_URL
  }
}
</script>

<style scoped>
/* Ensure DSFR Button looks good inside the box */
.fr-btn {
  font-weight: 600;
}
</style>

