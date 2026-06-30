/**
 * Prevents typing non-numeric characters (e, E, +, -) in a type="number" input
 */
export const onKeyDownNumber = (event: KeyboardEvent) => {
  if (['e', 'E', '+', '-'].includes(event.key)) {
    event.preventDefault()
  }
}
