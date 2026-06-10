<template>
  <div>
    <DsfrHeader
      service-title="Protect’Envi"
      service-description="Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
      :logoText="logoText"
      :quick-links="quickLinks"
    >
      <template #before-quick-links>
        <div class="fr-header__tools-item admin-toggle-header-item">
          <DsfrToggleSwitch
            label="Mode édition"
            v-model="editModeStore.isAdminMode"
            :label-left="true"
            :no-text="true"
            input-id="admin-mode-toggle-header"
          />
        </div>
      </template>

      <template #mainnav="{ hidemodal }">
        <nav
          v-if="!route.meta.hideNavigation"
          class="fr-nav"
          role="navigation"
          aria-label="Menu principal"
        >
          <ul class="fr-nav__list">
            <router-link
              v-for="lien in navLinks"
              :key="lien.href"
              :to="lien.href"
              custom
              v-slot="{ href, navigate, isActive }"
            >
              <li class="fr-nav__item">
                <a
                  class="fr-nav__link"
                  :class="{
                    'fr-nav__link--active': isActive || route.meta.activeMenu === lien.href,
                  }"
                  :aria-current="
                    isActive || route.meta.activeMenu === lien.href ? 'page' : undefined
                  "
                  :href="href"
                  @click="navigate(); hidemodal()"
                >
                  {{ lien.text }}
                </a>
              </li>
            </router-link>
          </ul>
        </nav>
      </template>
    </DsfrHeader>

    <main role="main" id="content">
      <slot />
    </main>
    <DsfrFooter
      :logo-text="logoText"
      :after-mandatory-links="afterMandatoryLinks"
    >
      <template #description>
        <strong>Protect’Envi</strong>
        <br />
        Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.
      </template>
      <template #bottom-link>
        <DsfrFooterLinkList :links="footerLinks" />
      </template>
      <template #content>
        <p>
          Sauf mention contraire, tous les contenus de ce site sont sous
          <a
            href="https://github.com/etalab/licence-ouverte/blob/master/LO.md"
            target="_blank"
            rel="noopener"
          >
            licence etalab-2.0
          </a>
        </p>
      </template>
    </DsfrFooter>
  </div>
</template>

<script setup lang="ts">
import { DsfrFooter, DsfrFooterLinkList, DsfrHeader, DsfrToggleSwitch } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useEditModeStore } from '../stores/editMode'
import { getUserInfo, getBypassAuthConfig } from '../services/api'
import { LOGIN_URL, LOGOUT_URL } from '../services/urls'
import { PROCONNECT_ENABLED } from '../services/config'

interface FooterLink {
  text: string
  href: string
}

interface BreadcrumbLink {
  text: string
  to: string
}

const route = useRoute()
const editModeStore = useEditModeStore()
const logoText = ['Ministère', 'de l’intérieur']
const breadcrumbLinks: BreadcrumbLink[] = []

interface NavLink {
  text: string
  href: string
}

const navLinks = computed<NavLink[]>(() => {
  return [
    { text: 'Accueil', href: '/' },
    { text: 'Comprendre la procédure', href: '/comprendre-la-procedure' },
    { text: 'Mes procédures', href: '/mes-procedures' },
    { text: 'Contact', href: '/contact' },
  ]
})

interface QuickLink {
  label: string
  href?: string
  to?: string
  icon?: string
  iconRight?: boolean
  button?: boolean
  onClick?: (event: MouseEvent) => void
}

const quickLinks = ref<QuickLink[]>([])

const isAuthenticated = ref(false)
const userInfo = ref<any>(null)

const goToLogin = (event?: MouseEvent) => {
  if (event) {
    event.preventDefault()
  }
  window.location.href = LOGIN_URL
}

const goToLogout = (event?: MouseEvent) => {
  if (event) {
    event.preventDefault()
  }
  window.location.href = LOGOUT_URL
}

const isProConnectEnabled = PROCONNECT_ENABLED

onMounted(async () => {
  let bypassEnabled = false
  try {
    const bypassConfig = await getBypassAuthConfig()
    bypassEnabled = bypassConfig.enabled
  } catch (e) {
    console.warn('Failed to fetch bypass auth config', e)
  }

  try {
    const info = await getUserInfo()
    userInfo.value = info

    if (info.is_authenticated) {
      isAuthenticated.value = true
      quickLinks.value.push({
        label: 'Se déconnecter',
        icon: 'fr-icon-logout-box-r-line',
        iconRight: false,
        href: LOGOUT_URL,
        to: LOGOUT_URL, // for styling
        onClick: goToLogout,
      })
    } else {
      if (bypassEnabled) {
        quickLinks.value.push({
          label: 'Connexion de démo',
          icon: 'fr-icon-user-line',
          iconRight: false,
          href: '/login-demo',
          to: '/login-demo',
          onClick: (event) => {
            if (event) event.preventDefault()
            window.location.href = '/login-demo'
          }
        })
      }
      if (isProConnectEnabled) {
        quickLinks.value.push({
          label: 'Se connecter via ProConnect',
          icon: 'fr-icon-lock-line',
          iconRight: false,
          href: LOGIN_URL,
          to: LOGIN_URL, // for styling
          onClick: goToLogin,
        })
      }
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)

    if (bypassEnabled) {
      quickLinks.value.push({
        label: 'Connexion de démo',
        icon: 'fr-icon-user-line',
        iconRight: false,
        href: '/login-demo',
        to: '/login-demo',
        onClick: (event) => {
          if (event) event.preventDefault()
          window.location.href = '/login-demo'
        }
      })
    }
    if (isProConnectEnabled) {
      quickLinks.value.push({
        label: 'Se connecter via ProConnect',
        icon: 'fr-icon-lock-line',
        iconRight: false,
        href: LOGIN_URL,
        to: LOGIN_URL, // for styling
        onClick: goToLogin,
      })
    }
  }
})

const footerLinks: FooterLink[] = [
  { text: 'legifrance.gouv.fr', href: 'https://legifrance.gouv.fr' },
  { text: 'gouvernement.fr', href: 'https://gouvernement.fr' },
  { text: 'service-public.fr', href: 'https://service-public.fr' },
  { text: 'data.gouv.fr', href: 'https://data.gouv.fr' },
]

const afterMandatoryLinks = [
  { label: 'Conditions générales d’utilisation', to: '/cgu' },
  { label: 'Plan du site', to: '/plan-du-site' },
  { label: 'Foire aux questions', to: '/faq' }
]
</script>

<style>
/* 
  Custom styles for mobile login button positioning.
  We keep these because standard utility classes cannot handle this specific 
  absolute positioning relative to the header structure.
*/

.admin-toggle-header-item {
  display: flex;
  align-items: center;
  margin-right: 1.5rem;
  padding-right: 1.5rem;
  border-right: 1px solid var(--border-default-grey);
}

.admin-toggle-header-item .fr-toggle {
  padding: 0;
  margin: 0;
}

.admin-toggle-header-item .fr-toggle__label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-title-grey);
  white-space: nowrap;
}

@media (max-width: 767px) {
  .admin-toggle-header-item {
    margin-right: 0;
    padding-right: 0;
    border-right: none;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-default-grey);
    width: 100%;
    justify-content: space-between;
  }
}
</style>
