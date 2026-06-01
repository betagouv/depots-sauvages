<template>
  <!-- 1. Banner style (prominent callout) -->
  <div v-if="type === 'banner'" class="premium-alert-banner fr-p-4w fr-mb-4w">
    <div class="fr-grid-row fr-grid-row--middle fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-8 banner-content">
        <div v-if="iconClass" class="banner-icon-container">
          <span :class="[iconClass, 'fr-icon--lg', 'banner-icon']" aria-hidden="true"></span>
        </div>
        <div>
          <h3 v-if="title" class="fr-h4 fr-mb-1v font-premium">{{ title }}</h3>
          <p v-if="description" class="fr-mb-0 fr-text--sm text-muted">
            <span v-html="description"></span>
          </p>
        </div>
      </div>
      <div v-if="buttonText" class="fr-col-12 fr-col-md-4 text-md-right">
        <router-link
          v-if="buttonTo"
          :to="buttonTo"
          class="fr-btn fr-btn--secondary hover-premium-btn"
        >
          <slot name="button-icon"></slot>
          {{ buttonText }}
        </router-link>
        <a
          v-else
          href="#"
          @click.prevent="$emit('click')"
          class="fr-btn fr-btn--secondary hover-premium-btn"
        >
          <slot name="button-icon"></slot>
          {{ buttonText }}
        </a>
      </div>
    </div>
  </div>

  <!-- 2. Discreet style (light line callout) -->
  <div v-else class="premium-callout-discreet fr-mb-4w">
    <span v-if="iconClass" :class="[iconClass, 'icon-accent fr-mr-1w']" aria-hidden="true"></span>
    <span class="callout-content">
      {{ description }}
      <strong>
        <router-link v-if="buttonTo" :to="buttonTo" class="callout-link fr-ml-1v">
          {{ buttonText }}
        </router-link>
        <a v-else href="#" @click.prevent="$emit('click')" class="callout-link fr-ml-1v">
          {{ buttonText }}
        </a>
      </strong>
    </span>
  </div>
</template>

<script setup lang="ts">
defineProps({
  type: {
    type: String,
    default: 'discreet', // 'discreet' or 'banner'
  },
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
  buttonText: {
    type: String,
    default: '',
  },
  buttonTo: {
    type: String,
    default: '',
  },
})

defineEmits(['click'])
</script>

<style scoped>
.font-premium {
  font-weight: 700;
  color: var(--text-title-blue-france);
}

.text-muted {
  color: var(--text-mention-grey);
}

@media (min-width: 768px) {
  .text-md-right {
    text-align: right;
  }
}

/* Discreet style CSS */
.premium-callout-discreet {
  display: flex;
  align-items: center;
  background-color: var(--background-alt-grey);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  border-left: 3px solid var(--border-default-grey);
}

.icon-accent {
  color: var(--text-active-blue-france);
  flex-shrink: 0;
}

.callout-link {
  color: var(--text-action-high-blue-france);
  transition: color 0.2s ease;
}

.callout-link:hover {
  color: var(--text-active-blue-france);
}
</style>
