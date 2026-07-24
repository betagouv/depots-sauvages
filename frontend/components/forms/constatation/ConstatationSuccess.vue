<template>
  <PremiumBox
    title="Constatation enregistrée !"
    description="Vos documents de procédure ont été pré-remplis automatiquement. Vous pouvez passer aux prochaines étapes."
    iconClass="fr-icon-checkbox-circle-fill"
    iconColor="#00875a"
  >
    <DsfrAlert type="info" small class="fr-mb-4w" style="text-align: left;">
      <p class="fr-mb-0">
        Le(s) document(s) doivent être signés par la personne habilitée pour avoir une valeur
        juridique.
      </p>
    </DsfrAlert>

    <template #actions>
      <DsfrButton label="Accéder aux documents sur mon suivi de procédure" @click="$emit('goToSuivi')" />
    </template>

    <template #footer>
      <router-link v-if="constatationId" :to="`/constatation/${constatationId}`" class="fr-link">
        Modifier la constatation
      </router-link>

      <TallySurveyEmbed v-if="constatationId && commune" :commune="commune" :id-dossier="constatationId" />
    </template>
  </PremiumBox>
</template>

<script setup lang="ts">
import PremiumBox from '@/components/shared/PremiumBox.vue'
import TallySurveyEmbed from '@/components/shared/TallySurveyEmbed.vue'
import { DsfrAlert, DsfrButton } from '@gouvminint/vue-dsfr'

defineProps<{
  constatationId?: number | null
  commune?: string | null
}>()

defineEmits<{
  (e: 'goToSuivi'): void
  (e: 'goToProcedures'): void
}>()
</script>
