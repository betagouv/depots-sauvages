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
            v-if="getFilteredQuestions(cat).length > 0 || isAdminMode"
            class="fr-mb-3w category-header-wrapper"
          >
            <h2 class="fr-h4 fr-mb-0 category-header">
              {{ cat.label }}
            </h2>

            <div v-if="isAdminMode" class="admin-inline-controls category-admin-controls fr-ml-2w">
              <button
                class="admin-btn fr-icon-arrow-up-line"
                aria-label="Monter cette thématique"
                title="Monter"
                :disabled="catIndex === 0"
                @click.stop="moveCategory(catIndex, -1)"
              ></button>
              <button
                class="admin-btn fr-icon-arrow-down-line"
                aria-label="Descendre cette thématique"
                title="Descendre"
                :disabled="catIndex === sortedCategories.length - 1"
                @click.stop="moveCategory(catIndex, 1)"
              ></button>
              <button
                class="admin-btn fr-icon-edit-line"
                aria-label="Modifier cette thématique"
                title="Modifier"
                @click.stop="editCategory(cat)"
              ></button>
              <button
                class="admin-btn admin-btn-delete fr-icon-delete-line"
                aria-label="Supprimer cette thématique"
                title="Supprimer"
                @click.stop="triggerDeleteCategory(cat.id)"
              ></button>
            </div>
          </div>

          <div v-if="getFilteredQuestions(cat).length > 0" class="fr-accordions-group">
            <section
              v-for="(item, index) in getFilteredQuestions(cat)"
              :key="item.id"
              class="fr-accordion faq-item-section"
              :class="{ 'faq-draft': !item.is_published }"
            >
              <div
                class="fr-grid-row fr-grid-row--middle faq-item-header"
                :class="{ 'faq-item-header--expanded': expandedItems[item.id] }"
              >
                <div class="fr-col">
                  <h3 class="fr-accordion__title">
                    <button
                      class="fr-accordion__btn"
                      :aria-expanded="expandedItems[item.id]"
                      :aria-controls="'accordion-' + item.id"
                      @click="toggleAccordion(item.id)"
                    >
                      {{ item.question }}
                      <span v-if="!item.is_published" class="fr-badge fr-badge--warning fr-ml-2w"
                        >Brouillon</span
                      >
                    </button>
                  </h3>
                </div>

                <div v-if="isAdminMode" class="fr-col-auto fr-pr-2w admin-inline-controls">
                  <button
                    class="admin-btn fr-icon-arrow-up-line"
                    aria-label="Monter cette question"
                    title="Monter"
                    :disabled="index === 0"
                    @click.stop="moveItem(cat.id, index, -1)"
                  ></button>
                  <button
                    class="admin-btn fr-icon-arrow-down-line"
                    aria-label="Descendre cette question"
                    title="Descendre"
                    :disabled="index === getFilteredQuestions(cat).length - 1"
                    @click.stop="moveItem(cat.id, index, 1)"
                  ></button>
                  <button
                    class="admin-btn fr-icon-edit-line"
                    aria-label="Modifier cette question"
                    title="Modifier"
                    @click.stop="editItem(item)"
                  ></button>
                  <button
                    class="admin-btn admin-btn-delete fr-icon-delete-line"
                    aria-label="Supprimer cette question"
                    title="Supprimer"
                    @click.stop="triggerDeleteItem(item.id)"
                  ></button>
                </div>
              </div>

              <div
                class="fr-collapse"
                :id="'accordion-' + item.id"
                :class="{ 'fr-collapse--expanded': expandedItems[item.id] }"
                :style="expandedItems[item.id] ? 'max-height: none;' : undefined"
              >
                <div class="fr-p-3w">
                  <BlockRenderer :blocks="item.content" />
                </div>
              </div>
            </section>
          </div>
        </div>

        <div v-if="getFilteredOrphans.length > 0" class="faq-category-group fr-mb-6w">
          <div class="fr-mb-3w category-header-wrapper">
            <h2 class="fr-h4 fr-mb-0 category-header">Questions sans thématique</h2>
          </div>

          <div class="fr-accordions-group">
            <section
              v-for="(item, index) in getFilteredOrphans"
              :key="item.id"
              class="fr-accordion faq-item-section"
              :class="{ 'faq-draft': !item.is_published }"
            >
              <div
                class="fr-grid-row fr-grid-row--middle faq-item-header"
                :class="{ 'faq-item-header--expanded': expandedItems[item.id] }"
              >
                <div class="fr-col">
                  <h3 class="fr-accordion__title">
                    <button
                      class="fr-accordion__btn"
                      :aria-expanded="expandedItems[item.id]"
                      :aria-controls="'accordion-' + item.id"
                      @click="toggleAccordion(item.id)"
                    >
                      {{ item.question }}
                      <span v-if="!item.is_published" class="fr-badge fr-badge--warning fr-ml-2w"
                        >Brouillon</span
                      >
                    </button>
                  </h3>
                </div>

                <div v-if="isAdminMode" class="fr-col-auto fr-pr-2w admin-inline-controls">
                  <button
                    class="admin-btn fr-icon-arrow-up-line"
                    aria-label="Monter cette question"
                    title="Monter"
                    :disabled="index === 0"
                    @click.stop="moveItem(null, index, -1)"
                  ></button>
                  <button
                    class="admin-btn fr-icon-arrow-down-line"
                    aria-label="Descendre cette question"
                    title="Descendre"
                    :disabled="index === getFilteredOrphans.length - 1"
                    @click.stop="moveItem(null, index, 1)"
                  ></button>
                  <button
                    class="admin-btn fr-icon-edit-line"
                    aria-label="Modifier cette question"
                    title="Modifier"
                    @click.stop="editItem(item)"
                  ></button>
                  <button
                    class="admin-btn admin-btn-delete fr-icon-delete-line"
                    aria-label="Supprimer cette question"
                    title="Supprimer"
                    @click.stop="triggerDeleteItem(item.id)"
                  ></button>
                </div>
              </div>

              <div
                class="fr-collapse"
                :id="'accordion-' + item.id"
                :class="{ 'fr-collapse--expanded': expandedItems[item.id] }"
                :style="expandedItems[item.id] ? 'max-height: none;' : undefined"
              >
                <div class="fr-p-3w">
                  <BlockRenderer :blocks="item.content" />
                </div>
              </div>
            </section>
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

      <DsfrModal
        :opened="showForm"
        :title="editingId ? 'Modifier la question de la FAQ' : 'Ajouter une nouvelle question'"
        :is-alert="true"
        @close="showForm = false"
      >
        <form @submit.prevent="saveItem" class="fr-container--fluid fr-p-0 faq-edit-form">
          <div class="fr-grid-row fr-grid-row--gutters">
            <div class="fr-col-12">
              <div class="fr-input-group">
                <label class="fr-label" for="faq-question">Question</label>
                <input
                  v-model="form.question"
                  class="fr-input"
                  type="text"
                  id="faq-question"
                  required
                  placeholder="Ex: Qu'est-ce qu'un dépôt sauvage ?"
                />
              </div>
            </div>

            <div class="fr-col-12">
              <div class="fr-select-group">
                <label class="fr-label" for="faq-category">Thématique / Catégorie</label>
                <select v-model="form.categoryId" class="fr-select" id="faq-category">
                  <option :value="null">Aucune thématique (placer en bas)</option>
                  <option v-for="cat in sortedCategories" :key="cat.id" :value="cat.id">
                    {{ cat.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="fr-col-12">
              <div class="fr-input-group">
                <label class="fr-label" for="faq-answer">Réponse</label>

                <div class="tiptap-editor-wrapper">
                  <RichTextEditor v-model="form.answer" />
                </div>
              </div>
            </div>

            <div class="fr-col-12">
              <div class="fr-checkbox-group">
                <input v-model="form.is_published" type="checkbox" id="faq-published" />
                <label class="fr-label" for="faq-published">Publié (visible de tous)</label>
              </div>
            </div>

            <div class="fr-col-12 fr-mt-3w text-right">
              <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--right">
                <li>
                  <button type="button" class="fr-btn fr-btn--secondary" @click="showForm = false">
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

      <DsfrModal
        :opened="showCategoryForm"
        :title="editingId ? 'Modifier la thématique' : 'Ajouter une thématique'"
        :is-alert="true"
        @close="showCategoryForm = false"
      >
        <form @submit.prevent="saveCategory" class="fr-container--fluid fr-p-0">
          <div class="fr-grid-row fr-grid-row--gutters">
            <div class="fr-col-12">
              <div class="fr-input-group">
                <label class="fr-label" for="category-label">Titre de la thématique</label>
                <input
                  v-model="categoryForm.label"
                  class="fr-input"
                  type="text"
                  id="category-label"
                  required
                  placeholder="Ex: ⚖️ Cadre général"
                />
              </div>
            </div>

            <div class="fr-col-12 fr-mt-3w text-right">
              <ul class="fr-btns-group fr-btns-group--inline fr-btns-group--right">
                <li>
                  <button
                    type="button"
                    class="fr-btn fr-btn--secondary"
                    @click="showCategoryForm = false"
                  >
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
import { DsfrButton, DsfrModal } from '@gouvminint/vue-dsfr'
import { computed, onMounted, reactive, ref } from 'vue'
import { useEditModeStore } from '../stores/editMode'
import { BlockRenderer } from '../vue-antoinette'

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
const expandedItems = reactive<Record<number, boolean>>({})

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

const getFilteredQuestions = (cat: FAQCategory) => {
  return cat.questions
    .filter((item) => isAdminMode.value || item.is_published)
    .sort((a, b) => a.order - b.order)
}

const getFilteredOrphans = computed(() => {
  return orphans.value
    .filter((item) => isAdminMode.value || item.is_published)
    .sort((a, b) => a.order - b.order)
})

const toggleAccordion = (id: number) => {
  expandedItems[id] = !expandedItems[id]
}

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

const saveCategory = async () => {
  try {
    if (editingId.value !== null) {
      const updated = await patchResource(`${API_URL}/faq-items/${editingId.value}/`, {
        title: categoryForm.label,
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
        title: categoryForm.label,
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

const saveItem = async () => {
  try {
    let finalId = editingId.value
    let finalOrder = form.order

    if (finalId !== null) {
      const originalInfo = findQuestionById(finalId)
      if (originalInfo) {
        if (originalInfo.categoryId !== form.categoryId) {
          if (form.categoryId === null) {
            finalOrder =
              orphans.value.length > 0 ? Math.max(...orphans.value.map((o) => o.order)) + 1 : 1
          } else {
            const targetCat = categories.value.find((c) => c.id === form.categoryId)
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
        title: form.question,
        content: [{ type: 'rich_text', value: form.answer }],
        parent: form.categoryId,
        order: finalOrder,
        is_published: form.is_published,
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

        if (form.categoryId === null) {
          orphans.value.push(mappedItem)
        } else {
          const targetCat = categories.value.find((c) => c.id === form.categoryId)
          if (targetCat) {
            targetCat.questions.push(mappedItem)
          }
        }
      }
    } else {
      if (form.categoryId === null) {
        finalOrder =
          orphans.value.length > 0 ? Math.max(...orphans.value.map((o) => o.order)) + 1 : 1
      } else {
        const targetCat = categories.value.find((c) => c.id === form.categoryId)
        finalOrder =
          targetCat && targetCat.questions.length > 0
            ? Math.max(...targetCat.questions.map((q) => q.order)) + 1
            : 1
      }

      const created = await createResource(`${API_URL}/faq-items/`, {
        title: form.question,
        content: [{ type: 'rich_text', value: form.answer }],
        parent: form.categoryId,
        order: finalOrder,
        is_published: form.is_published,
      })

      if (created) {
        const mappedItem: FAQItem = {
          id: created.id,
          question: created.title,
          content: created.content || [],
          order: created.order,
          is_published: created.is_published,
        }

        if (form.categoryId === null) {
          orphans.value.push(mappedItem)
        } else {
          const targetCat = categories.value.find((c) => c.id === form.categoryId)
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
      ? getFilteredQuestions(categories.value.find((c) => c.id === catId)!)
      : getFilteredOrphans.value
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
.faq-draft {
  opacity: 0.75;
  border-left: 4px solid #ffca00;
}
.faq-item-section {
  position: relative;
  margin-bottom: 1.5rem !important;
  border: 1px solid var(--border-default-grey) !important;
  border-radius: 8px !important;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 145, 0.02);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}
.faq-item-section:hover {
  border-color: var(--border-default-blue-france) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.05);
}
.faq-item-header {
  transition: background-color 0.2s ease;
}
.faq-item-header--expanded {
  background-color: var(--background-alt-blue-france);
}
.faq-item-header :deep(.fr-accordion__title) {
  margin: 0;
}
.faq-item-header :deep(.fr-accordion__btn) {
  padding: 1.25rem 1.5rem;
  background-color: transparent !important;
}
.faq-item-section :deep(.fr-accordion::before) {
  display: none !important;
}
.admin-inline-controls {
  z-index: 10;
  display: flex;
  gap: 0.35rem;
  align-items: center;
}
.admin-btn {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50% !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-default-grey) !important;
  border: 1px solid var(--border-default-grey) !important;
  color: var(--text-action-high-blue-france) !important;
  padding: 0 !important;
  min-height: auto !important;
  transition: all 0.15s ease-in-out;
}
.admin-btn::before {
  margin: 0 !important;
}
.admin-btn:hover:not(:disabled) {
  background-color: var(--background-alt-blue-france) !important;
  border-color: var(--border-default-blue-france) !important;
  color: var(--text-active-blue-france) !important;
}
.admin-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  background-color: var(--background-alt-grey) !important;
  border-color: var(--border-default-grey) !important;
  color: var(--text-disabled-grey) !important;
}
.admin-btn-delete {
  color: var(--text-default-error) !important;
}
.admin-btn-delete:hover:not(:disabled) {
  background-color: #fee9e9 !important;
  border-color: var(--border-plain-error) !important;
  color: var(--text-default-error) !important;
}

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
