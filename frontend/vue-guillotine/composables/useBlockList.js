import { ref } from 'vue'

export function useBlockList(initialBlocks = []) {
  const blocks = ref([...initialBlocks])

  const addBlock = (type, value = '') => {
    blocks.value.push({ type, value })
  }

  const removeBlock = (index) => {
    if (index >= 0 && index < blocks.value.length) {
      blocks.value.splice(index, 1)
    }
  }

  const moveBlock = (index, direction) => {
    const targetIndex = index + direction
    if (targetIndex < 0 || targetIndex >= blocks.value.length) return

    const temp = blocks.value[index]
    blocks.value[index] = blocks.value[targetIndex]
    blocks.value[targetIndex] = temp
  }

  return {
    blocks,
    addBlock,
    removeBlock,
    moveBlockUp: (index) => moveBlock(index, -1),
    moveBlockDown: (index) => moveBlock(index, 1),
  }
}
