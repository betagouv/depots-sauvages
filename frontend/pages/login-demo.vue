<template>
  <div v-if="bypassAuthEnabled" class="fr-container fr-py-8w">
    <div class="fr-grid-row fr-grid-row--center">
      <div class="fr-col-12 fr-col-md-6 fr-col-lg-5">
        <div class="fr-card fr-card--no-arrow fr-p-4w">
          <div class="fr-card__body">
            <h1 class="fr-h2 fr-mb-2w">Connexion à votre espace</h1>
            <p class="fr-text--sm fr-mb-4w text-muted">
              Saisissez votre adresse électronique pour vous connecter.
            </p>

            <form @submit.prevent="handleBypassLogin">
              <div class="fr-input-group fr-mb-3w">
                <label class="fr-label font-bold fr-mb-1w" for="input-email">
                  Adresse électronique
                </label>
                <input
                  id="input-email"
                  class="fr-input"
                  type="email"
                  placeholder="ex: nom.prenom@collectivite.fr"
                  v-model="emailInput"
                  required
                  :disabled="isLoggingIn"
                />
              </div>

              <div v-if="errorMessage" class="fr-alert fr-alert--error fr-alert--sm fr-mb-3w" role="alert">
                <p>{{ errorMessage }}</p>
              </div>

              <div class="fr-btns-group">
                <button
                  type="submit"
                  class="fr-btn fr-w-100 justify-center"
                  :disabled="!emailInput || isLoggingIn"
                >
                  <span v-if="isLoggingIn" class="spinner fr-mr-1w"></span>
                  {{ isLoggingIn ? 'Connexion en cours...' : 'Se connecter' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getBypassAuthConfig, loginBypassAuth } from '@/services/api'

const route = useRoute()
const bypassAuthEnabled = ref(false)
const emailInput = ref('')
const isLoggingIn = ref(false)
const errorMessage = ref('')

const handleBypassLogin = async () => {
  if (!emailInput.value) return
  isLoggingIn.value = true
  errorMessage.value = ''
  try {
    await loginBypassAuth(emailInput.value.trim().toLowerCase())
    // Redirect to dashboard or next url
    const nextPath = (route.query.next as string) || '/mes-procedures'
    window.location.href = nextPath
  } catch (error: any) {
    console.error('Login failed:', error)
    if (error && (error.detail || error.error)) {
      errorMessage.value = error.detail || error.error
    } else {
      errorMessage.value = "Adresse électronique inconnue ou non autorisée."
    }
  } finally {
    isLoggingIn.value = false
  }
}

onMounted(async () => {
  try {
    const config = await getBypassAuthConfig()
    if (config.enabled) {
      bypassAuthEnabled.value = true
    } else {
      // Redirect to homepage if bypass is disabled
      window.location.href = '/'
    }
  } catch (error) {
    console.warn('Authentication unavailable:', error)
    window.location.href = '/'
  }
})
</script>

<style scoped>
.fr-card {
  background-color: var(--background-alt-blue-france);
  border: 1px solid var(--border-default-blue-france);
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 0, 145, 0.06);
}

.font-bold {
  font-weight: 700;
}

.text-muted {
  color: var(--text-mention-grey);
}

.fr-w-100 {
  width: 100%;
}

.justify-center {
  justify-content: center;
}

/* Spinner animation */
.spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
