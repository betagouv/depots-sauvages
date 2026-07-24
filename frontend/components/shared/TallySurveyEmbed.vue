<template>
  <div class="fr-mt-4w fr-mb-4w" style="text-align: left;">
    <p class="fr-text--sm fr-mb-1w fr-text-mention--grey" style="text-align: center;">
      <span class="fr-icon-chat-3-line fr-mr-1w" aria-hidden="true"></span>
      Donnez votre avis en 10 secondes
    </p>
    <iframe
      :data-tally-src="tallySrc"
      loading="lazy"
      width="100%"
      height="180"
      frameborder="0"
      marginheight="0"
      marginwidth="0"
      title="Questionnaire de satisfaction"
    ></iframe>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { loadTallyEmbeds } from '@/utils/tally'

const props = defineProps<{
  commune: string
  idDossier: number | string
}>()

const tallySrc = computed(() => {
  const params = new URLSearchParams({
    alignLeft: '1',
    hideTitle: '1',
    transparentBackground: '1',
    dynamicHeight: '1',
  })
  params.set('commune', props.commune)
  params.set('ID_dossier', String(props.idDossier))

  return `https://tally.so/embed/VLArqN?${params.toString()}`
})

onMounted(() => {
  loadTallyEmbeds()
})
</script>
