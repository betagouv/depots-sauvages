<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">3</span>
        Description du dépôt
      </h2>
    </legend>

    <div class="fr-fieldset__element">
      <BooleanRadioSet
        v-model="store.formData.photoDispo"
        legend="Disposez vous de photos du dépôt ?"
        hint="À la fin de cette démarche, vous pourrez récupérer le rapport de constatation. Vous pourrez les joindre ci-dessous."
        id-prefix="photo-dispo"
        :required="true"
      />
    </div>

    <div v-if="store.formData.photoDispo" class="fr-fieldset__element fr-mb-3w">
      <label class="fr-label" for="photo-upload-input">
        Ajouter des photos du dépôt
        <span class="fr-hint-text"
          >Formats acceptés : JPG, PNG. Vous pouvez sélectionner plusieurs photos.</span
        >
      </label>
      <input
        id="photo-upload-input"
        class="fr-upload"
        type="file"
        accept="image/*"
        multiple
        @change="handleFileUpload"
      />
      <div v-if="(store.formData.photos || []).length > 0" class="fr-mt-2w">
        <p class="fr-text--sm fr-mb-1w">
          <strong>{{ store.formData.photos.length }} photo(s) chargée(s) :</strong>
        </p>
        <div class="photo-preview-grid">
          <div
            v-for="(photo, index) in store.formData.photos"
            :key="index"
            class="photo-preview-item"
          >
            <img :src="photo" alt="Aperçu photo" class="photo-thumbnail" />
            <button
              type="button"
              class="fr-btn fr-btn--tertiary-no-outline fr-btn--sm fr-icon-delete-line"
              title="Supprimer la photo"
              @click="removePhoto(index)"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="fr-fieldset__element fr-mb-4w">
      <DsfrInputGroup
        v-model="store.formData.precisionsDepot"
        :is-textarea="true"
        :required="true"
        label="Description du dépôt"
        :error-message="store.errors.precisionsDepot"
      >
        <template #hint>
          <div class="fr-hint-text">
            Décrivez en quelques lignes le dépôt constaté.
            <br />
            Apportez également tout autre élément important :
            <ul class="fr-m-0 fr-pl-2w">
              <li>présence d'habitation, présence d'élevage, voie ferrée ;</li>
              <li>identité du propriétaire du terrain (si terrain privé) ;</li>
              <li>
                zone particulière (zone agricole, zone forestière, zone naturelle, zone humide, zone
                Natura 2000, zone Ramsar, etc.) ;
              </li>
              <li>
                risque d'écoulement (présence de liquide, proximité avec un cours d'eau ou captage
                d'eau) ;
              </li>
              <li>
                dernière date à laquelle le dépôt n'était pas présent (si vous en avez
                connaissance).
              </li>
            </ul>
          </div>
        </template>
      </DsfrInputGroup>
    </div>

    <div class="fr-fieldset__element">
      <DsfrRadioButtonSet
        v-model="store.formData.volumeDepot"
        legend="Volume estimé"
        :required="true"
        :options="VolumeOptions"
        :error-message="store.errors.volumeDepot"
        @update:model-value="store.clearFieldError('volumeDepot')"
      />
    </div>

    <div class="fr-fieldset__element">
      <DsfrCheckboxSet
        v-model="store.formData.typesDepot"
        legend="Type de dépôt"
        :required="true"
        :options="TypeDepotOptions"
        :error-message="store.errors.typesDepot"
        @update:model-value="store.clearFieldError('typesDepot')"
      />
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import BooleanRadioSet from '@/components/shared/BooleanRadioSet.vue'
import { useConstatationStore } from '@/stores/constatation'
import { TypeDepotOptions, VolumeOptions } from '@/types/constatation'
import { DsfrCheckboxSet, DsfrInputGroup, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'

const store = useConstatationStore()

const compressImage = (
  file: File,
  maxWidth = 1600,
  maxHeight = 1600,
  quality = 0.8
): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        let width = img.width
        let height = img.height

        if (width > maxWidth || height > maxHeight) {
          if (width / height > maxWidth / maxHeight) {
            height = Math.round((height * maxWidth) / width)
            width = maxWidth
          } else {
            width = Math.round((width * maxHeight) / height)
            height = maxHeight
          }
        }

        const canvas = document.createElement('canvas')
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        if (!ctx) {
          resolve(e.target?.result as string)
          return
        }

        ctx.drawImage(img, 0, 0, width, height)
        const compressedDataUrl = canvas.toDataURL('image/jpeg', quality)
        resolve(compressedDataUrl)
      }
      img.onerror = () => reject(new Error("Erreur de chargement de l'image"))
      img.src = e.target?.result as string
    }
    reader.onerror = (err) => reject(err)
    reader.readAsDataURL(file)
  })
}

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files) return

  if (!Array.isArray(store.formData.photos)) {
    store.formData.photos = []
  }

  const files = Array.from(target.files)
  for (const file of files) {
    try {
      const compressedBase64 = await compressImage(file)
      store.formData.photos.push(compressedBase64)
    } catch (err) {
      console.error('Erreur lors de la compression de la photo:', err)
    }
  }
  store.autoSave()
  target.value = ''
}

const removePhoto = (index: number) => {
  if (Array.isArray(store.formData.photos)) {
    store.formData.photos.splice(index, 1)
    store.autoSave()
  }
}
</script>

<style scoped>
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
  border: 1px solid var(--border-default-grey);
  border-radius: 4px;
  padding: 0.5rem;
  background-color: var(--background-alt-grey);
}

.photo-thumbnail {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}
</style>
