<template>
  <div class="premium-block-container fr-py-8w text-center">
    <div class="premium-box fr-p-6w custom-width">
      <div v-if="iconClass" class="icon-container fr-mb-3w">
        <span
          :class="[iconClass, 'custom-icon-size']"
          :style="{ color: iconColor }"
          aria-hidden="true"
        ></span>
      </div>
      <h2 v-if="title" class="fr-h2">{{ title }}</h2>
      <p v-if="description" class="fr-text--lead fr-mb-4w">
        {{ description }}
      </p>

      <slot />

      <div class="fr-btns-group fr-btns-group--center">
        <slot name="actions" />
      </div>

      <div v-if="$slots.footer" class="fr-mt-4w">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  title: {
    type: String,
    default: '',
  },
  description: {
    type: String,
    default: '',
  },
  iconClass: {
    type: String,
    default: '',
  },
  iconColor: {
    type: String,
    default: 'var(--text-label-blue-france)',
  },
})
</script>

<style scoped>
.custom-width {
  max-width: 700px;
  margin: 0 auto;
}

.icon-container {
  display: inline-flex;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 145, 0.08);
}

.custom-icon-size {
  --icon-size: 3.5rem;
}

.text-center {
  text-align: center;
}
</style>
