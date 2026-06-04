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
import './styles/premium-design.css'

const pinia = createPinia()

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { el: to.hash }
    }

    // Empêcher le défilement vers le haut lors de la navigation entre l'accueil et les popups Tally
    const tallyRoutes = ['/', '/simulateur', '/calculateur']
    if (tallyRoutes.includes(to.path) && tallyRoutes.includes(from.path)) {
      return false
    }

    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      component: () => import('./pages/accueil.vue'),
      meta: { title: "Accueil" },
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
      meta: { title: "Calculateur de préjudice" },
    },
    {
      path: '/comprendre-la-procedure',
      name: 'ComprendreProcedure',
      component: () => import('./pages/comprendre-la-procedure.vue'),
      meta: { title: "Comprendre la procédure" },
    },
    {
      path: '/mes-procedures',
      name: 'MesProcedures',
      component: () => import('./pages/mes-procedures.vue'),
      meta: { title: "Mes procédures" },
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('./pages/contact.vue'),
      meta: { title: "Contact" },
    },
    {
      path: '/joindre',
      redirect: '/demarche-numerique-rejoindre-protectenvi',
    },
    {
      path: '/signalements-dn/:dossier_id',
      redirect: (to) => ({ name: 'SuiviProcedure', params: { dossier_id: to.params.dossier_id } }),
    },
    {
      path: '/rejoindre-le-dispositif',
      redirect: '/demarche-numerique-rejoindre-protectenvi',
    },
    {
      path: '/demarche-numerique-rejoindre-protectenvi',
      name: 'DemarcheNumeriqueRejoindreProtectEnvi',
      component: () => import('./pages/demarche-numerique-rejoindre-protectenvi.vue'),
      meta: { hideNavigation: true, title: "Rejoindre le dispositif" },
    },
    {
      path: '/suivi-procedure/:dossier_id',
      name: 'SuiviProcedure',
      component: () => import('./pages/suivi-procedure.vue'),
      meta: { activeMenu: '/mes-procedures', title: "Suivi de procédure" },
    },
    {
      path: '/rdv',
      name: 'RDV',
      component: () => import('./pages/rdv.vue'),
      meta: { title: "Prendre rendez-vous" },
    },
    {
      path: '/login-demo',
      name: 'LoginDemo',
      component: () => import('./pages/login-demo.vue'),
      meta: { title: "Connexion démo" },
    },
    {
      path: '/demarrer-constatation',
      name: 'ConstatationStart',
      component: () => import('./pages/commencer-constatation.vue'),
      meta: { title: "Démarrer une constatation" },
    },
    {
      path: '/constatation',
      name: 'ConstatationForm',
      component: () => import('./pages/constatation-form.vue'),
      meta: { title: "Créer une constatation" },
    },
    {
      path: '/constatation/:id',
      name: 'ConstatationEditForm',
      component: () => import('./pages/constatation-form.vue'),
      meta: { title: "Modifier la constatation" },
    },
    {
      path: '/constatation-fin/:id',
      name: 'ConstatationSuccess',
      component: () => import('./pages/constatation-fin.vue'),
      meta: { title: "Constatation enregistrée" },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    try {
      const userInfo = await getUserInfo()
      if (LOGIN_REQUIRED && !userInfo.is_authenticated) {
        next('/')
        return
      }
    } catch (error) {
      console.error('Error checking auth:', error)
      next('/')
      return
    }
  }
  next()
})

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(VueDsfr)

initMatomo(router)
initCrisp()

app.mount('#app')
