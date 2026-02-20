import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock HTMLCanvasElement.prototype.getContext for axe-core accessibility tests
if (typeof HTMLCanvasElement !== 'undefined') {
  HTMLCanvasElement.prototype.getContext = vi.fn()
}
