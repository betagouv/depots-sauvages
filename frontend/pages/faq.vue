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
      <!-- FAQ Accordions -->
      <div v-if="sortedCategories.length === 0 && orphans.length === 0" class="fr-alert fr-alert--info fr-mb-4w">
        <h3 class="fr-alert__title">Aucune question trouvée</h3>
        <p>Il n'y a pas encore de questions dans la FAQ.</p>
      </div>

      <div v-else>
        <!-- Loop categories -->
        <div v-for="(cat, catIndex) in sortedCategories" :key="cat.id" class="faq-category-group fr-mb-6w">
          <div v-if="getFilteredQuestions(cat).length > 0 || isAdminMode" class="fr-mb-3w category-header-wrapper">
            <h2 class="fr-h4 fr-mb-0 category-header">
              {{ cat.label }}
            </h2>

            <!-- Admin Category Controls -->
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

          <!-- Questions of this category -->
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

                <!-- Admin inline controls for questions -->
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
                <div class="fr-p-3w content-styled" v-html="renderContent(item.answer)"></div>
              </div>
            </section>
          </div>
        </div>

        <!-- Section for Questions without Parent (Orphans) -->
        <div v-if="getFilteredOrphans.length > 0" class="faq-category-group fr-mb-6w">
          <div class="fr-mb-3w category-header-wrapper">
            <h2 class="fr-h4 fr-mb-0 category-header">
              Questions sans thématique
            </h2>
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

                <!-- Admin inline controls for orphan questions -->
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
                <div class="fr-p-3w content-styled" v-html="renderContent(item.answer)"></div>
              </div>
            </section>
          </div>
        </div>
      </div>

      <!-- Admin Add Action Buttons -->
      <div v-if="isAdminMode" class="fr-mt-6w text-center fr-grid-row fr-grid-row--center fr-grid-row--gutters">
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

      <!-- Add / Edit Question Modal -->
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
                <select
                  v-model="form.categoryId"
                  class="fr-select"
                  id="faq-category"
                >
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

                <!-- TipTap Editor -->
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

      <!-- Add / Edit Category Modal -->
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
                  <button type="button" class="fr-btn fr-btn--secondary" @click="showCategoryForm = false">
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

      <!-- Reusable Confirmation Warning Modal for Question Deletion -->
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

      <!-- Reusable Confirmation Warning Modal for Category Deletion -->
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
import { DsfrButton, DsfrModal } from '@gouvminint/vue-dsfr'
import { computed, onMounted, reactive, ref } from 'vue'
import { useEditModeStore } from '../stores/editMode'

interface FAQItem {
  id: number
  question: string
  answer: string
  order: number
  is_published: boolean
}

interface FAQCategory {
  id: number
  label: string
  order: number
  questions: FAQItem[]
}

// Initial seed categories with embedded questions
const DEFAULT_CATEGORIES: FAQCategory[] = [
  {
    id: 1,
    label: '⚖️ Cadre général',
    order: 1,
    questions: [
      {
        id: 1,
        question: "Qu'est-ce qu'un dépôt sauvage ?",
        answer:
          'Un dépôt sauvage est un abandon illégal de déchets (gravats, ordures ménagères, encombrants, etc.) sur le domaine public ou privé, en dehors des emplacements autorisés (déchetteries, conteneurs dédiés).',
        order: 1,
        is_published: true,
      },
      {
        id: 2,
        question: 'Quelles sont les sanctions pour un dépôt sauvage ?',
        answer:
          "Les amende peuvent aller de 135 € (amende forfaitaire) à 1 500 € (voire 75 000 € et 2 ans d'emprisonnement pour les entreprises ou en cas d'utilisation d'un véhicule). Le maire dispose également de pouvoirs de police pour ordonner le nettoyage sous astreinte administrative.",
        order: 2,
        is_published: true,
      },
    ],
  },
  { id: 2, label: '🧾 Déroulement de la procédure', order: 2, questions: [] },
  { id: 3, label: '🔍 Identification des auteurs', order: 3, questions: [] },
  {
    id: 4,
    label: '🧰 Outils et accompagnement',
    order: 4,
    questions: [
      {
        id: 3,
        question: "Comment fonctionne Protect'Envi ?",
        answer:
          "Protect'Envi permet aux agents assermentés des collectivités de constater officiellement les infractions de dépôts sauvages, de centraliser les preuves et de générer automatiquement les rapports et courriers de mise en demeure.",
        order: 1,
        is_published: true,
      },
    ],
  },
  { id: 5, label: '🚗 Cas particuliers', order: 5, questions: [] },
  { id: 6, label: '👮‍♂️ Assermentation des agents', order: 6, questions: [] },
]

