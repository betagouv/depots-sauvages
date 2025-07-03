<template>
  <div class="fr-container--sm">
    <div class="fr-bg--contrast">
      <div class="fr-p-4w">
        <section class="document-section fr-py-3w fr-px-2w fr-mb-4w fr-bg--g100">
          <h2 class="fr-h3 fr-mb-1w">Télécharger et compléter les documents</h2>
          <p>
            Vous trouverez ci-dessous des pièces de procédure
            <span class="fr-text--bold">pré-remplies</span>, à compléter avec les éléments manquants
            (charte graphique de la mairie, date et signature du rédacteur du document, etc.).
          </p>

          <h3 class="fr-h4 document-title fr-mt-3w">
            <span aria-hidden="true">📄</span> Documents disponibles
          </h3>
          <p>Vous pouvez télécharger les documents suivants :</p>
          <ul class="fr-mb-3w">
            <li>
              <a
                v-if="isOdtReady"
                :href="getDocConstatUrl(store.currentId)"
                class="fr-link fr-text--sm fr-link--download"
                :aria-disabled="!isOdtReady"
                :tabindex="!isOdtReady ? -1 : 0"
              >
                Télécharger le rapport de constatation
                <span v-if="docConstatSize">( .odt, {{ docConstatSize }})</span>
              </a>
              <span v-else class="fr-text--sm fr-text--disabled">
                Télécharger le rapport de constatation
                <span aria-live="polite"> – Chargement…</span>
              </span>
            </li>
            <li>
              <a
                v-if="isOdtReady"
                :href="getLettreInfoUrl(store.currentId)"
                class="fr-link fr-text--sm fr-link--download"
                :aria-disabled="!isOdtReady"
                :tabindex="!isOdtReady ? -1 : 0"
              >
                Télécharger la lettre d'information
                <span v-if="lettreInfoSize">( .odt, {{ lettreInfoSize }})</span>
              </a>
              <span v-else class="fr-text--sm fr-text--disabled">
                Télécharger la lettre d'information <span aria-live="polite"> – Chargement…</span>
              </span>
            </li>
          </ul>

          <div class="fr-mt-4w">
            <h4 class="fr-h4">Recevoir vos documents par e-mail</h4>
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
                {{ isSending ? "Les documents sont en cours d'envoi" : 'Envoyer par e-mail' }}
              </span>
            </DsfrButton>
          </div>
        </section>

        <section class="fr-mt-4w fr-bg--g100">
          <h2 class="fr-h3"><span aria-hidden="true">📌</span> Ce qu’il vous reste à faire</h2>

          <h3 class="fr-h4 fr-mb-2w">Avant d'entamer la procédure</h3>
          <p>
            Pour lancer officiellement une procédure à l'encontre de l'auteur présumé de ce dépôt
            sauvage :
          </p>
          <ul class="fr-mb-3w">
            <li>
              <span aria-hidden="true">📥</span> Récupérez le rapport de constatation et la lettre
              d'information par e-mail ;
            </li>
            <li>
              <span aria-hidden="true">✍️</span> Relisez, complétez et signez ces deux documents (ou
              faites-les signer par votre autorité compétente : maire ou personne habilitée à
              réaliser des constatations).
            </li>
          </ul>

          <div class="fr-alert fr-alert--info fr-alert--sm fr-mt-3w" role="status">
            <h4 class="fr-alert__title">Procédure administrative</h4>
            <ul class="fr-mb-0">
              <li>
                <span aria-hidden="true">📬</span> Envoyez la lettre d'information en recommandé
                avec accusé de réception à l'auteur présumé ;
              </li>
              <li>
                <span aria-hidden="true">🗂️</span> Conservez une copie de tous les documents pour
                vos archives ;
              </li>
              <li>
                <span aria-hidden="true">⏳</span> À la fin de la période du contradictoire (10
                jours minimum), contactez l'équipe
                <span class="fr-text--bold">Protect'Envi</span> pour être aidé pour rédiger la mise en
                demeure et l'amende administrative.
              </li>
            </ul>
          </div>

          <div class="fr-alert fr-alert--info fr-alert--sm fr-mt-3w" role="status">
            <h4 class="fr-alert__title">Procédure judiciaire</h4>
            <ul class="fr-mb-0">
              <li>
                <span aria-hidden="true">📝</span> Envoyez le rapport de constatation à la brigade ;
              </li>
              <li>
                <span aria-hidden="true">🧾</span> Prenez rendez-vous auprès de la brigade de
                gendarmerie ou du commissariat pour déposer plainte.
              </li>
            </ul>
          </div>
        </section>

        <section class="fr-p-4w fr-bg--g100">
          <h3 class="fr-h3">Ressources utiles</h3>
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
          <p>
            <span aria-hidden="true">👉</span> Retrouvez des conseils pratiques sur l'application à
            destination des élus, Gend'élus, accessible à tout le monde :
          </p>
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
          <h3 class="fr-h3">
            <span aria-hidden="true">✅</span> Vous avez terminé le module "Débuter une procédure"
          </h3>
          <p>Vous pouvez maintenant :</p>
          <ul>
            <li>
              <span aria-hidden="true">🔍</span> Retrouver de l'aide dans la section
              <a href="/accompagnement" rel="noreferrer noopener">Être accompagné</a>
            </li>
            <li>
              <span aria-hidden="true">🔁</span> Démarrer une nouvelle procédure si nécessaire
            </li>
          </ul>
        </section>

        <div class="fr-btns-group fr-btns-group--inline fr-btns-group--center fr-mt-4w">
          <button class="fr-btn fr-btn--tertiary" @click="goHome">Retour à l'accueil</button>
          <button class="fr-btn" @click="handleRestart">
            Démarrer une nouvelle procédure
            <span class="fr-icon-arrow-right-line" aria-hidden="true"></span>
          </button>
          <button class="fr-btn fr-btn--secondary" @click="goToAccompagnement">
            Demander un accompagnement
            <span class="fr-ml-1w fr-icon-arrow-right-line" aria-hidden="true"></span>
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
import { formatBytes, getFileSizeFromUrl } from '@/utils/files'
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'

const store = useSignalementStore()
const emit = defineEmits(['restart'])

const isOdtReady = ref<boolean>(false)
const isSending = ref<boolean>(false)
const email = ref<string>('')
const emailError = ref<string>('')
const emailSuccess = ref<string>('')
const docConstatSize = ref(null)
const lettreInfoSize = ref(null)

const errorId = 'email-error'
const successId = 'email-success'

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

const goToAccompagnement = () => {
  window.location.href = '/accompagnement'
}

// Control buttons delay
onMounted(async () => {
  const urlDocConstat = getDocConstatUrl(store.currentId)
  const urlLettreInfo = getLettreInfoUrl(store.currentId)

  const [rawSizeDocConstat, rawSizeLettreInfo] = await Promise.all([
    getFileSizeFromUrl(urlDocConstat),
    getFileSizeFromUrl(urlLettreInfo),
  ])

  docConstatSize.value = rawSizeDocConstat ? formatBytes(rawSizeDocConstat) : 'Taille inconnue'
  lettreInfoSize.value = rawSizeLettreInfo ? formatBytes(rawSizeLettreInfo) : 'Taille inconnue'

  // Simulation : rendre le bouton actif après 3s
  setTimeout(() => {
    isOdtReady.value = true
  }, 3000)
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
