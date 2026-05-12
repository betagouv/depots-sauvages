import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import '@gouvfr/dsfr/dist/utility/icons/icons.min.css'
import './styles/premium-design.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import VueMatomo from 'vue-matomo'
import { createRouter, createWebHistory } from 'vue-router'
import App from './app.vue'
import { getUserInfo } from './services/api'

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

// Matomo initialization (Manual approach for better compatibility with Vite 8/Vue 3.5)
const matomoEnabled = import.meta.env.VITE_MATOMO_ENABLED === 'true' || import.meta.env.VITE_MATOMO_ENABLED === true
const matomoHost = import.meta.env.VITE_MATOMO_HOST
const matomoSiteId = parseInt(import.meta.env.VITE_MATOMO_SITE_ID)

if (matomoEnabled && matomoHost && matomoSiteId) {
  window._paq = window._paq || []
  window._paq.push(['setTrackerUrl', `${matomoHost.endsWith('/') ? matomoHost : matomoHost + '/'}matomo.php`])
  window._paq.push(['setSiteId', matomoSiteId])
  window._paq.push(['disableCookies'])
  window._paq.push(['trackPageView'])
  window._paq.push(['enableLinkTracking'])

  const script = document.createElement('script')
  script.async = true
  script.src = `${matomoHost.endsWith('/') ? matomoHost : matomoHost + '/'}matomo.js`
  script.onerror = () => console.error('[Matomo] Erreur fatale lors du chargement du script')
  script.onload = () => console.log('[Matomo] Script chargé et actif')
  document.head.appendChild(script)

  // Link to router for page tracking
  router.afterEach((to) => {
    window._paq.push(['setCustomUrl', window.location.origin + to.fullPath])
    window._paq.push(['setDocumentTitle', to.meta.title || document.title])
    window._paq.push(['trackPageView'])
  })
  
  console.log('[Matomo] Initialisation manuelle lancée', { host: matomoHost, siteId: matomoSiteId })
} else if (matomoEnabled) {
  console.warn('[Matomo] Activé mais configuration incomplète', { matomoHost, matomoSiteId })
}

if (import.meta.env.VITE_CRISP_ENABLED === 'true' && import.meta.env.VITE_CRISP_WEBSITE_ID) {
  window.$crisp = []
  window.CRISP_WEBSITE_ID = import.meta.env.VITE_CRISP_WEBSITE_ID
  const script = document.createElement('script')
  script.src = 'https://client.crisp.chat/l.js'
  script.async = true
  document.getElementsByTagName('head')[0].appendChild(script)
}

app.mount('#app')