const editModeStore = useEditModeStore()
const isAdminMode = computed(() => editModeStore.isAdminMode)

const categories = ref<FAQCategory[]>([])
const orphans = ref<FAQItem[]>([])
const expandedItems = reactive<Record<number, boolean>>({})

const renderContent = (answer: string) => {
  return answer
}

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

const loadFaq = () => {
  const stored = localStorage.getItem('protect_envi_faq')
  if (stored) {
    const parsed = JSON.parse(stored)
    
    // Check if it uses the nested structure
    if (parsed && parsed.categories && parsed.orphans) {
      categories.value = parsed.categories.map((c: any) => ({
        ...c,
        questions: c.questions || []
      }))
      orphans.value = parsed.orphans
    } else {
      // Migrate from other legacy formats
      const migratedCats: FAQCategory[] = [
        { id: 1, label: '⚖️ Cadre général', order: 1, questions: [] },
        { id: 2, label: '🧾 Déroulement de la procédure', order: 2, questions: [] },
        { id: 3, label: '🔍 Identification des auteurs', order: 3, questions: [] },
        { id: 4, label: '🧰 Outils et accompagnement', order: 4, questions: [] },
        { id: 5, label: '🚗 Cas particuliers', order: 5, questions: [] },
        { id: 6, label: '👮‍♂️ Assermentation des agents', order: 6, questions: [] },
      ]
      const migratedOrphans: FAQItem[] = []
      
      if (parsed.categories && parsed.items) {
        // Flat separated arrays
        parsed.categories.forEach((cat: any) => {
          let target = migratedCats.find(c => c.id === cat.id)
          if (!target) {
            target = { id: cat.id, label: (cat.icon ? `${cat.icon} ` : '') + cat.label, order: cat.order, questions: [] }
            migratedCats.push(target)
          } else {
            target.label = (cat.icon ? `${cat.icon} ` : '') + cat.label
            target.order = cat.order
          }
        })
        parsed.items.forEach((item: any) => {
          const mappedItem: FAQItem = {
            id: item.id,
            question: item.question,
            answer: item.answer,
            order: item.order,
            is_published: item.is_published
          }
          if (item.categoryId === null) {
            migratedOrphans.push(mappedItem)
          } else {
            const target = migratedCats.find(c => c.id === item.categoryId)
            if (target) {
              target.questions.push(mappedItem)
            } else {
              migratedOrphans.push(mappedItem)
            }
          }
        })
      } else if (Array.isArray(parsed)) {
        const hasMixedNodes = parsed.some((item: any) => item.type === 'category' || item.type === 'question')
        if (hasMixedNodes) {
          // FAQNode structure
          parsed.forEach((node: any) => {
            if (node.type === 'category') {
              let target = migratedCats.find(c => c.id === node.id)
              if (!target) {
                target = { id: node.id, label: (node.content ? `${node.content} ` : '') + node.title, order: node.order, questions: [] }
                migratedCats.push(target)
              } else {
                target.label = (node.content ? `${node.content} ` : '') + node.title
                target.order = node.order
              }
            }
          })
          parsed.forEach((node: any) => {
            if (node.type === 'question') {
              const mappedItem: FAQItem = {
                id: node.id,
                question: node.title,
                answer: node.content,
                order: node.order,
                is_published: node.is_published
              }
              if (node.parent_id === null) {
                migratedOrphans.push(mappedItem)
              } else {
                const target = migratedCats.find(c => c.id === node.parent_id)
                if (target) {
                  target.questions.push(mappedItem)
                } else {
                  migratedOrphans.push(mappedItem)
                }
              }
            }
          })
        } else {
          // Flat old items
          const catMap: Record<string, number> = {
            general: 1,
            procedure: 2,
            author: 3,
            tools: 4,
            special: 5,
            agents: 6
          }
          parsed.forEach((item: any) => {
            const catId = catMap[item.category] || 1
            const mappedItem: FAQItem = {
              id: item.id,
              question: item.question,
              answer: item.answer,
              order: item.order,
              is_published: item.is_published
            }
            const target = migratedCats.find(c => c.id === catId)
            if (target) {
              target.questions.push(mappedItem)
            } else {
              migratedOrphans.push(mappedItem)
            }
          })
        }
      }
      
      migratedCats.forEach(c => {
        c.questions.sort((a, b) => a.order - b.order)
      })
      migratedOrphans.sort((a, b) => a.order - b.order)
      
      categories.value = migratedCats
      orphans.value = migratedOrphans
      saveToLocalStorage()
    }
  } else {
    categories.value = JSON.parse(JSON.stringify(DEFAULT_CATEGORIES))
    orphans.value = []
    saveToLocalStorage()
  }
}

