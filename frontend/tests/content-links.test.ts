import '@testing-library/jest-dom'
import { fireEvent, render } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import BlockRenderer from '../vue-guillotine/BlockRenderer.vue'
import { getLinkTarget, processLinks } from '../vue-guillotine/utils/links.js'

const push = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({ push }),
}))

const SITE_HOSTS = ['stopdepotsauvage.beta.gouv.fr', 'stop-depot-sauvage.beta.gouv.fr']

const parse = (html: string) => {
  const container = document.createElement('div')
  container.innerHTML = html
  return container
}

describe('getLinkTarget', () => {
  it.each([
    ['/faq/une-question', { internalPath: '/faq/une-question' }],
    ['https://stopdepotsauvage.beta.gouv.fr/blog/a?x=1#y', { internalPath: '/blog/a?x=1#y' }],
    ['https://staging.stop-depot-sauvage.beta.gouv.fr/blog', { internalPath: '/blog' }],
    [`${window.location.origin}/contact`, { internalPath: '/contact' }],
    ['/media/documents/guide.pdf', { newTab: true }],
    ['https://stopdepotsauvage.beta.gouv.fr/static/modele.docx', { newTab: true }],
    ['https://www.legifrance.gouv.fr/codes/article', { newTab: true }],
    ['https://cellar-c2.services.clever-cloud.com/bucket/guide.pdf', { newTab: true }],
    ['#section', {}],
    ['mailto:contact@example.com', {}],
  ])('%s', (href, expected) => {
    expect(getLinkTarget(href, SITE_HOSTS)).toEqual(expected)
  })
})

describe('processLinks', () => {
  it('ouvre les pages du site dans le même onglet, sans nofollow, en lien relatif', () => {
    const html = processLinks(
      '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://stopdepotsauvage.beta.gouv.fr/faq/x#y">FAQ</a></p>',
      SITE_HOSTS
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
      SITE_HOSTS
    )
    parse(html)
      .querySelectorAll('a')
      .forEach((link) => {
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
