import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/utility/icons/icons.min.css'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './app.vue'
import { getUserInfo } from './services/api'
import { LOGIN_REQUIRED } from './services/config'
import { initCrisp } from './services/crisp'
import { initMatomo } from './services/matomo'
import { initSentry } from './services/sentry'
import { useAdminModeStore } from './stores/admin-mode'
import './styles/premium-design.css'

const pinia = createPinia()

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition && !to.hash) {
      return savedPosition
    }
    if (to.hash) {
      try {
        if (document.querySelector(to.hash)) {
          return { el: to.hash }
        }
      } catch (e) {
        // Ignore if the hash is not a valid query selector
      }
      return false
    }

    // Avoid scroll to top when toggling or switching between Tally modals on the same parent page
    const isTallyToParent = to.meta.tallyParent === from.path || from.meta.tallyParent === to.path
    const isTallySameParent = to.meta.tallyParent && to.meta.tallyParent === from.meta.tallyParent
    if (isTallyToParent || isTallySameParent) {
      return false
    }

    // Avoid scroll to top when navigating within the FAQ
    if (to.path.startsWith('/faq') && from.path.startsWith('/faq')) {
      return false
    }

    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      component: () => import('./pages/accueil.vue'),
      meta: { title: 'Accueil', breadcrumb: false },
    },
    {
      path: '/simulateur',
      name: 'Simulateur',
      component: () => import('./pages/accueil.vue'),
      meta: { title: "Simulateur d'amende pour dépôt sauvage", tallyParent: '/', breadcrumb: false },
    },
    {
      path: '/calculateur',
      name: 'Calculateur',
      component: () => import('./pages/accueil.vue'),
      meta: { title: "Calculateur d'amende", tallyParent: '/', breadcrumb: false },
    },
    {
      path: '/comprendre-la-procedure',
      name: 'ComprendreProcedure',
      component: () => import('./pages/comprendre-la-procedure.vue'),
      meta: { breadcrumbBand: true, title: 'Comprendre la procédure', breadcrumbParent: '/comment-agir' },
    },
    {
      path: '/mes-procedures',
      name: 'MesProcedures',
      component: () => import('./pages/mes-procedures.vue'),
      meta: { title: 'Mes procédures', fullWidth: true },
    },
    {
      path: '/acces-restreint',
      name: 'AccesRestreint',
      component: () => import('./pages/acces-restreint.vue'),
      meta: { breadcrumbBand: true, title: 'Accès réservé - Demande d’accès', breadcrumbLabel: 'Accès réservé' },
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('./pages/contact.vue'),
      meta: { breadcrumbBand: true, title: 'Contact' },
    },
    {
      path: '/joindre',
      redirect: '/demarche-numerique-rejoindre-stop-depot-sauvage',
    },
    {
      path: '/signalements-dn/:dossier_id',
      redirect: (to) => ({
        name: 'SuiviProcedure',
        params: { constatation_id: to.params.dossier_id },
      }),
    },
    {
      path: '/rejoindre-le-dispositif',
      redirect: '/demarche-numerique-rejoindre-stop-depot-sauvage',
    },
    {
      path: '/demarche-numerique-rejoindre-protectenvi',
      redirect: '/demarche-numerique-rejoindre-stop-depot-sauvage',
    },
    {
      path: '/demarche-numerique-rejoindre-stop-depot-sauvage',
      name: 'DemarcheNumeriqueRejoindreStopDepotSauvage',
      component: () => import('./pages/demarche-numerique-rejoindre-protectenvi.vue'),
      meta: { hideNavigation: true, title: 'Rejoindre le dispositif', breadcrumb: false },
    },
    {
      path: '/suivi-procedure/:constatation_id',
      name: 'SuiviProcedure',
      component: () => import('./pages/suivi-procedure.vue'),
      meta: {
        activeMenu: '/mes-procedures',
        title: 'Suivi de procédure',
        breadcrumbParent: '/mes-procedures',
      },
    },
    {
      path: '/rdv',
      name: 'RDV',
      component: () => import('./pages/rdv.vue'),
      meta: { breadcrumbBand: true, title: 'Prendre rendez-vous' },
    },
    {
      path: '/rdv/etre-informe',
      name: 'RDVEtreInforme',
      component: () => import('./pages/rdv.vue'),
      meta: { breadcrumbBand: true, title: 'Prendre rendez-vous' },
    },
    {
      path: '/login-demo',
      name: 'LoginDemo',
      component: () => import('./pages/login-demo.vue'),
      meta: { title: 'Connexion démo', breadcrumb: false },
    },
    {
      path: '/demarrer-constatation',
      name: 'ConstatationStart',
      component: () => import('./pages/commencer-constatation.vue'),
      meta: { title: 'Démarrer une constatation', breadcrumbParent: '/mes-procedures' },
    },
    {
      path: '/demarrer-constatation/simulateur',
      name: 'ConstatationStartSimulateur',
      component: () => import('./pages/commencer-constatation.vue'),
      meta: {
        title: "Simulateur d'éligibilité",
        tallyParent: '/demarrer-constatation',
        breadcrumbLabel: 'Démarrer une constatation',
        breadcrumbParent: '/mes-procedures',
      },
    },
    {
      path: '/constatation',
      name: 'ConstatationForm',
      component: () => import('./pages/constatation-form.vue'),
      meta: { title: 'Créer une constatation', breadcrumbParent: '/mes-procedures' },
    },
    {
      path: '/constatation/:id',
      name: 'ConstatationEditForm',
      component: () => import('./pages/constatation-form.vue'),
      meta: { title: 'Modifier la constatation', breadcrumbParent: '/mes-procedures' },
    },
    {
      path: '/constatation-fin/:id',
      name: 'ConstatationSuccess',
      component: () => import('./pages/constatation-fin.vue'),
      meta: { title: 'Constatation enregistrée', breadcrumbParent: '/mes-procedures' },
    },
    {
      path: '/faq/:slug?',
      name: 'FAQ',
      component: () => import('./pages/faq.vue'),
      meta: { breadcrumbBand: true, title: 'Foire Aux Questions', breadcrumbLabel: 'Foire aux questions' },
    },
    {
      path: '/blog',
      name: 'Blog',
      component: () => import('./pages/blog.vue'),
      meta: { breadcrumbBand: true, title: 'Blog & Retours d’expérience', breadcrumbLabel: 'Articles' },
    },
    {
      path: '/blog/:slug',
      name: 'BlogArticle',
      // The real title is known only after fetching article data: page triggers trackPageView itself
      component: () => import('./pages/blog-article.vue'),
      meta: { title: 'Article', deferPageView: true, breadcrumbParent: '/blog' },
    },
    {
      path: '/backoffice',
      redirect: '/tableau-de-bord',
      meta: { breadcrumbLabel: 'Backoffice' },
    },
    {
      path: '/tableau-de-bord',
      name: 'DashboardBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: {
        title: 'Backoffice - Tableau de bord',
        breadcrumbLabel: 'Tableau de bord',
        breadcrumbParent: '/backoffice',
        requiresStaff: true,
        tab: 'dashboard',
        activeMenu: '/backoffice',
      },
    },
    {
      path: '/procedures-liste',
      name: 'ProceduresListBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: {
        title: 'Backoffice - Liste des procédures',
        breadcrumbLabel: 'Liste des procédures',
        breadcrumbParent: '/backoffice',
        requiresStaff: true,
        tab: 'list',
        activeMenu: '/backoffice',
      },
    },
    {
      path: '/procedure-detail/:procedureId?',
      name: 'ProcedureDetailBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: {
        title: 'Backoffice - Détail de la procédure',
        breadcrumbLabel: 'Détail de la procédure',
        breadcrumbParent: '/backoffice',
        requiresStaff: true,
        tab: 'detail',
        activeMenu: '/backoffice',
      },
    },
    {
      path: '/utilisateurs-liste',
      name: 'UsersListBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: {
        title: 'Backoffice - Utilisateurs',
        breadcrumbLabel: 'Utilisateurs',
        breadcrumbParent: '/backoffice',
        requiresStaff: true,
        tab: 'users',
        activeMenu: '/backoffice',
      },
    },
    {
      path: '/proconnect-acces',
      name: 'ProConnectAccesBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: {
        title: 'Backoffice - Règles d’accès ProConnect',
        breadcrumbLabel: 'Règles d’accès ProConnect',
        breadcrumbParent: '/backoffice',
        requiresStaff: true,
        tab: 'proconnect',
        activeMenu: '/backoffice',
      },
    },

    {
      path: '/mentions-legales',
      name: 'MentionsLegales',
      component: () => import('./pages/mentions-legales.vue'),
      meta: { breadcrumbBand: true, title: 'Mentions légales' },
    },
    {
      path: '/donnees-personnelles',
      name: 'DonneesPersonnelles',
      component: () => import('./pages/donnees-personnelles.vue'),
      meta: { breadcrumbBand: true, title: 'Données personnelles' },
    },
    {
      path: '/a11y',
      name: 'Accessibilite',
      component: () => import('./pages/a11y.vue'),
      meta: { breadcrumbBand: true, title: 'Accessibilité' },
    },
    {
      path: '/cookies',
      name: 'Cookies',
      component: () => import('./pages/cookies.vue'),
      meta: { breadcrumbBand: true, title: 'Gestion des cookies' },
    },
    {
      path: '/cgu',
      name: 'CGU',
      component: () => import('./pages/cgu.vue'),
      meta: { breadcrumbBand: true, title: 'Conditions générales d’utilisation' },
    },
    {
      path: '/plan-du-site',
      name: 'PlanDuSite',
      component: () => import('./pages/plan-du-site.vue'),
      meta: { breadcrumbBand: true, title: 'Plan du site' },
    },
    {
      path: '/comment-agir',
      name: 'CommentAgir',
      component: () => import('./pages/comment-agir.vue'),
      meta: { breadcrumbBand: true, title: 'Comment agir' },
    },
    {
      path: '/comment-agir/etre-informe',
      name: 'CommentAgirEtreInforme',
      component: () => import('./pages/comment-agir.vue'),
      meta: { breadcrumbBand: true, title: 'Comment agir' },
    },
  ],
})

router.beforeEach(async (to) => {
  if (to.matched.some((record) => record.meta.requiresStaff)) {
    try {
      const userInfo = await getUserInfo()
      const adminModeStore = useAdminModeStore()
      if (!userInfo.is_authenticated || !userInfo.is_staff || !adminModeStore.isAdminMode) {
        return '/'
      }
    } catch (error) {
      console.error('Error checking staff status:', error)
      return '/'
    }
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    try {
      const userInfo = await getUserInfo()
      if (LOGIN_REQUIRED && !userInfo.is_authenticated) {
        return '/'
      }
    } catch (error) {
      console.error('Error checking auth:', error)
      return '/'
    }
  }
})

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(VueDsfr)

initSentry(app, router)
initMatomo(router)
initCrisp()

app.mount('#app')
