<template>
  <div>
    <p class="fr-mb-2w">
      Sans auteur identifié, la procédure administrative ne peut pas être initiée.
    </p>
    <p class="fr-mb-2w">
      Si la procédure judiciaire ou de nouveaux éléments permettent d'identifier un auteur, vous
      pourrez alors initier une procédure administrative.
    </p>
    <p v-if="modifyUrl" class="fr-mb-0">
      Vous pourrez alors
      <a
        :href="modifyUrl"
        class="fr-link fr-icon-external-link-line fr-link--icon-right"
        target="_blank"
        rel="nopener"
      >
        modifier les informations sur votre démarche numérique
      </a>
      pour mettre à jour vos documents.
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modifyUrl?: string | null
}>()
</script>
