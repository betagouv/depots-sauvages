<template>
  <div class="fr-container--sm">
    <div class="fr-bg--contrast fr-mt-3w">
      <div class="fr-p-4w">
        <section class="fr-callout fr-callout--grey fr-mt-3w fr-mb-3w">
          <p>
            Vous trouverez ci-dessous des pièces de procédure <span class="fr-text--bold">pré-remplies</span>, à compléter avec les éléments manquants (charte graphique de la mairie, date et signature du rédacteur du document, etc.).
          </p>
          <p>
            Si vous envisagez de déposer plainte, <span class="fr-text--bold">apportez le rapport de constatation</span> en brigade.
          </p>
          <p>
            Ce rapport est également <span class="fr-text--bold">indispensable pour lancer une procédure administrative</span>. Des conseils et une aide à la rédaction sont disponibles en bas de page.
          </p>
        </section>

        <section class="document-section fr-p-4w fr-mt-4w fr-mb-4w">
          <h3 class="document-title"><span aria-hidden="true">📄</span> Documents disponibles</h3>
          <p>Vous pouvez télécharger les documents suivants :</p>
          <ul class="fr-btns-group fr-btns-group--block fr-btns-group--inline-md">
            <li>
              <DsfrButton
                :icon="{ name: 'ri-download-line', animation: isOdtReady ? undefined : 'spin' }"
                :disabled="!isOdtReady"
                @click="downloadDocConstat"
              >
                <span class="fr-m-1w">Télécharger le rapport de constatation au format ODT</span>
              </DsfrButton>
            </li>
           <li>
             <DsfrButton
               :icon="{ name: 'ri-download-line', animation: isOdtReady ? undefined : 'spin' }"
               :disabled="!isOdtReady"
               @click="downloadLettreInfo"
             >
               <span class="fr-m-1w">Télécharger la lettre d'information au format ODT</span>
             </DsfrButton>
           </li>
          </ul>

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

        <section class="fr-p-4w fr-mt-4w fr-bg--g100">
          <h3 class="fr-h3"><span aria-hidden="true">📌</span> Étapes suivantes</h3>
          <section class="fr-bg--g100">
            <h4 class="fr-h3 fr-mb-2w">Étapes à effectuer avant d'entamer la procédure</h4>
            <p>Pour lancer officiellement une procédure à l'encontre de l'auteur présumé de ce dépôt sauvage :</p>
            <ul class="fr-mb-3w">
              <li><span aria-hidden="true">📥</span> Récupérez le rapport de constatation et la lettre d'information par e-mail ;</li>
              <li><span aria-hidden="true">✍️</span> Relisez, complétez et signez ces deux documents (ou faites-les signer par votre autorité compétente : maire ou personne habilitée à réaliser des constatations).</li>
            </ul>

            <div class="fr-alert fr-alert--info fr-alert--sm fr-mt-3w" role="status">
              <h4 class="fr-alert__title">Procédure administrative</h4>
              <ul class="fr-mb-0">
                <li><span aria-hidden="true">📬</span> Envoyez la lettre d'information en recommandé avec accusé de réception à l'auteur présumé du dépôt ;</li>
                <li><span aria-hidden="true">🗂️</span> Conservez une copie de tous les documents pour vos archives ;</li>
                <li><span aria-hidden="true">⏳</span> À la fin de la période du contradictoire (10 jours minimum), contactez l'équipe <span class="fr-text--bold">Protect'Envi</span> pour être aidé dans la rédaction de la suite (mise en demeure et amende administrative).</li>
              </ul>
            </div>

            <div class="fr-alert fr-alert--info fr-alert--sm fr-mt-3w" role="status">
              <h4 class="fr-alert__title">Procédure judiciaire</h4>
              <ul class="fr-mb-0">
                <li><span aria-hidden="true">📝</span> Envoyez le rapport de constatation.</li>
                <li><span aria-hidden="true">🧾</span> Prenez rendez-vous auprès de la brigade de gendarmerie ou du commissariat de police pour déposer plainte.</li>
              </ul>
            </div>
          </section>

          <p class="fr-mt-3w">
            <span aria-hidden="true">👉</span> Pour un accompagnement pas à pas, consultez le
            <a
              href="https://acdechets.smartidf.services/aide-verbalisation"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
              rel="noopener"
            >
              guide ACDéchets de la Région Île-de-France
            </a>
          </p>
        </section>

        <section class="fr-p-4w fr-bg--g100">
          <h3 class="fr-h3 fr-mb-2w">Conseils pratiques</h3>
          <p>Retrouvez des conseils pratiques sur l'application à destination des élus, Gend'élus :</p>
          <ul>
            <li>
              <a
                href="https://play.google.com/store/apps/details?id=com.gendelus&hl=fr&pli=1"
                class="fr-link fr-icon-external-link-line fr-link--icon-right"
                target="_blank"
                rel="noreferrer noopener"
              >
                Télécharger sur le Play Store
              </a>
            </li>
            <li>
              <a
                href="https://apps.apple.com/fr/app/gend%C3%A9lus/id6444316373"
                class="fr-link fr-icon-external-link-line fr-link--icon-right"
                target="_blank"
                rel="noreferrer noopener"
              >
                Télécharger sur l’App Store
              </a>
            </li>
          </ul>
        </section>

        <section class="fr-p-4w fr-bg--g100">
          <h3 class="fr-h3"><span aria-hidden="true">✅</span> Vous avez terminé le module "Débuter une procédure"</h3>
          <p>Vous pouvez maintenant :</p>
          <ul>
            <li><span aria-hidden="true">🔍</span> Retrouver de l'aide dans la section
              <a
                href="/accompagnement"
                rel="noreferrer noopener"
              >
                Être accompagné ;
              </a>
            </li>
            <li><span aria-hidden="true">🔁</span> Démarrer une nouvelle procédure si nécessaire</li>
          </ul>
        </section>

        <div class="fr-btns-group fr-btns-group--inline fr-btns-group--center fr-mt-4w">
          <button class="fr-btn fr-btn--secondary" @click="goHome">
            Retour à l'accueil
          </button>
          <button class="fr-btn" @click="handleRestart">
            Démarrer une nouvelle procédure
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

const goHome = () => {
  window.location.href = '/'
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
