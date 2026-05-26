<template>
  <PremiumBox
    title="Constatation enregistrée !"
    description="La constatation du dépôt sauvage a été enregistrée avec succès. Votre dossier de procédure est maintenant prêt pour les étapes suivantes."
    iconClass="fr-icon-checkbox-circle-fill"
    iconColor="#00875a"
  >
    <template #actions>
      <DsfrButton label="Accéder au suivi de la procédure" @click="$emit('goToSuivi')" />
      <DsfrButton secondary label="Retourner à mes procédures" @click="$emit('goToProcedures')" />
    </template>
  </PremiumBox>
</template>

<script setup lang="ts">
import PremiumBox from '@/components/shared/PremiumBox.vue'
import { DsfrButton } from '@gouvminint/vue-dsfr'

defineEmits<{
  (e: 'goToSuivi'): void
  (e: 'goToProcedures'): void
}>()
</script>
