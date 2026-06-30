/**
 * Smoothly scrolls the page to the target element with native smooth scroll and top offset.
 */
export const smoothScrollTo = (element: HTMLElement, duration = 800, offset = 100) => {
  const targetPosition = element.getBoundingClientRect().top + window.scrollY - offset
  window.scrollTo({
    top: targetPosition,
    behavior: 'smooth'
  })
}

