<template>
  <div class="confirmation-container">
    <DsfrAlert type="success" title="Merci pour votre signalement" />

    <div class="confirmation-content">
      <section class="confirmation-section">
        <p>
          Vous trouverez ci-dessous votre rapport de constatation pré-rempli, à compléter avec les
          éléments manquants (charte graphique de la mairie, date et signature du rédacteur du
          document, etc.).
        </p>
        <p>
          Si vous souhaitez déposer plainte, pensez à apporter ce rapport de constatation en
          brigade.
        </p>
        <p>
          Ce rapport est nécessaire pour initier une procédure administrative (voir conseils et aide
          à la rédaction d'une procédure administrative en bas de page).
        </p>
      </section>

      <section class="confirmation-section document-section">
        <div class="document-header">
          <span class="document-icon">📄</span>
          <h3 class="document-title">Document disponible</h3>
        </div>
        <p>Vous pouvez télécharger votre rapport de constatation :</p>

        <DsfrButton
          class="action-button download-button"
          :icon="{ name: 'ri-download-line', animation: isPdfReady ? undefined : 'spin' }"
          :disabled="!isPdfReady"
          @click="downloadDocument('pdf')"
        >
          Télécharger le document au format PDF
        </DsfrButton>
        <DsfrButton
          class="action-button download-button"
          :icon="{ name: 'ri-download-line', animation: isOdtReady ? undefined : 'spin' }"
          :disabled="!isOdtReady"
          @click="downloadDocument('odt')"
        >
          Télécharger le document au format ODT
        </DsfrButton>
      </section>

      <section class="confirmation-section">
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

      <section class="confirmation-section">
        <h3>🙋🏻‍♂️ Conseils pratiques</h3>
        <p>Retrouvez des conseils pratiques sur l'application à destination des élus, Gend'élus:</p>
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

      <!-- Restart button with updated styling -->
      <div class="action-buttons">
        <button class="fr-btn action-button restart-button" @click="handleRestart">
          Faire un nouveau signalement
          <span class="fr-icon-arrow-right-line" aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getDocumentUrl } from '@/services/urls'
import { useSignalementStore } from '@/stores/signalement'
import { computed, onMounted, ref } from 'vue'

const store = useSignalementStore()
const emit = defineEmits(['restart'])

// Loading states
const isPdfReady = ref(false)
const isOdtReady = ref(false)

// Create computed properties for both formats
const documentUrl = computed(() => getDocumentUrl(store.currentId))
const pdfUrl = computed(() => getDocumentUrl(store.currentId, 'pdf'))

// Download function
const downloadDocument = (format: 'pdf' | 'odt') => {
  window.open(getDocumentUrl(store.currentId, format), '_blank')
}

const handleRestart = () => {
  emit('restart')
}

// Control buttons delay
onMounted(() => {
  setTimeout(() => {
    isOdtReady.value = true
  }, 3000) // Enable after 3 seconds

  setTimeout(() => {
    isPdfReady.value = true
  }, 6000) // Enable after 6 seconds
})
</script>

<style scoped>
.confirmation-container {
  max-width: 800px;
  margin: 0 auto;
}

.confirmation-content {
  background: var(--background-contrast-grey);
  padding: 2rem;
  border-radius: 8px;
  text-align: left;
  margin-top: 1.5rem;
}

.confirmation-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-default-grey);
}

.confirmation-section:last-of-type {
  margin-bottom: 1.5rem;
  padding-bottom: 0;
  border: none;
}

.document-section {
  background-color: #f5f5fe;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 2rem;
  margin-bottom: 2rem;
  border: 1px solid #e3e3fd;
}

.document-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.document-icon {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

.document-title {
  margin: 0;
  color: #000091;
}

h3 {
  color: var(--text-title-grey);
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

p {
  line-height: 1.5;
  margin: 0.5rem 0;
}

/* Common button styling */
.action-button {
  background-color: #000091;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  display: inline-flex;
  align-items: center;
  font-weight: 500;
}

.action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.download-button {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-buttons {
  margin-top: 2rem;
  text-align: center;
}

.restart-button .fr-icon-arrow-right-line {
  margin-left: 0.5rem;
}

@media (max-width: 768px) {
  .confirmation-container {
    padding: 0 0.5rem;
  }
  .confirmation-content {
    padding: 1.5rem;
  }
}
</style>
