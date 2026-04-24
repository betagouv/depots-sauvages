<template>
  <div class="login-invitation fr-py-8w">
    <div class="premium-box fr-p-6w text-center">
      <div class="icon-container fr-mb-3w">
        <v-icon name="ri-account-circle-line" scale="4" aria-hidden="true" />
      </div>
      <h2 class="fr-h2">Consultez vos procédures</h2>
      <p class="fr-text--lead fr-mb-4w">
        Pour accéder à la liste de vos dossiers et suivre l'avancement de vos procédures, vous devez
        être connecté.
      </p>
      <div class="fr-btns-group fr-btns-group--center">
        <DsfrButton
          label="Se connecter avec ProConnect"
          :icon="{ name: 'ri-login-box-line', class: 'fr-mr-1w' }"
          @click="goToLogin"
        />
      </div>
      <p class="fr-text--sm fr-mt-4w fr-mb-0">
        ProConnect est la solution de connexion sécurisée pour les agents de l'État et des
        collectivités.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LOGIN_URL } from '@/services/urls'

const goToLogin = () => {
  window.location.href = LOGIN_URL
}
</script>

<style scoped>
.premium-box {
  background-color: var(--background-alt-blue-france);
  border: 1px solid var(--border-default-blue-france);
  border-radius: 24px;
  max-width: 700px;
  margin: 0 auto;
  box-shadow: 0 12px 40px rgba(0, 0, 145, 0.08);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.premium-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 145, 0.12);
}

.icon-container {
  display: inline-flex;
  padding: 1.5rem;
  background: white;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.icon-container :deep(svg) {
  color: var(--text-label-blue-france);
}

.text-center {
  text-align: center;
}

/* Ensure DSFR Button looks good inside the box */
.fr-btn {
  font-weight: 600;
}
</style>
