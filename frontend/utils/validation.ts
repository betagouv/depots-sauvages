/**
 * Converts a value to a number or returns null if it is invalid or empty.
 */
export const toNumOrNull = (v: any): number | null => {
  const n = Number(v)
  return v == null || v === '' || isNaN(n) ? null : n
}

/**
 * Validates that a required value is a positive number or zero.
 */
export const validateRequiredPositiveNumber = (
  val: any,
  fieldName: string,
  errors: Record<string, string>,
  requiredMsg: string = 'Ce champ est obligatoire'
) => {
  const num = toNumOrNull(val)
  if (num === null) {
    errors[fieldName] = requiredMsg
  } else if (num < 0) {
    errors[fieldName] = 'La valeur doit être supérieure ou égale à 0'
  }
}

/**
 * Validates that an optional value is a positive number or zero if specified.
 */
export const validateOptionalPositiveNumber = (
  val: any,
  fieldName: string,
  errors: Record<string, string>
) => {
  const num = toNumOrNull(val)
  if (num !== null && num < 0) {
    errors[fieldName] = 'La valeur doit être supérieure ou égale à 0'
  }
}
