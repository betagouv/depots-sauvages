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
        v-if="sortedCategories.length === 0 && orphans.length === 0"
        class="fr-alert fr-alert--info fr-mb-4w"
      >
        <h3 class="fr-alert__title">Aucune question trouvée</h3>
        <p>Il n'y a pas encore de questions dans la FAQ.</p>
      </div>

      <div v-else>
        <div
          v-for="(cat, catIndex) in sortedCategories"
          :key="cat.id"
          class="faq-category-group fr-mb-6w"
        >
          <div
            v-if="getVisibleQuestions(cat).length > 0 || isAdminMode"
            class="fr-mb-3w category-header-wrapper"
          >
            <h2 class="fr-h4 fr-mb-0 category-header">
              {{ cat.label }}
            </h2>

            <AdminControls
              v-if="isAdminMode"
              class="category-admin-controls fr-ml-2w"
              :up-disabled="catIndex === 0"
              :down-disabled="catIndex === sortedCategories.length - 1"
              up-label="Monter cette thématique"
              down-label="Descendre cette thématique"
              edit-label="Modifier cette thématique"
              delete-label="Supprimer cette thématique"
              @up="moveCategory(catIndex, -1)"
              @down="moveCategory(catIndex, 1)"
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
              @up="moveItem(cat.id, index, -1)"
              @down="moveItem(cat.id, index, 1)"
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
              @up="moveItem(null, index, -1)"
              @down="moveItem(null, index, 1)"
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
        :categories="sortedCategories"
        :initial-data="form"
        @close="showForm = false"
        @save="saveItem"
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
import ConfirmModal from '@/components/shared/ConfirmModal.vue'
import RichTextEditor from '@/components/shared/RichTextEditor.vue'
import {
  API_URL,
  createResource,
  deleteResource,
  fetchResource,
  patchResource,
} from '@/services/api'
import { DsfrButton } from '@gouvminint/vue-dsfr'
import { computed, onMounted, reactive, ref } from 'vue'
import { useEditModeStore } from '../stores/editMode'
import FaqItem from '@/components/faq/FaqItem.vue'
import FaqQuestionModal from '@/components/faq/FaqQuestionModal.vue'
import FaqCategoryModal from '@/components/faq/FaqCategoryModal.vue'
import { AdminControls } from '../vue-antoinette'

interface FAQItem {
  id: number
  question: string
  content: Array<{ type: string; value: string }>
  order: number
  is_published: boolean
}

interface FAQCategory {
  id: number
  label: string
  order: number
  questions: FAQItem[]
}

const editModeStore = useEditModeStore()
const isAdminMode = computed(() => editModeStore.isAdminMode)

const categories = ref<FAQCategory[]>([])
const orphans = ref<FAQItem[]>([])

// Question Form State
const showForm = ref(false)
const editingId = ref<number | null>(null)
const form = reactive({
  question: '',
  answer: '',
  categoryId: null as number | null,
  order: 1,
  is_published: true,
})

// Category Form State
const showCategoryForm = ref(false)
const categoryForm = reactive({
  label: '',
  order: 0,
})

// Deletion State
const showDeleteConfirm = ref(false)
const showDeleteCategoryConfirm = ref(false)
const deletingItemId = ref<number | null>(null)
const deletingCategoryId = ref<number | null>(null)

const loadFaq = async () => {
  try {
    const items = await fetchResource(`${API_URL}/faq-items/?parent=null`)
    categories.value = (items || [])
      .filter((item: any) => !item.content || item.content.length === 0)
      .map((cat: any) => ({
        id: cat.id,
        label: cat.title,
        order: cat.order,
        questions: (cat.children || []).map((q: any) => ({
          id: q.id,
          question: q.title,
          content: q.content || [],
          order: q.order,
          is_published: q.is_published,
        })),
      }))
    orphans.value = (items || [])
      .filter((item: any) => item.content && item.content.length > 0)
      .map((q: any) => ({
        id: q.id,
        question: q.title,
        content: q.content || [],
        order: q.order,
        is_published: q.is_published,
      }))
  } catch (error) {
    console.error('Erreur lors du chargement de la FAQ :', error)
  }
}

const sortedCategories = computed(() => {
  return [...categories.value].sort((a, b) => a.order - b.order)
})

