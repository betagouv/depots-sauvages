<template>
  <div>
    <DsfrHeader
      service-title="Stop Dépôt Sauvage - Protect'Envi"
      service-description="Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
      :logoText="logoText"
      :quick-links="quickLinks"
    >
      <template #before-quick-links>
        <div class="fr-header__tools-item assistant-header-item">
          <button
            type="button"
            class="assistant-pill-btn"
            @click="openAssistant"
            title="Ouvrir l'Assistant IA"
            aria-label="Assistant IA"
          >
            <div class="assistant-pill-icon-glow">
              <svg class="assistant-pill-icon-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L13.8 8.2L20 10L13.8 11.8L12 18L10.2 11.8L4 10L10.2 8.2L12 2Z" fill="white" />
                <path d="M19 16L20 19L23 20L20 21L19 24L18 21L15 20L18 19L19 16Z" fill="white" opacity="0.8" />
              </svg>
            </div>
            <span class="assistant-pill-label">Assistant IA</span>
          </button>
        </div>
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

    <!-- Volet latéral Assistant IA -->
    <AssistantDrawer :is-open="isAssistantOpen" @close="isAssistantOpen = false" />
  </div>
</template>

<script setup lang="ts">
import { DsfrFooter, DsfrFooterLinkList, DsfrHeader, DsfrToggleSwitch } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AssistantDrawer from '../components/AssistantDrawer.vue'
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
const isAssistantOpen = ref(false)

const openAssistant = () => {
  isAssistantOpen.value = true
  // En mobile, si le menu modal DSFR est ouvert, on déclenche le clic sur le bouton de fermeture
  const closeMenuBtn = document.getElementById('close-button')
  if (closeMenuBtn) {
    closeMenuBtn.click()
  }
}
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
    bypassEnabled = bypassConfig?.enabled ?? false
  } catch {
    bypassEnabled = false
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

.assistant-header-item {
  display: flex;
  align-items: center;
  margin-right: 1.25rem;
}

/* Style Pill Premium inspiré du bouton Agent moderne */
.assistant-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #1b1e36 0%, #0d1226 100%);
  color: #ffffff;
  border: 1px solid rgba(100, 115, 255, 0.3);
  padding: 0.35rem 0.85rem 0.35rem 0.45rem;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(10, 15, 60, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.2);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none;
}

.assistant-pill-btn:hover {
  background: linear-gradient(135deg, #24294a 0%, #151b38 100%);
  border-color: rgba(140, 155, 255, 0.6);
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 6px 20px rgba(45, 60, 180, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.3);
}

.assistant-pill-btn:active {
  transform: translateY(0) scale(0.98);
}

.assistant-pill-icon-glow {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2b7fff 0%, #9834ff 50%, #f43f5e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 10px rgba(152, 52, 255, 0.5);
  flex-shrink: 0;
}

.assistant-pill-icon-svg {
  width: 16px;
  height: 16px;
}

.assistant-pill-label {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.2px;
  color: #ffffff;
}

.assistant-pill-badge {
  font-size: 0.62rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  background: rgba(255, 255, 255, 0.15);
  color: #c9d5ff;
  padding: 0.1rem 0.4rem;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@media (max-width: 767px) {
  .assistant-header-item {
    margin-right: 0;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-default-grey);
    width: 100%;
    justify-content: space-between;
  }
  .assistant-pill-btn {
    width: 100%;
    justify-content: center;
    padding: 0.5rem 1rem;
  }
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
