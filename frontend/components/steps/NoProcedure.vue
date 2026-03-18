<template>
  <div class="no-procedure-step">
    <div class="fr-mb-4w">
      <p>
        Pour accéder à vos documents et poursuivre vos démarches, merci de
        <a
          :href="modifyUrl"
          class="fr-link fr-icon-external-link-line fr-link--icon-right"
          target="_blank"
          rel="noopener noreferrer"
          >mettre à jour votre procédure sur la plateforme Démarches Numériques</a
        >.
      </p>
      <DsfrAlert
        type="info"
        title="Note"
        description="Les formulaires de Protect'Envi évoluent régulièrement. Si vous avez rempli une version antérieure de la procédure, une mise à jour de certaines informations est nécessaire pour accéder à vos documents."
        small
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert } from '@gouvminint/vue-dsfr'

defineProps<{
  modifyUrl: string
}>()
</script>

<style scoped></style>