const getVisibleQuestions = (cat: FAQCategory) => {
  return cat.questions
    .filter((item) => isAdminMode.value || item.is_published)
    .sort((a, b) => a.order - b.order)
}

const visibleOrphans = computed(() => {
  return orphans.value
    .filter((item) => isAdminMode.value || item.is_published)
    .sort((a, b) => a.order - b.order)
})

// Category CRUD Actions
const openAddCategoryForm = () => {
  editingId.value = null
  categoryForm.label = ''
  categoryForm.order =
    categories.value.length > 0 ? Math.max(...categories.value.map((c) => c.order)) + 1 : 1
  showCategoryForm.value = true
}

const editCategory = (cat: FAQCategory) => {
  editingId.value = cat.id
  categoryForm.label = cat.label
  categoryForm.order = cat.order
  showCategoryForm.value = true
}

const saveCategory = async (data: { label: string }) => {
  try {
    if (editingId.value !== null) {
      const updated = await patchResource(`${API_URL}/faq-items/${editingId.value}/`, {
        title: data.label,
        order: categoryForm.order,
      })
      const idx = categories.value.findIndex((item) => item.id === editingId.value)
      if (idx !== -1 && updated) {
        categories.value[idx] = {
          ...categories.value[idx],
          label: updated.title,
          order: updated.order,
        }
      }
    } else {
      const created = await createResource(`${API_URL}/faq-items/`, {
        title: data.label,
        order: categoryForm.order,
        parent: null,
        content: [],
      })
      if (created) {
        categories.value.push({
          id: created.id,
          label: created.title,
          order: created.order,
          questions: [],
        })
      }
    }
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
      await deleteResource(`${API_URL}/faq-items/${deletingCategoryId.value}/`)
      const cat = categories.value.find((c) => c.id === deletingCategoryId.value)
      if (cat) {
        // Append children to orphans
        const updatedQuestions = cat.questions.map((q) => ({ ...q, categoryId: null }))
        orphans.value.push(...updatedQuestions)
      }
      categories.value = categories.value.filter((item) => item.id !== deletingCategoryId.value)
      showDeleteCategoryConfirm.value = false
      deletingCategoryId.value = null
    } catch (error) {
      console.error('Erreur lors de la suppression de la thématique :', error)
    }
  }
}

const moveCategory = async (currentIndex: number, direction: number) => {
  const cats = [...sortedCategories.value]
  const targetIndex = currentIndex + direction
  if (targetIndex < 0 || targetIndex >= cats.length) return

  const currentCat = cats[currentIndex]
  const targetCat = cats[targetIndex]

  const tempOrder = currentCat.order
  currentCat.order = targetCat.order
  targetCat.order = tempOrder

  const originalCurrent = categories.value.find((i) => i.id === currentCat.id)
  const originalTarget = categories.value.find((i) => i.id === targetCat.id)
  if (originalCurrent) originalCurrent.order = currentCat.order
  if (originalTarget) originalTarget.order = targetCat.order

  try {
    await Promise.all([
      patchResource(`${API_URL}/faq-items/${currentCat.id}/`, { order: currentCat.order }),
      patchResource(`${API_URL}/faq-items/${targetCat.id}/`, { order: targetCat.order }),
    ])
  } catch (error) {
    console.error('Erreur lors de la réorganisation des thématiques :', error)
  }
}

// Question CRUD Actions
const findQuestionById = (id: number): { item: FAQItem; categoryId: number | null } | null => {
  for (const cat of categories.value) {
    const found = cat.questions.find((q) => q.id === id)
    if (found) return { item: found, categoryId: cat.id }
  }
  const foundOrphan = orphans.value.find((o) => o.id === id)
  if (foundOrphan) return { item: foundOrphan, categoryId: null }
  return null
}

const removeQuestionFromAll = (id: number) => {
  categories.value.forEach((cat) => {
    cat.questions = cat.questions.filter((q) => q.id !== id)
  })
  orphans.value = orphans.value.filter((o) => o.id !== id)
}

const openAddForm = () => {
  editingId.value = null
  form.question = ''
  form.answer = ''
  form.categoryId = categories.value.length > 0 ? sortedCategories.value[0].id : null
  form.order = 1
  form.is_published = true
  showForm.value = true
}

