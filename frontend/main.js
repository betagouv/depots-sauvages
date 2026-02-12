import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/dsfr.module.min.js'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import {
  RiCalendarLine,
  RiDownloadLine,
  RiEditLine,
  RiFileEditLine,
  RiFileListLine,
  RiFolderLine,
  RiLoginBoxLine,
  RiLogoutBoxRLine,
  RiMailSendLine,
  RiMoneyEuroCircleLine,
  RiPenNibLine,
  RiSearchEyeLine,
  RiTimeLine,
} from 'oh-vue-icons/icons/ri'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import VueMatomo from 'vue-matomo'
import { createRouter, createWebHistory } from 'vue-router'
import App from './app.vue'
import { getUserInfo } from './services/api'

addIcons(
  RiCalendarLine,
  RiDownloadLine,
  RiEditLine,
  RiFileEditLine,
  RiFileListLine,
  RiFolderLine,
  RiLoginBoxLine,
  RiLogoutBoxRLine,
  RiMailSendLine,
  RiMoneyEuroCircleLine,
  RiPenNibLine,
  RiSearchEyeLine,
  RiTimeLine
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
      path: '/mes-dossiers',
      name: 'MesDossiers',
      component: () => import('./pages/mes-dossiers.vue'),
      meta: { requiresAuth: true },
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
      name: 'SignalementsDN',
      component: () => import('./pages/signalements-dn.vue'),
      meta: { requiresAuth: true },
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
