<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-2w">Foire Aux Questions (FAQ)</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Retrouvez toutes les réponses aux questions les plus fréquentes sur la lutte contre les
          dépôts sauvages.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div
        v-if="categories.length === 0 && orphans.length === 0"
        class="fr-alert fr-alert--info fr-mb-4w"
      >
        <h3 class="fr-alert__title">Aucune question trouvée</h3>
        <p>Il n'y a pas encore de questions dans la FAQ.</p>
      </div>

      <div v-else>
        <div
          v-for="(cat, catIndex) in categories"
          :key="cat.id"
          class="faq-category-group fr-mb-6w"
        >
          <div
            v-if="getVisibleQuestions(cat).length > 0 || isAdminMode"
            class="fr-mb-3w category-header-wrapper"
          >
            <h2 class="fr-h4 fr-mb-0 category-header">
              {{ cat.title }}
            </h2>

            <AdminControls
              v-if="isAdminMode"
              class="category-admin-controls fr-ml-2w"
              :up-disabled="catIndex === 0"
              :down-disabled="catIndex === categories.length - 1"
              up-label="Monter cette thématique"
              down-label="Descendre cette thématique"
              edit-label="Modifier cette thématique"
              delete-label="Supprimer cette thématique"
              @up="moveUp(cat.id)"
              @down="moveDown(cat.id)"
              @edit="editCategory(cat)"
              @delete="triggerDeleteCategory(cat.id)"
            />
          </div>

          <div v-if="getVisibleQuestions(cat).length > 0" class="fr-accordions-group">
            <FaqItem
              v-for="(item, index) in getVisibleQuestions(cat)"
              :key="item.id"
              :item="item"
              :index="index"
              :list-length="getVisibleQuestions(cat).length"
              :is-admin-mode="isAdminMode"
              @up="moveUp(item.id)"
              @down="moveDown(item.id)"
              @edit="editItem(item)"
              @delete="triggerDeleteItem(item.id)"
            />
          </div>
        </div>

        <div v-if="visibleOrphans.length > 0" class="faq-category-group fr-mb-6w">
          <div class="fr-mb-3w category-header-wrapper">
            <h2 class="fr-h4 fr-mb-0 category-header">Questions sans thématique</h2>
          </div>

          <div class="fr-accordions-group">
            <FaqItem
              v-for="(item, index) in visibleOrphans"
              :key="item.id"
              :item="item"
              :index="index"
              :list-length="visibleOrphans.length"
              :is-admin-mode="isAdminMode"
              @up="moveUp(item.id)"
              @down="moveDown(item.id)"
              @edit="editItem(item)"
              @delete="triggerDeleteItem(item.id)"
            />
          </div>
        </div>
      </div>

      <div
        v-if="isAdminMode"
        class="fr-mt-6w text-center fr-grid-row fr-grid-row--center fr-grid-row--gutters"
      >
        <div class="fr-col-auto">
          <DsfrButton secondary @click="openAddCategoryForm">
            <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
            Ajouter une thématique
          </DsfrButton>
        </div>
        <div class="fr-col-auto">
          <DsfrButton @click="openAddForm">
            <span class="fr-icon-add-line fr-mr-1w" aria-hidden="true"></span>
            Ajouter une question
          </DsfrButton>
        </div>
      </div>

      <FaqQuestionModal
        :opened="showForm"
        :title="editingId ? 'Modifier la question de la FAQ' : 'Ajouter une nouvelle question'"
        :categories="categories.map((c: any) => ({ id: c.id, label: c.title }))"
        :initial-data="form"
        @close="showForm = false"
        @save="saveQuestion"
      />

      <FaqCategoryModal
        :opened="showCategoryForm"
        :title="editingId ? 'Modifier la thématique' : 'Ajouter une thématique'"
        :initial-data="categoryForm"
        @close="showCategoryForm = false"
        @save="saveCategory"
      />

      <ConfirmModal
        :opened="showDeleteConfirm"
        title="Supprimer la question ?"
        message="Êtes-vous sûr de vouloir supprimer cette question ? Cette action est irréversible."
        confirm-button-label="Oui, supprimer"
        cancel-button-label="Annuler"
        :is-danger="true"
        @close="showDeleteConfirm = false"
        @confirm="confirmDeleteItem"
      />

      <ConfirmModal
        :opened="showDeleteCategoryConfirm"
        title="Supprimer la thématique ?"
        message="Êtes-vous sûr de vouloir supprimer cette thématique ? Les questions associées ne seront pas supprimées mais seront déplacées dans la section « Questions sans thématique » en bas de page."
        confirm-button-label="Oui, supprimer"
        cancel-button-label="Annuler"
        :is-danger="true"
        @close="showDeleteCategoryConfirm = false"
        @confirm="confirmDeleteCategory"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import FaqCategoryModal from '@/components/faq/FaqCategoryModal.vue'
