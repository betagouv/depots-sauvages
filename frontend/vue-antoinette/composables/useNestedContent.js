import { computed, ref } from 'vue'

export function useNestedContent(apiUrl, apiHelpers) {
  const { fetchResource, createResource, patchResource, deleteResource, postResource } = apiHelpers

  const topLevel = ref([])
  const orphans = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const items = computed(() => [...topLevel.value, ...orphans.value])

  const load = async () => {
    isLoading.value = true
    error.value = null
    try {
      const data = await fetchResource(`${apiUrl}/`)
      topLevel.value = data.top_level || []
      orphans.value = data.orphans || []
    } catch (err) {
      error.value = err
      console.error('Error loading content:', err)
    } finally {
      isLoading.value = false
    }
  }

  const moveUp = async (id) => {
    try {
      await postResource(`${apiUrl}/${id}/move-up/`)
      await load()
    } catch (err) {
      console.error('Error moving item up:', err)
    }
  }

  const moveDown = async (id) => {
    try {
      await postResource(`${apiUrl}/${id}/move-down/`)
      await load()
    } catch (err) {
      console.error('Error moving item down:', err)
    }
  }

  const deleteItem = async (id) => {
    try {
      await deleteResource(`${apiUrl}/${id}/`)
      await load()
    } catch (err) {
      console.error('Error deleting item:', err)
    }
  }

  const saveItem = async (id, payload) => {
    try {
      let result
      if (id !== null && id !== undefined) {
        result = await patchResource(`${apiUrl}/${id}/`, payload)
      } else {
        result = await createResource(`${apiUrl}/`, payload)
      }
      await load()
      return result
    } catch (err) {
      console.error('Error saving item:', err)
      throw err
    }
  }

  return {
    items,
    isLoading,
    error,
    topLevel,
    orphans,
    load,
    moveUp,
    moveDown,
    deleteItem,
    saveItem,
  }
}
