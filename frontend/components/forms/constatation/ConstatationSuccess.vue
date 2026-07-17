<template>
  <PremiumBox
    title="Constatation enregistrée !"
    description="La constatation du dépôt sauvage a bien été enregistrée. Vous pouvez maintenant accéder au suivi de procédure pour consulter les prochaines étapes."
    iconClass="fr-icon-checkbox-circle-fill"
    iconColor="#00875a"
  >
    <DsfrCallout
      title="Attention la procédure n'est pas terminée !"
      class="fr-mb-4w fr-callout--yellow-tournesol"
      style="text-align: left;"
    >
      <p>
        Le rapport de constatation généré devra être signé par l'autorité compétente pour avoir une
        valeur juridique.
      </p>
    </DsfrCallout>

    <template #actions>
      <DsfrButton label="Consulter les prochaines étapes sur mon suivi de procédure" @click="$emit('goToSuivi')" />
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
import { DsfrButton, DsfrCallout } from '@gouvminint/vue-dsfr'

defineProps<{
  constatationId?: number | null
  commune?: string | null
}>()

defineEmits<{
  (e: 'goToSuivi'): void
  (e: 'goToProcedures'): void
}>()
</script>