import FaqItem from '@/components/faq/FaqItem.vue'
import FaqQuestionModal from '@/components/faq/FaqQuestionModal.vue'
import ConfirmModal from '@/components/shared/ConfirmModal.vue'
import * as api from '@/services/api'
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, reactive, ref } from 'vue'
import { useEditModeStore } from '../stores/editMode'
import { AdminControls, useNestedContent } from '../vue-antoinette'

const editModeStore = useEditModeStore()
const isAdminMode = computed(() => editModeStore.isAdminMode)

const {
  categories,
  orphans,
  load: loadFaq,
  moveUp,
  moveDown,
  deleteItem,
  saveItem,
} = useNestedContent(`${api.API_URL}/faq-items`, api)

const showForm = ref(false)
const editingId = ref<number | null>(null)
const form = reactive({
  question: '',
  answer: '',
  categoryId: null as number | null,
  is_published: true,
})

const showCategoryForm = ref(false)
const categoryForm = reactive({
  label: '',
})

const showDeleteConfirm = ref(false)
const showDeleteCategoryConfirm = ref(false)
const deletingItemId = ref<number | null>(null)
const deletingCategoryId = ref<number | null>(null)

const getVisibleQuestions = (cat: any) => {
  const children = cat.children || []
  return children
    .filter((item: any) => isAdminMode.value || item.is_published)
    .map((item: any) => ({
      ...item,
      question: item.title, // Align with FaqItem expectations
    }))
}

const visibleOrphans = computed(() => {
  return orphans.value
    .filter((item) => isAdminMode.value || item.is_published)
    .map((item: any) => ({
      ...item,
      question: item.title, // Align with FaqItem expectations
    }))
})

const openAddCategoryForm = () => {
  editingId.value = null
  categoryForm.label = ''
  showCategoryForm.value = true
}

const editCategory = (cat: any) => {
  editingId.value = cat.id
  categoryForm.label = cat.title
  showCategoryForm.value = true
}

const saveCategory = async (data: { label: string }) => {
  try {
    await saveItem(editingId.value, {
      title: data.label,
      parent: null,
      content: [],
    })
    showCategoryForm.value = false
    editingId.value = null
  } catch (error) {
    console.error("Erreur lors de l'enregistrement de la thématique :", error)
  }
}

const triggerDeleteCategory = (id: number) => {
  deletingCategoryId.value = id
  showDeleteCategoryConfirm.value = true
}

const confirmDeleteCategory = async () => {
  if (deletingCategoryId.value !== null) {
    try {
      await deleteItem(deletingCategoryId.value)
      showDeleteCategoryConfirm.value = false
      deletingCategoryId.value = null
    } catch (error) {
      console.error('Erreur lors de la suppression de la thématique :', error)
    }
  }
}

const openAddForm = () => {
  editingId.value = null
  form.question = ''
  form.answer = ''
  form.categoryId = categories.value.length > 0 ? categories.value[0].id : null
  form.is_published = true
  showForm.value = true
}

const editItem = (item: any) => {
  editingId.value = item.id
  form.question = item.title
  const richTextBlock = (item.content || []).find((b: any) => b.type === 'rich_text')
  form.answer = richTextBlock ? richTextBlock.value : ''
  form.categoryId = item.parent
  form.is_published = item.is_published
  showForm.value = true
}

const saveQuestion = async (data: {
  question: string
  answer: string
  categoryId: number | null
  is_published: boolean
}) => {
  try {
    await saveItem(editingId.value, {
      title: data.question,
      content: [{ type: 'rich_text', value: data.answer }],
      parent: data.categoryId,
      is_published: data.is_published,
    })
    showForm.value = false
    editingId.value = null
  } catch (error) {
    console.error("Erreur lors de l'enregistrement de la question :", error)
  }
}

const triggerDeleteItem = (id: number) => {
  deletingItemId.value = id
  showDeleteConfirm.value = true
}

const confirmDeleteItem = async () => {
  if (deletingItemId.value !== null) {
    try {
      await deleteItem(deletingItemId.value)
      showDeleteConfirm.value = false
      deletingItemId.value = null
    } catch (error) {
      console.error('Erreur lors de la suppression de la question :', error)
    }
  }
}

onMounted(() => {
  loadFaq()
})
</script>

<style scoped>
.category-header-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid var(--border-default-blue-france);
  padding-bottom: 0.5rem;
}
.category-header {
  border-bottom: none !important;
  padding-bottom: 0 !important;
  color: var(--text-title-blue-france);
  display: flex;
  align-items: center;
}
.category-icon {
  font-size: 1.25rem;
}

.text-right {
  text-align: right;
}
</style>
