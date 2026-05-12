import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import '@gouvfr/dsfr/dist/utility/icons/icons.min.css'
import './styles/premium-design.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './app.vue'
import { getUserInfo } from './services/api'
import { initMatomo } from './services/matomo'
import { initCrisp } from './services/crisp'

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
    return { top: 0 }
  },
  routes: [
    {
      path: '/',
      component: () => import('./pages/accueil.vue'),
    },
    {
      path: '/comprendre-la-procedure',
      name: 'ComprendreProcedure',
      component: () => import('./pages/comprendre-la-procedure.vue'),
    },
    {
      path: '/mes-procedures',
      name: 'MesProcedures',
      component: () => import('./pages/mes-procedures.vue'),
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('./pages/contact.vue'),
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
      meta: { hideNavigation: true },
    },
    {
      path: '/suivi-procedure/:dossier_id',
      name: 'SuiviProcedure',
      component: () => import('./pages/suivi-procedure.vue'),
      meta: { activeMenu: '/mes-procedures' },
    },
    {
      path: '/rdv',
      name: 'RDV',
      component: () => import('./pages/rdv.vue'),
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    try {
      const userInfo = await getUserInfo()
      const loginRequired = import.meta.env.VITE_LOGIN_REQUIRED !== 'false'
      if (loginRequired && !userInfo.is_authenticated) {
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
