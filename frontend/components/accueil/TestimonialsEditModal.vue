<template>
  <DsfrModal
    :opened="opened"
    title="Modifier les témoignages"
    :is-alert="true"
    @close="$emit('close')"
  >
    <form @submit.prevent="submitForm" class="fr-container--fluid fr-p-0">
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-mb-2w">
          <div class="fr-input-group">
            <label class="fr-label" for="testimonials-title">Titre de la section</label>
            <input
              v-model="localTitle"
              class="fr-input"
              type="text"
              id="testimonials-title"
              required
              placeholder="Ex: Ils ont agi avec Protect'Envi"
            />
          </div>
        </div>

        <div
          v-for="(item, index) in localTestimonials"
          :key="index"
          class="fr-col-12 fr-col-md-6 fr-mb-2w"
        >
          <div class="testimonial-edit-card fr-p-2w">
            <h3 class="fr-text--lead fr-mb-1w">Témoignage {{ index + 1 }}</h3>

            <div class="fr-input-group fr-mb-2w">
              <label class="fr-label" :for="'testimonial-quote-' + index">Citation</label>
              <textarea
                v-model="item.quote"
                class="fr-input"
                :id="'testimonial-quote-' + index"
                required
                rows="4"
                placeholder="Le texte du témoignage..."
              ></textarea>
            </div>

            <div class="fr-input-group fr-mb-2w">
              <label class="fr-label" :for="'testimonial-author-' + index">Auteur</label>
              <input
                v-model="item.author"
                class="fr-input"
                type="text"
                :id="'testimonial-author-' + index"
                required
                placeholder="Ex: Philippe Barneron"
              />
            </div>

            <div class="fr-input-group fr-mb-0">
              <label class="fr-label" :for="'testimonial-source-' + index"
                >Source / Description</label
              >
              <input
                v-model="item.source"
                class="fr-input"
                type="text"
                :id="'testimonial-source-' + index"
                required
                placeholder="Ex: Maire de Peyrins (26) — commune de 2 700 habitants"
              />
            </div>
          </div>
        </div>

        <div class="fr-col-12 fr-mt-3w text-right">
          <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--right">
            <li>
              <button type="button" class="fr-btn fr-btn--secondary" @click="$emit('close')">
                Annuler
              </button>
            </li>
            <li>
              <button type="submit" class="fr-btn">Enregistrer</button>
            </li>
          </ul>
        </div>
      </div>
    </form>
  </DsfrModal>
</template>

<script setup lang="ts">
import { DsfrModal } from '@gouvminint/vue-dsfr'
import { ref, watch } from 'vue'

interface TestimonialItem {
  quote: string
  author: string
  source: string
}

const props = defineProps<{
  opened: boolean
  title: string
  testimonials: TestimonialItem[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: { title: string; testimonials: TestimonialItem[] }): void
}>()

const localTitle = ref('')
const localTestimonials = ref<TestimonialItem[]>([])

watch(
  () => props.opened,
  (isOpened) => {
    if (isOpened) {
      localTitle.value = props.title
      // Deep copy
      localTestimonials.value = props.testimonials.map((t) => ({ ...t }))
    }
  },
  { immediate: true }
)

const submitForm = () => {
  emit('save', {
    title: localTitle.value,
    testimonials: localTestimonials.value,
  })
}
</script>

<style scoped>
.testimonial-edit-card {
  border: 1px solid var(--border-default-grey);
  border-radius: 4px;
  background-color: var(--background-alt-grey);
}
</style>
