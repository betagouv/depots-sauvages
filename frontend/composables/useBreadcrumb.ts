import { ref } from 'vue'

// Label known only after loading data (e.g. blog article title); reset by the layout on navigation.
const dynamicLabel = ref<string | null>(null)

export function useBreadcrumb() {
  const setCurrentPageLabel = (label: string | null) => {
    dynamicLabel.value = label
  }
  return { dynamicLabel, setCurrentPageLabel }
}
