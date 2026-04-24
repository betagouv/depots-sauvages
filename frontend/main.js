import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/dsfr.module.min.js'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import './styles/premium-design.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import {
  RiAlertLine,
  RiCalendarLine,
  RiChat1Line,
  RiCheckLine,
  RiDownloadLine,
  RiEditLine,
  RiExternalLinkLine,
  RiFileEditLine,
  RiFileList3Line,
  RiFileListLine,
  RiFolderLine,
  RiLoginBoxLine,
  RiLogoutBoxRLine,
  RiMailLine,
  RiMailSendLine,
  RiMapPin2Line,
  RiMoneyEuroCircleLine,
  RiPenNibLine,
  RiRefreshLine,
  RiSearchEyeLine,
  RiTimeLine,
  RiAccountCircleLine,
} from 'oh-vue-icons/icons/ri'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import VueMatomo from 'vue-matomo'
import { createRouter, createWebHistory } from 'vue-router'
import App from './app.vue'
import { getUserInfo } from './services/api'

addIcons(
  RiAlertLine,
  RiCalendarLine,
  RiChat1Line,
  RiCheckLine,
  RiDownloadLine,
  RiEditLine,
  RiExternalLinkLine,
  RiFileEditLine,
  RiFileList3Line,
  RiFileListLine,
  RiFolderLine,
  RiLoginBoxLine,
  RiLogoutBoxRLine,
  RiMailLine,
  RiMailSendLine,
  RiMapPin2Line,
  RiMoneyEuroCircleLine,
  RiPenNibLine,
  RiRefreshLine,
  RiSearchEyeLine,
  RiTimeLine,
  RiAccountCircleLine
)

const pinia = createPinia()

const router = createRouter({
  history: createWebHistory(),
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
app.component('VIcon', OhVueIcon)

if (import.meta.env.VITE_MATOMO_ENABLED === 'true') {
  app.use(VueMatomo, {
    host: import.meta.env.VITE_MATOMO_HOST,
    siteId: parseInt(import.meta.env.VITE_MATOMO_SITE_ID),
    router: router,
    disableCookies: true,
    requireConsent: false,
    trackInitialView: true, // trigger the first pageview
    trackInitialViewOnce: true, // avoid double counting on hot-reload
  })
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
