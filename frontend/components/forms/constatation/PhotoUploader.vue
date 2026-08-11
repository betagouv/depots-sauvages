<template>
  <div class="photo-uploader">
    <label v-if="label" class="fr-label">
      {{ label }}
      <span v-if="hint" class="fr-hint-text">{{ hint }}</span>
    </label>

    <div class="uppy-container fr-mt-2w">
      <Dashboard
        :uppy="uppy"
        :props="{
          plugins: [],
          theme: 'light',
          height: height,
          showRemoveButtonAfterComplete: true,
          note: note,
        }"
      />
    </div>

    <div v-if="modelValue.length > 0" class="fr-mt-3w">
      <p class="fr-text--sm fr-mb-2w">
        <strong>{{ modelValue.length }} photo(s) conservée(s) :</strong>
      </p>
      <div class="photo-preview-grid">
        <div v-for="(photo, index) in modelValue" :key="index" class="photo-preview-item">
          <img :src="photo" alt="Aperçu photo" class="photo-thumbnail" />
          <button
            type="button"
            class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-icon-delete-line delete-photo-btn"
            title="Supprimer la photo"
            @click="removePhoto(index)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Compressor from '@uppy/compressor'
import Uppy from '@uppy/core'
import FrenchLocale from '@uppy/locales/lib/fr_FR'
import Dashboard from '@uppy/vue/dashboard'
import { onBeforeUnmount } from 'vue'

import '@uppy/core/css/style.min.css'
import '@uppy/dashboard/css/style.min.css'

const props = withDefaults(
  defineProps<{
    modelValue?: string[]
    maxFileSizeMb?: number
    label?: string
    hint?: string
    note?: string
    height?: number
  }>(),
  {
    modelValue: () => [],
    maxFileSizeMb: 20,
    label: '',
    hint: '',
    note: "JPG/PNG jusqu'à 20 Mo par photo",
    height: 180,
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
  (e: 'change'): void
}>()

const maxSizeBytes = props.maxFileSizeMb * 1024 * 1024

const uppy = new Uppy({
  id: 'photo-uppy-uploader',
  autoProceed: true,
  locale: {
    ...FrenchLocale,
    strings: {
      ...FrenchLocale.strings,
      dropPasteImportBoth: 'Prendre une photo ou %{browse}',
      dropPasteFiles: 'Sélectionner des photos ou %{browse}',
      browseFiles: 'naviguer dans vos fichiers',
    },
  },
  restrictions: {
    maxFileSize: maxSizeBytes,
    allowedFileTypes: ['image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif'],
  },
}).use(Compressor, {
  quality: 0.8,
  maxWidth: 1600,
  maxHeight: 1600,
})

const fileToBase64 = (file: File | Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = (err) => reject(err)
    reader.readAsDataURL(file)
  })
}

uppy.on('file-added', async (file) => {
  try {
    if (file.data) {
      const base64 = await fileToBase64(file.data)
      const newList = [...props.modelValue, base64]
      emit('update:modelValue', newList)
      emit('change')
    }
  } catch (err) {
    console.error("Erreur d'encodage de la photo Uppy:", err)
  }
})

const removePhoto = (index: number) => {
  const newList = [...props.modelValue]
  newList.splice(index, 1)
  emit('update:modelValue', newList)
  emit('change')
}

onBeforeUnmount(() => {
  uppy.destroy()
})
</script>

<style scoped>
.uppy-container {
  border-radius: 12px;
  overflow: hidden;
  border: 2px dashed var(--border-action-high-blue-france, #000091);
  background-color: var(--background-alt-grey, #f6f6f6);
  transition: all 0.2s ease-in-out;
}

.uppy-container:hover {
  border-color: var(--border-active-blue-france, #1212ff);
  background-color: var(--background-alt-blue-france, #f5f5fe);
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.08);
}

.uppy-container :deep(.uppy-Dashboard-inner) {
  background-color: transparent !important;
  border: none !important;
  width: 100% !important;
  font-family: inherit;
}

.uppy-container :deep(.uppy-Dashboard-dropFilesTitle) {
  font-size: 0.95rem !important;
  font-weight: 500 !important;
  color: var(--text-title-grey, #161616) !important;
}

.uppy-container :deep(.uppy-Dashboard-browse) {
  color: var(--text-action-high-blue-france, #000091) !important;
  font-weight: 600 !important;
  text-decoration: underline !important;
}

.uppy-container :deep(.uppy-Dashboard-note) {
  font-size: 0.8rem !important;
  color: var(--text-mention-grey, #666) !important;
}

.uppy-container :deep(.uppy-Dashboard-AddFiles-info) {
  margin-bottom: 0 !important;
}

.photo-preview-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.photo-preview-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid var(--border-default-grey, #e5e5e5);
  border-radius: 8px;
  padding: 0.5rem;
  background-color: var(--background-default-grey, #ffffff);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;
}

.photo-preview-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.photo-thumbnail {
  width: 110px;
  height: 110px;
  object-fit: cover;
  border-radius: 6px;
}

.delete-photo-btn {
  margin-top: 0.25rem;
  color: var(--text-default-error, #ce0500);
  min-height: 44px;
  min-width: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Optimisations spécifiques mobile */
@media (max-width: 576px) {
  .uppy-container {
    border-radius: 8px;
    border-width: 1.5px;
  }

  .uppy-container :deep(.uppy-Dashboard-AddFiles-title) {
    font-size: 0.875rem !important;
    line-height: 1.35 !important;
    padding: 0 0.5rem;
  }

  .uppy-container :deep(.uppy-Dashboard-browse) {
    display: inline-block;
    padding: 0.35rem 0.6rem;
    margin-top: 0.25rem;
    background-color: var(--background-action-low-blue-france, #e3e3fd);
    border-radius: 4px;
    text-decoration: none !important;
  }

  .photo-preview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.75rem;
  }

  .photo-preview-item {
    width: 100%;
    padding: 0.4rem;
  }

  .photo-thumbnail {
    width: 100%;
    height: 90px;
  }
}
</style>
