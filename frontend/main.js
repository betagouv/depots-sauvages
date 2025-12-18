import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/dsfr.module.min.js'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import VueMatomo from 'vue-matomo'
import { createRouter, createWebHistory } from 'vue-router'
import App from './app.vue'

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
      path: '/debuter-procedure',
      name: 'Introduction',
      component: () => import('./pages/introduction-formulaire.vue'),
    },
    {
      path: '/debuter-procedure/formulaire',
      name: 'Formulaire',
      component: () => import('./pages/debuter-procedure.vue'),
    },
    {
      path: '/contact',
      name: 'Contact',
      component: () => import('./pages/contact.vue'),
    },
    {
      path: '/joindre',
      name: 'Joindre',
      component: () => import('./pages/joindre.vue'),
      meta: { hideNavigation: true },
    },
    {
      path: '/signalements-dn/:dossier_id',
      name: 'SignalementsDN',
      component: () => import('./pages/signalements-dn.vue'),
      meta: { hideNavigation: true },
    },
    {
      path: '/rejoindre-le-dispositif',
      name: 'RejoindreDispositif',
      component: () => import('./pages/rejoindre-le-dispositif.vue'),
      meta: { hideNavigation: true },
    },
    {
      path: '/demarche-numerique-rejoindre-protectenvi',
      name: 'DemarcheNumeriqueRejoindreProtectEnvi',
      component: () => import('./pages/demarche-numerique-rejoindre-protectenvi.vue'),
      meta: { hideNavigation: true },
    },
  ],
})

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(VueDsfr)

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
