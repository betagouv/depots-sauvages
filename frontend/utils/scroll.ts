/**
 * Smoothly scrolls the page to the target element with custom easing, duration, and top offset.
 */
export const smoothScrollTo = (element: HTMLElement, duration = 800, offset = 100) => {
  const targetPosition = element.getBoundingClientRect().top + window.scrollY - offset
  const startPosition = window.scrollY
  const distance = targetPosition - startPosition
  let startTime: number | null = null

  const easeInOutQuad = (t: number, b: number, c: number, d: number) => {
    t /= d / 2
    if (t < 1) return (c / 2) * t * t + b
    t--
    return (-c / 2) * (t * (t - 2) - 1) + b
  }

  const animation = (currentTime: number) => {
    if (startTime === null) startTime = currentTime
    const timeElapsed = currentTime - startTime
    const run = easeInOutQuad(timeElapsed, startPosition, distance, duration)
    window.scrollTo(0, run)
    if (timeElapsed < duration) {
      requestAnimationFrame(animation)
    } else {
      window.scrollTo(0, targetPosition)
    }
  }

  requestAnimationFrame(animation)
}