const saveToLocalStorage = () => {
  localStorage.setItem(
    'protect_envi_faq',
    JSON.stringify({
      categories: categories.value,
      orphans: orphans.value,
    })
  )
}

const sortedCategories = computed(() => {
  return [...categories.value].sort((a, b) => a.order - b.order)
})

const getFilteredQuestions = (cat: FAQCategory) => {
  return cat.questions
    .filter(item => isAdminMode.value || item.is_published)
    .sort((a, b) => a.order - b.order)
}

const getFilteredOrphans = computed(() => {
  return orphans.value
    .filter(item => isAdminMode.value || item.is_published)
    .sort((a, b) => a.order - b.order)
})

const toggleAccordion = (id: number) => {
  expandedItems[id] = !expandedItems[id]
}

// Category CRUD Actions
const openAddCategoryForm = () => {
  editingId.value = null
  categoryForm.label = ''
  categoryForm.order = categories.value.length > 0 ? Math.max(...categories.value.map(c => c.order)) + 1 : 1
  showCategoryForm.value = true
}

const editCategory = (cat: FAQCategory) => {
  editingId.value = cat.id
  categoryForm.label = cat.label
  categoryForm.order = cat.order
  showCategoryForm.value = true
}

const saveCategory = () => {
  if (editingId.value !== null) {
    const idx = categories.value.findIndex(item => item.id === editingId.value)
    if (idx !== -1) {
      categories.value[idx] = {
        ...categories.value[idx],
        label: categoryForm.label,
        order: categoryForm.order,
      }
    }
  } else {
    const newId = categories.value.length > 0 ? Math.max(...categories.value.map(i => i.id)) + 1 : 1
    categories.value.push({
      id: newId,
      label: categoryForm.label,
      order: categoryForm.order,
      questions: []
    })
  }
  saveToLocalStorage()
  showCategoryForm.value = false
  editingId.value = null
}

const triggerDeleteCategory = (id: number) => {
  deletingCategoryId.value = id
  showDeleteCategoryConfirm.value = true
}

const confirmDeleteCategory = () => {
  if (deletingCategoryId.value !== null) {
    const cat = categories.value.find(c => c.id === deletingCategoryId.value)
    if (cat) {
      // Append children to orphans
      orphans.value.push(...cat.questions)
    }
    categories.value = categories.value.filter(item => item.id !== deletingCategoryId.value)
    saveToLocalStorage()
    showDeleteCategoryConfirm.value = false
    deletingCategoryId.value = null
  }
}

const moveCategory = (currentIndex: number, direction: number) => {
  const cats = [...sortedCategories.value]
  const targetIndex = currentIndex + direction
  if (targetIndex < 0 || targetIndex >= cats.length) return

  const currentCat = cats[currentIndex]
  const targetCat = cats[targetIndex]

  const tempOrder = currentCat.order
  currentCat.order = targetCat.order
  targetCat.order = tempOrder

  const originalCurrent = categories.value.find(i => i.id === currentCat.id)
  const originalTarget = categories.value.find(i => i.id === targetCat.id)
  if (originalCurrent) originalCurrent.order = currentCat.order
  if (originalTarget) originalTarget.order = targetCat.order

  saveToLocalStorage()
}

