<template>
  <div>
    <DsfrSkipLinks :links="skipLinks" />
    <DsfrHeader
      service-title="Stop Dépôt Sauvage - Protect'Envi"
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
          id="main-navigation"
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

    <main role="main" id="content" tabindex="-1">
      <div
        v-if="breadcrumbLinks.length"
        :class="{ 'fr-background-alt--blue-france': route.meta.breadcrumbBand }"
      >
        <div
          :class="route.meta.fullWidth ? 'fr-container--fluid fr-px-2w fr-px-md-4w' : 'fr-container'"
        >
          <DsfrBreadcrumb :links="breadcrumbLinks" class="fr-mt-0 fr-mb-0 fr-pt-2w" />
        </div>
      </div>
      <slot />
    </main>
    <DsfrFooter :logo-text="logoText" :after-mandatory-links="afterMandatoryLinks">
      <template #description>
        <strong>Stop Dépôt Sauvage - Protect'Envi</strong>
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
import {
  DsfrBreadcrumb,
  DsfrFooter,
  DsfrFooterLinkList,
  DsfrHeader,
  DsfrSkipLinks,
  DsfrToggleSwitch,
} from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBreadcrumb } from '../composables/useBreadcrumb'
import { getBypassAuthConfig } from '../services/api'
import { PROCONNECT_ENABLED } from '../services/config'
import { LOGIN_URL, LOGOUT_URL } from '../services/urls'
import { useAdminModeStore } from '../stores/admin-mode'
import { useUserStore } from '../stores/user'
import { buildBreadcrumbLinks } from '../utils/breadcrumb'

interface FooterLink {
  text: string
  href: string
}

const route = useRoute()
const router = useRouter()
const adminModeStore = useAdminModeStore()
const userStore = useUserStore()
const logoText = ['Ministère', 'de l’intérieur']
const { dynamicLabel, setCurrentPageLabel } = useBreadcrumb()
const breadcrumbLinks = computed(() => buildBreadcrumbLinks(route, router, dynamicLabel.value))
watch(
  () => route.path,
  () => setCurrentPageLabel(null),
)

interface NavLink {
  text: string
  href: string
}

const navLinks = computed<NavLink[]>(() => {
  const links = [
    { text: 'Accueil', href: '/' },
    { text: 'Comment agir', href: '/comment-agir' },
    { text: 'FAQ', href: '/faq' },
    { text: 'Articles', href: '/blog' },
    { text: 'Mes procédures', href: '/mes-procedures' },
    { text: 'Contact', href: '/contact' },
  ]
  if (adminModeStore.isAdminMode && userStore.userInfo?.is_staff) {
    links.push({ text: 'Backoffice', href: '/backoffice' })
  }
  return links
})

const skipLinks = computed(() => [
  { id: 'content', text: 'Contenu' },
  ...(route.meta.hideNavigation ? [] : [{ id: 'main-navigation', text: 'Menu' }]),
  { id: 'footer', text: 'Pied de page' },
])

interface QuickLink {
  label: string
  href?: string
  to?: string
  icon?: string
  iconRight?: boolean
  button?: boolean
  onClick?: (event: MouseEvent) => void
}

const isAuthenticated = ref(false)
const bypassEnabled = ref(false)
const userInfo = computed(() => userStore.userInfo)
const isProConnectEnabled = PROCONNECT_ENABLED

// Computed from the current route so the user comes back to the page they were on after login.
const loginNextPath = computed(() => (route.fullPath === '/' ? '/mes-procedures' : route.fullPath))

const redirectTo = (url: string) => (event?: MouseEvent) => {
  event?.preventDefault()
  window.location.href = url
}

const quickLinks = computed<QuickLink[]>(() => {
  if (isAuthenticated.value) {
    return [
      {
        label: 'Se déconnecter',
        icon: 'fr-icon-logout-box-r-line',
        iconRight: false,
        href: LOGOUT_URL,
        to: LOGOUT_URL, // for styling
        onClick: redirectTo(LOGOUT_URL),
      },
    ]
  }
  const next = encodeURIComponent(loginNextPath.value)
  const links: QuickLink[] = []
  if (bypassEnabled.value) {
    const demoUrl = `/login-demo?next=${next}`
    links.push({
      label: 'Connexion de démo',
      icon: 'fr-icon-user-line',
      iconRight: false,
      href: demoUrl,
      to: demoUrl,
      onClick: redirectTo(demoUrl),
    })
  }
  if (isProConnectEnabled) {
    const loginUrl = `${LOGIN_URL}?next=${next}`
    links.push({
      label: 'Se connecter via ProConnect',
      icon: 'fr-icon-lock-line',
      iconRight: false,
      href: loginUrl,
      to: loginUrl, // for styling
      onClick: redirectTo(loginUrl),
    })
  }
  return links
})

onMounted(async () => {
  try {
    const bypassConfig = await getBypassAuthConfig()
    bypassEnabled.value = bypassConfig?.enabled ?? false
  } catch {
    bypassEnabled.value = false
  }

  try {
    const fetchedUserInfo = await userStore.fetchUserInfo()
    if (!fetchedUserInfo.is_staff) {
      adminModeStore.setAdminMode(false)
    }
    isAuthenticated.value = fetchedUserInfo.is_authenticated
  } catch (error) {
    console.error('Failed to fetch user info:', error)
    adminModeStore.setAdminMode(false)
  }
})

const footerLinks: FooterLink[] = [
  { text: 'legifrance.gouv.fr', href: 'https://legifrance.gouv.fr' },
  { text: 'gouvernement.fr', href: 'https://gouvernement.fr' },
  { text: 'service-public.fr', href: 'https://service-public.fr' },
  { text: 'data.gouv.fr', href: 'https://data.gouv.fr' },
]

const afterMandatoryLinks = [
  { label: 'Blog & Retours d’expérience', to: '/blog' },
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
