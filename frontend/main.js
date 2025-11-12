import '@gouvfr/dsfr/dist/dsfr.min.css'
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
      path: '/accompagnement',
      name: 'Accompagnement',
      component: () => import('./pages/accompagnement.vue'),
    },
    {
      path: '/joindre',
      name: 'Joindre',
      component: () => import('./pages/joindre.vue'),
      meta: { hideNavigation: true, hideFeedback: true },
    },
    {
      path: '/rejoindre-le-dispositif',
      name: 'RejoindreDispositif',
      component: () => import('./pages/rejoindre-le-dispositif.vue'),
      meta: { hideNavigation: true, hideFeedback: true },
    },
    {
      path: '/demarches-simplifiees-rejoindre-protectenvi',
      name: 'DemarchesSimplifieesRejoindreProtectEnvi',
      component: () => import('./pages/demarches-simplifiees-rejoindre-protectenvi.vue'),
      meta: { hideNavigation: true, hideFeedback: true },
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

app.mount('#app')