// Question CRUD Actions
const findQuestionById = (id: number): { item: FAQItem, categoryId: number | null } | null => {
  for (const cat of categories.value) {
    const found = cat.questions.find(q => q.id === id)
    if (found) return { item: found, categoryId: cat.id }
  }
  const foundOrphan = orphans.value.find(o => o.id === id)
  if (foundOrphan) return { item: foundOrphan, categoryId: null }
  return null
}

const removeQuestionFromAll = (id: number) => {
  categories.value.forEach(cat => {
    cat.questions = cat.questions.filter(q => q.id !== id)
  })
  orphans.value = orphans.value.filter(o => o.id !== id)
}

const getMaxQuestionId = () => {
  let maxId = 0
  categories.value.forEach(cat => {
    cat.questions.forEach(q => {
      if (q.id > maxId) maxId = q.id
    })
  })
  orphans.value.forEach(o => {
    if (o.id > maxId) maxId = o.id
  })
  return maxId
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
  form.answer = item.answer
  
  const questionInfo = findQuestionById(item.id)
  form.categoryId = questionInfo ? questionInfo.categoryId : null
  form.order = item.order
  form.is_published = item.is_published
  showForm.value = true
}

const saveItem = () => {
  let finalId = editingId.value
  let finalOrder = form.order

  if (finalId !== null) {
    const originalInfo = findQuestionById(finalId)
    if (originalInfo) {
      if (originalInfo.categoryId !== form.categoryId) {
        if (form.categoryId === null) {
          finalOrder = orphans.value.length > 0 ? Math.max(...orphans.value.map(o => o.order)) + 1 : 1
        } else {
          const targetCat = categories.value.find(c => c.id === form.categoryId)
          finalOrder = targetCat && targetCat.questions.length > 0 ? Math.max(...targetCat.questions.map(q => q.order)) + 1 : 1
        }
      } else {
        finalOrder = originalInfo.item.order
      }
    }
    removeQuestionFromAll(finalId)
  } else {
    finalId = getMaxQuestionId() + 1
    if (form.categoryId === null) {
      finalOrder = orphans.value.length > 0 ? Math.max(...orphans.value.map(o => o.order)) + 1 : 1
    } else {
      const targetCat = categories.value.find(c => c.id === form.categoryId)
      finalOrder = targetCat && targetCat.questions.length > 0 ? Math.max(...targetCat.questions.map(q => q.order)) + 1 : 1
    }
  }

  const mappedItem: FAQItem = {
    id: finalId,
    question: form.question,
    answer: form.answer,
    order: finalOrder,
    is_published: form.is_published
  }

  if (form.categoryId === null) {
    orphans.value.push(mappedItem)
  } else {
    const targetCat = categories.value.find(c => c.id === form.categoryId)
    if (targetCat) {
      targetCat.questions.push(mappedItem)
    }
  }

  saveToLocalStorage()
  showForm.value = false
  editingId.value = null
}

const triggerDeleteItem = (id: number) => {
  deletingItemId.value = id
  showDeleteConfirm.value = true
}

const confirmDeleteItem = () => {
  if (deletingItemId.value !== null) {
    removeQuestionFromAll(deletingItemId.value)
    saveToLocalStorage()
    showDeleteConfirm.value = false
    deletingItemId.value = null
  }
}

const moveItem = (catId: number | null, currentIndex: number, direction: number) => {
  const list = catId !== null 
    ? getFilteredQuestions(categories.value.find(c => c.id === catId)!)
    : getFilteredOrphans.value
  const targetIndex = currentIndex + direction
  if (targetIndex < 0 || targetIndex >= list.length) return

  const currentItem = list[currentIndex]
  const targetItem = list[targetIndex]

  const tempOrder = currentItem.order
  currentItem.order = targetItem.order
  targetItem.order = tempOrder

  saveToLocalStorage()
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