const editItem = (item: FAQItem) => {
  editingId.value = item.id
  form.question = item.question
  const richTextBlock = (item.content || []).find((b: any) => b.type === 'rich_text')
  form.answer = richTextBlock ? richTextBlock.value : ''

  const questionInfo = findQuestionById(item.id)
  form.categoryId = questionInfo ? questionInfo.categoryId : null
  form.order = item.order
  form.is_published = item.is_published
  showForm.value = true
}

const saveItem = async (data: {
  question: string
  answer: string
  categoryId: number | null
  is_published: boolean
}) => {
  try {
    let finalId = editingId.value
    let finalOrder = form.order

    if (finalId !== null) {
      const originalInfo = findQuestionById(finalId)
      if (originalInfo) {
        if (originalInfo.categoryId !== data.categoryId) {
          if (data.categoryId === null) {
            finalOrder =
              orphans.value.length > 0 ? Math.max(...orphans.value.map((o) => o.order)) + 1 : 1
          } else {
            const targetCat = categories.value.find((c) => c.id === data.categoryId)
            finalOrder =
              targetCat && targetCat.questions.length > 0
                ? Math.max(...targetCat.questions.map((q) => q.order)) + 1
                : 1
          }
        } else {
          finalOrder = originalInfo.item.order
        }
      }

      const updated = await patchResource(`${API_URL}/faq-items/${finalId}/`, {
        title: data.question,
        content: [{ type: 'rich_text', value: data.answer }],
        parent: data.categoryId,
        order: finalOrder,
        is_published: data.is_published,
      })

      if (updated) {
        removeQuestionFromAll(finalId)
        const mappedItem: FAQItem = {
          id: updated.id,
          question: updated.title,
          content: updated.content || [],
          order: updated.order,
          is_published: updated.is_published,
        }

        if (data.categoryId === null) {
          orphans.value.push(mappedItem)
        } else {
          const targetCat = categories.value.find((c) => c.id === data.categoryId)
          if (targetCat) {
            targetCat.questions.push(mappedItem)
          }
        }
      }
    } else {
      if (data.categoryId === null) {
        finalOrder =
          orphans.value.length > 0 ? Math.max(...orphans.value.map((o) => o.order)) + 1 : 1
      } else {
        const targetCat = categories.value.find((c) => c.id === data.categoryId)
        finalOrder =
          targetCat && targetCat.questions.length > 0
            ? Math.max(...targetCat.questions.map((q) => q.order)) + 1
            : 1
      }

      const created = await createResource(`${API_URL}/faq-items/`, {
        title: data.question,
        content: [{ type: 'rich_text', value: data.answer }],
        parent: data.categoryId,
        order: finalOrder,
        is_published: data.is_published,
      })

      if (created) {
        const mappedItem: FAQItem = {
          id: created.id,
          question: created.title,
          content: created.content || [],
          order: created.order,
          is_published: created.is_published,
        }

        if (data.categoryId === null) {
          orphans.value.push(mappedItem)
        } else {
          const targetCat = categories.value.find((c) => c.id === data.categoryId)
          if (targetCat) {
            targetCat.questions.push(mappedItem)
          }
        }
      }
    }

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
      await deleteResource(`${API_URL}/faq-items/${deletingItemId.value}/`)
      removeQuestionFromAll(deletingItemId.value)
      showDeleteConfirm.value = false
      deletingItemId.value = null
    } catch (error) {
      console.error('Erreur lors de la suppression de la question :', error)
    }
  }
}

const moveItem = async (catId: number | null, currentIndex: number, direction: number) => {
  const list =
    catId !== null
      ? getVisibleQuestions(categories.value.find((c) => c.id === catId)!)
      : visibleOrphans.value
  const targetIndex = currentIndex + direction
  if (targetIndex < 0 || targetIndex >= list.length) return

  const currentItem = list[currentIndex]
  const targetItem = list[targetIndex]

  const tempOrder = currentItem.order
  currentItem.order = targetItem.order
  targetItem.order = tempOrder

  try {
    await Promise.all([
      patchResource(`${API_URL}/faq-items/${currentItem.id}/`, { order: currentItem.order }),
      patchResource(`${API_URL}/faq-items/${targetItem.id}/`, { order: targetItem.order }),
    ])
  } catch (error) {
    console.error('Erreur lors de la réorganisation des questions :', error)
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
