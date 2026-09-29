import '@testing-library/jest-dom'
import { fireEvent, render } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import BlockRenderer from '../vue-guillotine/BlockRenderer.vue'
import { classifyLink, processLinks } from '../vue-guillotine/utils/links.js'

const push = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({ push }),
}))

const HOST = 'localhost:8000'

describe('classifyLink', () => {
  it.each([
    ['/faq/une-question', 'internal'],
    ['https://stopdepotsauvage.beta.gouv.fr/blog/article', 'internal'],
    ['https://protectenvi.beta.gouv.fr/faq', 'internal'],
    ['https://staging.stop-depot-sauvage.beta.gouv.fr/blog', 'internal'],
    ['https://cellar-c2.services.clever-cloud.com/bucket/guide.pdf', 'external'],
    [`http://${HOST}/contact`, 'internal'],
    ['#section', 'anchor'],
    ['/media/documents/guide.pdf', 'file'],
    ['https://stopdepotsauvage.beta.gouv.fr/static/modele.docx', 'file'],
    ['https://www.legifrance.gouv.fr/codes/article', 'external'],
    ['mailto:contact@example.com', 'other'],
  ])('%s -> %s', (href, expected) => {
    expect(classifyLink(href, HOST)).toBe(expected)
  })
})

// Rattache le HTML au document de test (les assertions DOM l'exigent)
const parse = (html: string) => {
  const container = document.createElement('div')
  container.innerHTML = html
  return container
}

describe('processLinks', () => {
  it('ouvre les pages du site dans le même onglet, sans nofollow, en lien relatif', () => {
    const html = processLinks(
      '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://stopdepotsauvage.beta.gouv.fr/faq/x#y">FAQ</a></p>',
      HOST
    )
    const link = parse(html).querySelector('a')!
    expect(link.getAttribute('href')).toBe('/faq/x#y')
    expect(link).not.toHaveAttribute('target')
    expect(link).not.toHaveAttribute('rel')
    expect(link).toHaveClass('fr-link')
  })

  it('ouvre les autres sites et les fichiers dans un nouvel onglet avec noopener', () => {
    const html = processLinks(
      '<a href="https://www.legifrance.gouv.fr">Légifrance</a><a href="/media/guide.pdf">Guide</a>',
      HOST
    )
    const links = parse(html).querySelectorAll('a')
    links.forEach((link) => {
      expect(link).toHaveAttribute('target', '_blank')
      expect(link).toHaveAttribute('rel', 'noopener noreferrer')
      expect(link).toHaveAttribute('title', `${link.textContent} - nouvelle fenêtre`)
    })
  })
})

describe('BlockRenderer', () => {
  const blocks = [
    {
      type: 'rich_text',
      value:
        '<p><a target="_blank" href="/blog/article">Interne</a> <a href="https://www.legifrance.gouv.fr">Externe</a></p>',
    },
  ]

  it('navigue sans recharger la page pour un lien interne', async () => {
    push.mockClear()
    const { getByText } = render(BlockRenderer, { props: { blocks } })
    await fireEvent.click(getByText('Interne'))
    expect(push).toHaveBeenCalledWith('/blog/article')
  })

  it('laisse le navigateur gérer un lien externe', async () => {
    push.mockClear()
    const { getByText } = render(BlockRenderer, { props: { blocks } })
    expect(getByText('Externe')).toHaveAttribute('target', '_blank')
    await fireEvent.click(getByText('Externe'))
    expect(push).not.toHaveBeenCalled()
  })
})
