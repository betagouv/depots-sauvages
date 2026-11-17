<template>
  <DsfrModal
    :opened="opened"
    title="Attention : Conflit de modification"
    :actions="modalActions"
    @close="emit('close')"
  >
    <div class="fr-p-1w">
      <div class="fr-alert fr-alert--warning fr-mb-3w">
        <h3 class="fr-alert__title">Ce dossier a été modifié par un autre utilisateur</h3>
        <p class="fr-text--sm fr-mb-0">
          <strong>{{ updatedBy }}</strong> a enregistré des modifications sur cette procédure entre-temps.
        </p>
      </div>

      <p class="fr-text--sm">
        Afin d'éviter d'écraser involontairement le travail de votre collègue, vos modifications locales ont été préservées sur votre écran.
      </p>

      <ul class="fr-text--sm">
        <li>
          <strong>Recharger la version serveur (recommandé) :</strong> Récupère la dernière version à jour enregistrée par votre collègue. Vos modifications locales non enregistrées seront remplacées.
        </li>
        <li>
          <strong>Conserver et forcer l'enregistrement :</strong> Écrase la version de votre collègue avec vos saisies actuelles.
        </li>
      </ul>
    </div>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    opened: boolean
    updatedBy?: string
    message?: string
  }>(),
  {
    updatedBy: 'Un autre utilisateur',
    message: 'Ce dossier a été modifié par un autre utilisateur entre-temps.',
  }
)

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'reload'): void
  (e: 'force-save'): void
}>()

const modalActions = computed(() => [
  {
    label: 'Recharger la version à jour',
    onClick: () => emit('reload'),
  },
  {
    label: 'Conserver mes saisies et écraser',
    secondary: true,
    onClick: () => emit('force-save'),
  },
])
</script>
