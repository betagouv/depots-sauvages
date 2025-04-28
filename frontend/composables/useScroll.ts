import { ref } from 'vue'

export function useScroll() {
  const stepperRef = ref<HTMLElement | null>(null)

  const scrollToTop = () => {
    const stepper = document.querySelector('.waste-report')
    if (stepper) {
      stepper.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return {
    scrollToTop,
  }
}
