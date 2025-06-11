import '@gouvfr/dsfr/dist/dsfr.min.css'
import '@gouvfr/dsfr/dist/utility/utility.min.css'
import VueDsfr from '@gouvminint/vue-dsfr'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
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
      path: '/debuter-procedure',
      name: 'Formulaire',
      component: () => import('./pages/debuter-procedure.vue'),
    } ,
    {
      path: '/accompagnement',
      name: 'Accompagnement',
      component: () => import('./pages/accompagnement.vue'),
    }
  ],
})

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(VueDsfr)
app.mount('#app')
