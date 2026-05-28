<template>
  <div class="step-update-dn">
    <DsfrAlert type="success" title="Identification réussie" class="fr-mb-4w">
      <p class="fr-mb-1w">
        Vous avez identifié l'auteur. Vous pouvez maintenant
        <router-link :to="modifyUrl">modifier la constatation</router-link>
        pour y ajouter l'identité de l'auteur.
      </p>
    </DsfrAlert>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modifyUrl: string
}>()
</script>

<style scoped></style>
