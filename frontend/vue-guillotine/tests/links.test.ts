import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BlockRenderer from '../BlockRenderer.vue'
import { cleanHtmlLinks, isInternalUrl, normalizeLinkHref } from '../utils/linkUtils.js'

describe('vue-guillotine link handling', () => {
  describe('isInternalUrl', () => {
    it('detects relative URLs as internal', () => {
      expect(isInternalUrl('/')).toBe(true)
      expect(isInternalUrl('/calculateur')).toBe(true)
      expect(isInternalUrl('/blog/mon-article?query=1#ancre')).toBe(true)
      expect(isInternalUrl('#section')).toBe(true)
    })

    it('detects internal domain names as internal', () => {
      expect(isInternalUrl('https://stopdepotsauvage.beta.gouv.fr')).toBe(true)
      expect(isInternalUrl('https://www.stopdepotsauvage.beta.gouv.fr/calculateur')).toBe(true)
      expect(isInternalUrl('https://stop-depot-sauvage.beta.gouv.fr')).toBe(true)
      expect(isInternalUrl('https://protect-envi.beta.gouv.fr')).toBe(true)
      expect(isInternalUrl('https://protect-envi.beta.gouv.fr/demarrer-constatation')).toBe(true)
      expect(isInternalUrl('https://depots-sauvages.beta.gouv.fr/contact')).toBe(true)
      expect(isInternalUrl('http://localhost:5173/page')).toBe(true)
      expect(isInternalUrl('http://127.0.0.1:8000/api')).toBe(true)
    })

    it('detects external URLs as external', () => {
      expect(
        isInternalUrl('https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000037200843')
      ).toBe(false)
      expect(isInternalUrl('https://google.com')).toBe(false)
      expect(isInternalUrl('https://proconnect.crisp.help/fr/article/test')).toBe(false)
    })

    it('detects mailto and tel as internal', () => {
      expect(isInternalUrl('mailto:contact@depots-sauvages.beta.gouv.fr')).toBe(true)
      expect(isInternalUrl('tel:0123456789')).toBe(true)
    })
  })

  describe('normalizeLinkHref', () => {
    it('converts absolute URLs of current platform to relative paths', () => {
      expect(normalizeLinkHref('https://protect-envi.beta.gouv.fr/calculateur')).toBe(
        '/calculateur'
      )
      expect(
        normalizeLinkHref('https://protect-envi.beta.gouv.fr/demarrer-constatation?foo=bar#section')
      ).toBe('/demarrer-constatation?foo=bar#section')
    })

    it('leaves relative and external URLs unchanged', () => {
      expect(normalizeLinkHref('/deja-relatif')).toBe('/deja-relatif')
      expect(normalizeLinkHref('https://www.legifrance.gouv.fr/article')).toBe(
        'https://www.legifrance.gouv.fr/article'
      )
    })
  })

  describe('cleanHtmlLinks', () => {
    it('cleans internal and external links in HTML string', () => {
      const html =
        '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://protect-envi.beta.gouv.fr/calculateur">Calculateur</a> et <a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://google.com">Google</a></p>'
      const cleaned = cleanHtmlLinks(html)
      expect(cleaned).toContain('href="/calculateur"')
      expect(cleaned).not.toContain(
        'target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://protect-envi'
      )
      expect(cleaned).toContain('href="https://google.com"')
      expect(cleaned).toContain('rel="noopener noreferrer"')
      expect(cleaned).not.toContain('nofollow')
    })
  })

  describe('BlockRenderer rendering links', () => {
    it('removes target="_blank" and rel="nofollow" on internal links', () => {
      const blocks = [
        {
          type: 'rich_text',
          value:
            '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://protect-envi.beta.gouv.fr/demarrer-constatation">Démarrer</a></p>',
        },
      ]
      const wrapper = mount(BlockRenderer, {
        props: { blocks },
      })

      const link = wrapper.find('a')
      expect(link.exists()).toBe(true)
      expect(link.attributes('href')).toBe('/demarrer-constatation')
      expect(link.attributes('target')).toBeUndefined()
      expect(link.attributes('rel')).toBeUndefined()
      expect(link.classes()).toContain('fr-link')
    })

    it('keeps target="_blank" and rel="noopener noreferrer" on external links without nofollow', () => {
      const blocks = [
        {
          type: 'rich_text',
          value:
            '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" href="https://www.legifrance.gouv.fr/codes/article">Legifrance</a></p>',
        },
      ]
      const wrapper = mount(BlockRenderer, {
        props: { blocks },
      })

      const link = wrapper.find('a')
      expect(link.exists()).toBe(true)
      expect(link.attributes('href')).toBe('https://www.legifrance.gouv.fr/codes/article')
      expect(link.attributes('target')).toBe('_blank')
      expect(link.attributes('rel')).toBe('noopener noreferrer')
    })
  })
})
