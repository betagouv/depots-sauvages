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

    // Avoid scroll to top when switching between home, simulateur and calculateur
    const tallyRoutes = ['/', '/simulateur', '/calculateur']
    if (tallyRoutes.includes(to.path) && tallyRoutes.includes(from.path)) {
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
      meta: { title: 'Accueil' },
    },
    {
      path: '/simulateur',
      name: 'Simulateur',
      component: () => import('./pages/accueil.vue'),
      meta: { title: "Simulateur d'amende pour dépôt sauvage" },
    },
    {
      path: '/calculateur',
      name: 'Calculateur',
      component: () => import('./pages/accueil.vue'),
      meta: { title: 'Calculateur de préjudice' },
    },
    {
      path: '/comprendre-la-procedure',
      name: 'ComprendreProcedure',
      component: () => import('./pages/comprendre-la-procedure.vue'),
      meta: { title: 'Comprendre la procédure' },
    },
    {
      path: '/mes-procedures',
      name: 'MesProcedures',
      component: () => import('./pages/mes-procedures.vue'),
      meta: { title: 'Mes procédures' },
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('./pages/contact.vue'),
      meta: { title: 'Contact' },
    },
    {
      path: '/joindre',
      redirect: '/demarche-numerique-rejoindre-protectenvi',
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
      redirect: '/demarche-numerique-rejoindre-protectenvi',
    },
    {
      path: '/demarche-numerique-rejoindre-protectenvi',
      name: 'DemarcheNumeriqueRejoindreProtectEnvi',
      component: () => import('./pages/demarche-numerique-rejoindre-protectenvi.vue'),
      meta: { hideNavigation: true, title: 'Rejoindre le dispositif' },
    },
    {
      path: '/suivi-procedure/:constatation_id',
      name: 'SuiviProcedure',
      component: () => import('./pages/suivi-procedure.vue'),
      meta: { activeMenu: '/mes-procedures', title: 'Suivi de procédure' },
    },
    {
      path: '/rdv',
      name: 'RDV',
      component: () => import('./pages/rdv.vue'),
      meta: { title: 'Prendre rendez-vous' },
    },
    {
      path: '/login-demo',
      name: 'LoginDemo',
      component: () => import('./pages/login-demo.vue'),
      meta: { title: 'Connexion démo' },
    },
    {
      path: '/demarrer-constatation',
      name: 'ConstatationStart',
      component: () => import('./pages/commencer-constatation.vue'),
      meta: { title: 'Démarrer une constatation' },
    },
    {
      path: '/constatation',
      name: 'ConstatationForm',
      component: () => import('./pages/constatation-form.vue'),
      meta: { title: 'Créer une constatation' },
    },
    {
      path: '/constatation/:id',
      name: 'ConstatationEditForm',
      component: () => import('./pages/constatation-form.vue'),
      meta: { title: 'Modifier la constatation' },
    },
    {
      path: '/constatation-fin/:id',
      name: 'ConstatationSuccess',
      component: () => import('./pages/constatation-fin.vue'),
      meta: { title: 'Constatation enregistrée' },
    },
    {
      path: '/faq/:slug?',
      name: 'FAQ',
      component: () => import('./pages/faq.vue'),
      meta: { title: 'Foire Aux Questions' },
    },
    {
      path: '/backoffice',
      redirect: '/tableau-de-bord',
    },
    {
      path: '/tableau-de-bord',
      name: 'DashboardBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: { title: 'Backoffice - Tableau de bord', requiresStaff: true, tab: 'dashboard', activeMenu: '/backoffice' },
    },
    {
      path: '/procedures-liste',
      name: 'ProceduresListBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: { title: 'Backoffice - Liste des procédures', requiresStaff: true, tab: 'list', activeMenu: '/backoffice' },
    },
    {
      path: '/procedure-detail/:procedureId?',
      name: 'ProcedureDetailBackoffice',
      component: () => import('./pages/backoffice.vue'),
      meta: { title: 'Backoffice - Détail de la procédure', requiresStaff: true, tab: 'detail', activeMenu: '/backoffice' },
    },
    {
      path: '/mentions-legales',
      name: 'MentionsLegales',
      component: () => import('./pages/mentions-legales.vue'),
    },
    {
      path: '/donnees-personnelles',
      name: 'DonneesPersonnelles',
      component: () => import('./pages/donnees-personnelles.vue'),
    },
    {
      path: '/a11y',
      name: 'Accessibilite',
      component: () => import('./pages/a11y.vue'),
    },
    {
      path: '/cookies',
      name: 'Cookies',
      component: () => import('./pages/cookies.vue'),
    },
    {
      path: '/cgu',
      name: 'CGU',
      component: () => import('./pages/cgu.vue'),
    },
    {
      path: '/plan-du-site',
      name: 'PlanDuSite',
      component: () => import('./pages/plan-du-site.vue'),
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

initMatomo(router)
initCrisp()

app.mount('#app')
