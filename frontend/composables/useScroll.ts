export function useScroll() {
  const scrollToTop = () => {
    window.scrollTo(0, 0)
  }

  return { scrollToTop }
}
