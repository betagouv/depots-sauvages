<template>
  <div class="confirmation-container">
    <DsfrAlert type="success" title="Merci pour votre signalement" />

    <div class="confirmation-content">
      <section class="confirmation-section">
        <p>
          Vous trouverez ci-dessous votre rapport de constatation pré-rempli, à compléter avec les éléments manquants (charte graphique de la mairie, date et signature du rédacteur du document, etc.). Ce rapport est nécessaire pour initier une procédure administrative (voir conseils et aide à la rédaction d’une procédure administrative en bas de page).
          Si vous souhaitez déposer plainte, pensez à apporter ce rapport de constatation en brigade.
        </p>
      </section>

      <section class="confirmation-section document-section">
        <div class="document-header">
          <span class="document-icon">📄</span>
          <h3 class="document-title">Document disponible</h3>
        </div>
        <p>Le document récapitulatif de votre signalement est prêt, vous pouvez le télécharger:</p>

        <button
          class="fr-btn action-button download-button"
          @click="downloadDocument"
          :disabled="isDownloading"
        >
          <span class="fr-icon-download-line" aria-hidden="true"></span>
          {{ isDownloading ? 'Téléchargement...' : 'Télécharger le document' }}
        </button>
      </section>

      <section class="confirmation-section">
        <h3>📞 Demandez conseil à un enquêteur environnement</h3>
        <p>
          Vous avez une question, besoin d'un renseignement ou d'un conseil spécifique ? Contactez
          un gendarme spécialisé (Enquêteur environnement) via
          <a
            href="#"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
          >
            ProtectEnvi sur Tchap
          </a>
        </p>
        <p>Nous nous engageons à vous répondre le plus rapidement possible.</p>
      </section>

      <section class="confirmation-section">
        <h3>📑 Procédure administrative</h3>
        <p>
          Si vous souhaitez plus d'informations concernant la procédure administrative rendez-vous
          <a
            href="#"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
          >
            sur le guide pas à pas
          </a>
          de la Région Île de France (ACDéchets).
        </p>
      </section>

      <section class="confirmation-section">
        <h3>🙋🏻‍♂️ Conseils pratiques</h3>
        <p>
          Retrouvez des conseils pratiques sur l'application à destination des élus :
          <a
            href="#"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
          >
            Gend'Elu
          </a>
        </p>
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
import { getDocumentUrl } from '@/services/api'
import { useSignalementStore } from '@/stores/signalement'
import { computed, ref } from 'vue'

const store = useSignalementStore()
const emit = defineEmits(['restart'])
const isDownloading = ref(false)

// Create a computed property for the document URL
const documentUrl = computed(() => getDocumentUrl(store.currentId))

// Function to handle document download
const downloadDocument = () => {
  window.open(documentUrl.value, '_blank')
}

// Function to handle restart
const handleRestart = () => {
  emit('restart')
}
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
}

.download-button .fr-icon-download-line {
  margin-right: 0.5rem;
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
