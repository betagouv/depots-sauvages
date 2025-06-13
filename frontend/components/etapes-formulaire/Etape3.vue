<template>
  <div class="fr-container--sm">
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
              <span class="fr-m-1w">Télécharger le rapport de constatation au format ODT</span>
            </DsfrButton>
            <DsfrButton
              :icon="{ name: 'ri-download-line', animation: isOdtReady ? undefined : 'spin' }"
              :disabled="!isOdtReady"
              @click="downloadLettreInfo"
            >
              <span class="fr-m-1w">Télécharger la lettre d'information au format ODT</span>
            </DsfrButton>
          </div>

          <div class="fr-mt-4w">
            <h4>Recevoir vos documents par e-mail</h4>
            <div class="fr-input-group">
              <label class="fr-label" for="email-input">
                Adresse électronique
                <span class="fr-hint-text">Format attendu : nom@domaine.fr</span>
              </label>
              <input
                class="fr-input"
                :class="{ 'fr-input--error': emailError }"
                id="email-input"
                v-model="email"
                type="email"
                :aria-describedby="emailInputDescribedBy || undefined"
                @input="clearEmailSuccessError"
                autocomplete="email"
              />
              <p v-if="emailError" class="fr-error-text" :id="errorId" role="alert">
                {{ emailError }}
              </p>
              <p v-if="emailSuccess" class="fr-valid-text" :id="successId" role="alert">
                {{ emailSuccess }}
              </p>
            </div>
            <DsfrButton
              class="fr-mt-2w"
              :icon="{ name: 'ri-mail-fill' }"
              :disabled="!isEmailValid || isSending"
              @click="sendEmail"
            >
              <span class="fr-m-1w">
                {{
                  isSending
                    ? "Les documents sont en cours d'envoi"
                    : 'Envoyer les documents par e-mail'
                }}
              </span>
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
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'

const store = useSignalementStore()
const emit = defineEmits(['restart'])

const isOdtReady = ref<boolean>(false)
const isSending = ref<boolean>(false)
const email = ref<string>('')
const emailError = ref<string>('')
const emailSuccess = ref<string>('')

const errorId = 'email-error'
const successId = 'email-success'

const downloadDocConstat = () => {
  window.open(getDocConstatUrl(store.currentId), '_blank')
}

const downloadLettreInfo = () => {
  window.open(getLettreInfoUrl(store.currentId), '_blank')
}

const isEmailValid = computed(() => {
  if (email.value.trim() === '') return false
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email.value)
})

const emailInputDescribedBy = computed(() => {
  if (emailError.value) return errorId
  if (emailSuccess.value) return successId
  return null
})

const clearEmailSuccessError = () => {
  emailError.value = ''
  emailSuccess.value = ''
}

const sendEmail = async () => {
  if (!isEmailValid.value) {
    emailError.value =
      "L'adresse e-mail saisie n'est pas valide. Vérifiez le format (ex. : nom@domaine.fr)."
    return
  }
  isSending.value = true
  emailError.value = ''
  emailSuccess.value = ''
  try {
    await createResource(getSendEmailUrl(store.currentId), { email: email.value })
    emailSuccess.value = `Un e-mail contenant les documents a été envoyé avec succès à l'adresse ${email.value}`
    email.value = ''
  } catch (error: any) {
    const messageServeur = error.response?.data?.error
    emailError.value = messageServeur
      ? `L'envoi a échoué : ${messageServeur}. Veuillez réessayer.`
      : "L'envoi a échoué. Vérifiez votre connexion ou réessayez dans quelques instants."
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
