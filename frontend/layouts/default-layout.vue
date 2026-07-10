<template>
  <div>
    <DsfrHeader
      service-title="Protect’Envi"
      service-description="Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
      :logoText="logoText"
      :quick-links="quickLinks"
    >
      <template #before-quick-links>
        <div v-if="userInfo?.is_staff" class="fr-header__tools-item admin-toggle-header-item">
          <DsfrToggleSwitch
            label="Mode admin"
            v-model="adminModeStore.isAdminMode"
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
                  @click="(navigate(), hidemodal())"
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
    <DsfrFooter :logo-text="logoText" :after-mandatory-links="afterMandatoryLinks">
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
import { getBypassAuthConfig } from '../services/api'
import { PROCONNECT_ENABLED } from '../services/config'
import { LOGIN_URL, LOGOUT_URL } from '../services/urls'
import { useAdminModeStore } from '../stores/admin-mode'
import { useUserStore } from '../stores/user'

interface FooterLink {
  text: string
  href: string
}

interface BreadcrumbLink {
  text: string
  to: string
}

const route = useRoute()
const adminModeStore = useAdminModeStore()
const userStore = useUserStore()
const logoText = ['Ministère', 'de l’intérieur']
const breadcrumbLinks: BreadcrumbLink[] = []

interface NavLink {
  text: string
  href: string
}

const navLinks = computed<NavLink[]>(() => {
  const links = [
    { text: 'Accueil', href: '/' },
    { text: 'Comment agir', href: '/comment-agir' },
    { text: 'Mes procédures', href: '/mes-procedures' },
    { text: 'FAQ', href: '/faq' },
    { text: 'Contact', href: '/contact' },
  ]
  if (adminModeStore.isAdminMode && userStore.userInfo?.is_staff) {
    links.push({ text: 'Backoffice', href: '/backoffice' })
  }
  return links
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
const userInfo = computed(() => userStore.userInfo)

const goToLogin = (event?: MouseEvent) => {
  if (event) {
    event.preventDefault()
  }
  const nextParam = route.fullPath === '/' ? '/mes-procedures' : route.fullPath
  window.location.href = `${LOGIN_URL}?next=${encodeURIComponent(nextParam)}`
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
    const fetchedUserInfo = await userStore.fetchUserInfo()

    if (!fetchedUserInfo.is_staff) {
      adminModeStore.setAdminMode(false)
    }

    if (fetchedUserInfo.is_authenticated) {
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
        const demoUrl = `/login-demo?next=${encodeURIComponent(route.fullPath === '/' ? '/mes-procedures' : route.fullPath)}`
        quickLinks.value.push({
          label: 'Connexion de démo',
          icon: 'fr-icon-user-line',
          iconRight: false,
          href: demoUrl,
          to: demoUrl,
          onClick: (event) => {
            if (event) event.preventDefault()
            window.location.href = demoUrl
          },
        })
      }
      if (isProConnectEnabled) {
        const nextParam = route.fullPath === '/' ? '/mes-procedures' : route.fullPath
        const loginUrlWithNext = `${LOGIN_URL}?next=${encodeURIComponent(nextParam)}`
        quickLinks.value.push({
          label: 'Se connecter via ProConnect',
          icon: 'fr-icon-lock-line',
          iconRight: false,
          href: loginUrlWithNext,
          to: loginUrlWithNext, // for styling
          onClick: goToLogin,
        })
      }
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)
    adminModeStore.setAdminMode(false)

    if (bypassEnabled) {
      const demoUrl = `/login-demo?next=${encodeURIComponent(route.fullPath === '/' ? '/mes-procedures' : route.fullPath)}`
      quickLinks.value.push({
        label: 'Connexion de démo',
        icon: 'fr-icon-user-line',
        iconRight: false,
        href: demoUrl,
        to: demoUrl,
        onClick: (event) => {
          if (event) event.preventDefault()
          window.location.href = demoUrl
        },
      })
    }
    if (isProConnectEnabled) {
      const nextParam = route.fullPath === '/' ? '/mes-procedures' : route.fullPath
      const loginUrlWithNext = `${LOGIN_URL}?next=${encodeURIComponent(nextParam)}`
      quickLinks.value.push({
        label: 'Se connecter via ProConnect',
        icon: 'fr-icon-lock-line',
        iconRight: false,
        href: loginUrlWithNext,
        to: loginUrlWithNext, // for styling
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
  { label: 'Foire aux questions', to: '/faq' },
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

.admin-toggle-header-item .fr-toggle__label {
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
