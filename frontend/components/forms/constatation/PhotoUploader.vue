<template>
  <div class="photo-uploader">
    <label v-if="label" class="fr-label">
      {{ label }}
      <span v-if="hint" class="fr-hint-text">{{ hint }}</span>
    </label>

    <div
      class="dropzone-container fr-mt-2w"
      :class="{ 'is-dragging': isDragging, 'is-processing': isProcessing }"
      @dragover.prevent="onDragOver"
      @dragenter.prevent="onDragEnter"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="triggerFileInput"
    >
      <input
        ref="fileInputRef"
        type="file"
        multiple
        accept="image/jpeg,image/png,image/webp,image/heic,image/heif"
        class="file-input-hidden"
        :disabled="isProcessing"
        @change="onFileSelect"
      />

      <div class="dropzone-content">
        <template v-if="isProcessing">
          <span class="fr-icon-refresh-line dropzone-icon spinner" aria-hidden="true"></span>
          <p class="dropzone-title fr-mb-1v">
            <strong>Optimisation de la photo en cours...</strong>
          </p>
        </template>
        <template v-else>
          <span class="fr-icon-add-circle-line dropzone-icon" aria-hidden="true"></span>
          <p class="dropzone-title fr-mb-1v">
            <span class="hide-mobile"> <strong>Glissez-déposez vos photos ici</strong> ou </span>
            <span class="browse-link">parcourez vos fichiers</span>
          </p>
          <p class="dropzone-note fr-text--xs fr-mb-0">
            {{ note }}
          </p>
        </template>
      </div>
    </div>

    <div v-if="modelValue.length > 0" class="fr-mt-3w">
      <p class="fr-text--sm fr-mb-2w">
        <strong>{{ modelValue.length }} photo(s) ajoutée(s) :</strong>
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
import Compressor from 'compressorjs'
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue?: string[]
    maxFileSizeMb?: number
    label?: string
    hint?: string
    note?: string
  }>(),
  {
    modelValue: () => [],
    maxFileSizeMb: 20,
    label: '',
    hint: '',
    note: 'Formats acceptés : JPG, PNG, WEBP (Max 20 Mo par photo)',
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
  (e: 'change'): void
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isProcessing = ref(false)

const triggerFileInput = () => {
  if (!isProcessing.value) {
    fileInputRef.value?.click()
  }
}

const onDragEnter = () => {
  isDragging.value = true
}

const onDragOver = () => {
  isDragging.value = true
}

const onDragLeave = (e: DragEvent) => {
  if (!(e.currentTarget as HTMLElement).contains(e.relatedTarget as Node)) {
    isDragging.value = false
  }
}

const onDrop = (e: DragEvent) => {
  isDragging.value = false
  if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
    processFiles(Array.from(e.dataTransfer.files))
  }
}

const onFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    processFiles(Array.from(target.files))
    target.value = ''
  }
}

/**
 * Fallback image compression using native Canvas if Compressor.js fails.
 */
const compressWithCanvasFallback = (file: File): Promise<Blob | File> => {
  return new Promise((resolve) => {
    const img = new Image()
    const url = URL.createObjectURL(file)

    const cleanup = () => URL.revokeObjectURL(url)

    img.onload = () => {
      const MAX_SIZE = 1600
      let { width, height } = img

      if (width > MAX_SIZE || height > MAX_SIZE) {
        if (width > height) {
          height = Math.round((height * MAX_SIZE) / width)
          width = MAX_SIZE
        } else {
          width = Math.round((width * MAX_SIZE) / height)
          height = MAX_SIZE
        }
      }

      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        cleanup()
        resolve(file)
        return
      }

      ctx.drawImage(img, 0, 0, width, height)
      canvas.toBlob(
        (blob) => {
          cleanup()
          resolve(blob && blob.size < file.size ? blob : file)
        },
        'image/jpeg',
        0.8
      )
    }

    img.onerror = () => {
      cleanup()
      resolve(file)
    }

    img.src = url
  })
}

/**
 * Compress image using Compressor.js or native Canvas fallback.
 */
const compressImage = (file: File): Promise<Blob | File> => {
  return new Promise((resolve) => {
    if (!file.type.startsWith('image/')) {
      resolve(file)
      return
    }

    new Compressor(file, {
      quality: 0.8,
      maxWidth: 1600,
      maxHeight: 1600,
      success(result) {
        resolve(result)
      },
      async error(err) {
        console.warn('Erreur Compressor.js, fallback Canvas natif:', err)
        const fallbackResult = await compressWithCanvasFallback(file)
        resolve(fallbackResult)
      },
    })
  })
}

const fileToBase64 = (file: Blob | File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = (err) => reject(err)
    reader.readAsDataURL(file)
  })
}

const processFiles = async (files: File[]) => {
  const maxSizeBytes = props.maxFileSizeMb * 1024 * 1024
  const validFiles = files.filter((file) => {
    if (file.size > maxSizeBytes) {
      alert(
        `Le fichier "${file.name}" dépasse la taille maximale autorisée de ${props.maxFileSizeMb} Mo.`
      )
      return false
    }
    return true
  })

  if (validFiles.length === 0) return

  isProcessing.value = true
  try {
    const newBase64List: string[] = []
    for (const file of validFiles) {
      const compressed = await compressImage(file)
      const base64 = await fileToBase64(compressed)
      newBase64List.push(base64)
    }

    const updatedList = [...props.modelValue, ...newBase64List]
    emit('update:modelValue', updatedList)
    emit('change')
  } catch (err) {
    console.error('Erreur lors du traitement des images:', err)
  } finally {
    isProcessing.value = false
  }
}

const removePhoto = (index: number) => {
  const newList = [...props.modelValue]
  newList.splice(index, 1)
  emit('update:modelValue', newList)
  emit('change')
}
</script>

<style scoped>
.file-input-hidden {
  display: none;
}

.dropzone-container {
  border: 2px dashed var(--border-action-high-blue-france, #000091);
  border-radius: 12px;
  background-color: var(--background-alt-grey, #f6f6f6);
  padding: 2rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.dropzone-container:hover,
.dropzone-container.is-dragging {
  border-color: var(--border-active-blue-france, #1212ff);
  background-color: var(--background-alt-blue-france, #f5f5fe);
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.08);
}

.dropzone-container.is-processing {
  cursor: wait;
  opacity: 0.8;
}

.dropzone-icon {
  font-size: 2rem;
  color: var(--text-action-high-blue-france, #000091);
  margin-bottom: 0.5rem;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.dropzone-title {
  color: var(--text-title-grey, #161616);
  font-size: 0.95rem;
}

.browse-link {
  color: var(--text-action-high-blue-france, #000091);
  text-decoration: underline;
  font-weight: 600;
}

.dropzone-note {
  color: var(--text-mention-grey, #666666);
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

/* Optimisations mobiles */
@media (max-width: 576px) {
  .hide-mobile {
    display: none;
  }

  .dropzone-container {
    padding: 1.5rem 1rem;
    border-radius: 8px;
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
