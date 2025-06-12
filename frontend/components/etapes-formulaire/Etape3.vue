<template>
  <div class="fr-container--sm">
    <DsfrAlert type="success" title="Merci pour votre signalement" />

    <div class="fr-bg--contrast fr-mt-3w">
      <div class="confirmation-content fr-p-4w">
        <section class="confirmation-section fr-mb-4w fr-pb-4w">
          <p>
            Vous trouverez ci-dessous des pièces de procédures pré-remplies, à compléter avec les
            éléments manquants (charte graphique de la mairie, date et signature du rédacteur du
            document, etc.).
          </p>
          <p>
            Si vous souhaitez déposer plainte, pensez à apporter ce rapport de constatation en
            brigade.
          </p>
          <p>
            Ce rapport est nécessaire pour initier une procédure administrative (voir conseils et
            aide à la rédaction d'une procédure administrative en bas de page).
          </p>
        </section>

        <section class="document-section fr-p-4w fr-mb-4w fr-mt-4w">
          <h3 class="document-title">📄 Documents disponibles</h3>
          <p>Vous pouvez télécharger les documents suivants :</p>
          <div class="fr-btns-group fr-btns-group--block fr-btns-group--inline-md">
            <DsfrButton
              :icon="{ name: 'ri-download-line', animation: isOdtReady ? undefined : 'spin' }"
              :disabled="!isOdtReady"
              @click="downloadDocConstat"
            >
              <span class="fr-m-2w">Télécharger le rapport de constatation au format ODT</span>
            </DsfrButton>
            <DsfrButton
              :icon="{ name: 'ri-download-line', animation: isOdtReady ? undefined : 'spin' }"
              :disabled="!isOdtReady"
              @click="downloadLettreInfo"
            >
              <span class="fr-m-2w">Télécharger la lettre d'information au format ODT</span>
            </DsfrButton>
          </div>

          <div class="fr-mt-4w">
            <h4>Recevoir les documents par email</h4>
            <div class="fr-input-group">
              <label class="fr-label" for="email-input"> Adresse email </label>
              <input
                class="fr-input"
                :class="{ 'fr-input--error': emailError }"
                id="email-input"
                v-model="email"
                type="email"
                placeholder="votre@email.com"
              />
              <p v-if="emailError" class="fr-error-text">
                {{ emailError }}
              </p>
            </div>
            <DsfrButton
              class="fr-mt-2w"
              :icon="{ name: 'fr-icon-mail-fill', animation: isSending ? 'spin' : undefined }"
              :disabled="!isEmailValid || isSending"
              @click="sendEmail"
            >
              Envoyer par email
            </DsfrButton>
          </div>
        </section>

        <section class="confirmation-section fr-mb-4w fr-pb-4w">
          <h3>📑 Procédure administrative</h3>
          <p>
            Si vous souhaitez plus d'informations concernant la procédure administrative rendez-vous
            <a
              href="https://acdechets.smartidf.services/aide-verbalisation"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
            >
              sur le guide ACDéchets de la Région Île de France
            </a>
            pour vous aider pas à pas.
          </p>
        </section>

        <section class="confirmation-section fr-mb-4w fr-pb-4w">
          <h3>🙋🏻‍♂️ Conseils pratiques</h3>
          <p>
            Retrouvez des conseils pratiques sur l'application à destination des élus, Gend'élus:
          </p>
          <ul>
            <li>
              <a
                href="https://play.google.com/store/apps/details?id=com.gendelus&hl=fr&pli=1"
                class="fr-link fr-icon-external-link-line fr-link--icon-right"
                target="_blank"
                rel="noreferrer noopener"
              >
                Télécharger l'application sur le Play Store
              </a>
            </li>
            <li>
              <a
                href="https://apps.apple.com/fr/app/gend%C3%A9lus/id6444316373"
                class="fr-link fr-icon-external-link-line fr-link--icon-right"
                target="_blank"
                rel="noreferrer noopener"
              >
                Télécharger l'application sur l'App store
              </a>
            </li>
          </ul>
        </section>

        <div class="fr-mt-5w fr-text--center">
          <button class="fr-btn" @click="handleRestart">
            Faire un nouveau signalement
            <span class="fr-icon-arrow-right-line" aria-hidden="true"></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { createResource } from '@/services/api'
import { getDocConstatUrl, getLettreInfoUrl, getSendEmailUrl } from '@/services/urls'
import { useSignalementStore } from '@/stores/signalement'
import { DsfrAlert, DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'

const store = useSignalementStore()
const emit = defineEmits(['restart'])

// Loading states
const isOdtReady = ref(false)
const isSending = ref(false)
const email = ref('')
const emailError = ref('')

// Email validation
const isEmailValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email.value)
})

// Create computed properties for document URLs
const docConstatUrl = computed(() => getDocConstatUrl(store.currentId))
const lettreInfoUrl = computed(() => getLettreInfoUrl(store.currentId))

// Download functions
const downloadDocConstat = () => {
  window.open(getDocConstatUrl(store.currentId), '_blank')
}

const downloadLettreInfo = () => {
  window.open(getLettreInfoUrl(store.currentId), '_blank')
}

// Email sending function
const sendEmail = async () => {
  if (!isEmailValid.value) {
    emailError.value = 'Veuillez entrer une adresse email valide'
    return
  }

  isSending.value = true
  emailError.value = ''

  try {
    await createResource(getSendEmailUrl(store.currentId), { email: email.value })
    alert('Les documents ont été envoyés avec succès à votre adresse email')
    email.value = ''
  } catch (error: any) {
    emailError.value = error.response?.data?.error || "Erreur lors de l'envoi de l'email"
  } finally {
    isSending.value = false
  }
}

const handleRestart = () => {
  emit('restart')
}

// Control buttons delay
onMounted(() => {
  setTimeout(() => {
    isOdtReady.value = true
  }, 3000) // Enable after 3 seconds
})
</script>

<style scoped>
.confirmation-content {
  background: var(--background-contrast-grey);
}

.confirmation-section {
  border-bottom: 1px solid var(--border-default-grey);
}

.confirmation-section:last-of-type {
  border: none;
}

.document-section {
  background-color: #f5f5fe;
}

.document-title {
  color: #000091;
}
</style>
