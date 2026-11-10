import { describe, expect, it } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { buildBreadcrumbLinks } from '../utils/breadcrumb'

const Page = { template: '<div />' }

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: Page, meta: { title: 'Accueil', breadcrumb: false } },
    { path: '/comment-agir', component: Page, meta: { title: 'Comment agir' } },
    {
      path: '/comprendre-la-procedure',
      component: Page,
      meta: { title: 'Comprendre la procédure', breadcrumbParent: '/comment-agir' },
    },
    {
      path: '/blog',
      component: Page,
      meta: { title: 'Blog & Retours d’expérience', breadcrumbLabel: 'Articles' },
    },
    {
      path: '/blog/:slug',
      component: Page,
      meta: { title: 'Article', breadcrumbParent: '/blog' },
    },
    {
      path: '/backoffice',
      redirect: '/utilisateurs-liste',
      meta: { breadcrumbLabel: 'Backoffice' },
    },
    {
      path: '/utilisateurs-liste',
      component: Page,
      meta: {
        title: 'Backoffice - Utilisateurs',
        breadcrumbLabel: 'Utilisateurs',
        breadcrumbParent: '/backoffice',
      },
    },
    {
      path: '/rejoindre',
      component: Page,
      meta: { title: 'Rejoindre le dispositif', hideNavigation: true },
    },
    { path: '/sans-titre', component: Page },
  ],
})

const linksFor = async (path: string, dynamicLabel?: string | null) => {
  await router.push(path)
  return buildBreadcrumbLinks(router.currentRoute.value, router, dynamicLabel)
}

describe('buildBreadcrumbLinks', () => {
  it("n'affiche pas de fil d'Ariane sur l'accueil", async () => {
    expect(await linksFor('/')).toEqual([])
  })

  it('masque le fil sur les pages sans menu de navigation', async () => {
    expect(await linksFor('/rejoindre')).toEqual([])
  })

  it('masque le fil sur une page sans titre plutôt que d’afficher un libellé vide', async () => {
    expect(await linksFor('/sans-titre')).toEqual([])
  })

  it('affiche Accueil > page, la page courante sans lien', async () => {
    expect(await linksFor('/comment-agir')).toEqual([
      { text: 'Accueil', to: '/' },
      { text: 'Comment agir' },
    ])
  })

  it('ajoute la page parente comme niveau intermédiaire cliquable', async () => {
    expect(await linksFor('/comprendre-la-procedure')).toEqual([
      { text: 'Accueil', to: '/' },
      { text: 'Comment agir', to: '/comment-agir' },
      { text: 'Comprendre la procédure' },
    ])
  })

  it('utilise le libellé court plutôt que le titre de l’onglet', async () => {
    expect(await linksFor('/utilisateurs-liste')).toEqual([
      { text: 'Accueil', to: '/' },
      { text: 'Backoffice', to: '/backoffice' },
      { text: 'Utilisateurs' },
    ])
  })

  it('affiche le titre de l’article une fois chargé, le titre générique sinon', async () => {
    expect(await linksFor('/blog/mon-article')).toEqual([
      { text: 'Accueil', to: '/' },
      { text: 'Articles', to: '/blog' },
      { text: 'Article' },
    ])
    expect((await linksFor('/blog/mon-article', 'Un retour d’expérience')).at(-1)).toEqual({
      text: 'Un retour d’expérience',
    })
  })
})
