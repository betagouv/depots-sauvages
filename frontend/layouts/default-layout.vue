<template>
  <div>
    <DsfrHeader
      service-title="Protect’Envi"
      service-description="Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
      :logoText="logoText"
      :quick-links="quickLinks"
    >
      <template #operator>
        <div class="mobile-login-btn fr-hidden-lg">
          <button
            v-if="!isAuthenticated && isProConnectEnabled"
            class="fr-btn fr-btn--tertiary-no-outline fr-icon-account-circle-line fr-p-2v"
            title="Se connecter via ProConnect"
            @click="goToLogin"
          >
            Se connecter
          </button>
          <button
            v-if="isAuthenticated"
            class="fr-btn fr-btn--tertiary-no-outline fr-icon-logout-box-r-line fr-p-2v"
            title="Se déconnecter"
            @click="goToLogout"
          >
            Se déconnecter
          </button>
        </div>
      </template>
      <template #mainnav>
        <nav
          v-if="!route.meta.hideNavigation"
          class="fr-nav"
          role="navigation"
          aria-label="Menu principal"
        >
          <ul class="fr-nav__list">
            <li v-for="lien in navLinks" :key="lien.href" class="fr-nav__item">
              <a
                class="fr-nav__link"
                :class="{ 'fr-nav__link--active': route.path === lien.href }"
                :aria-current="route.path === lien.href ? 'page' : undefined"
                :href="lien.href"
              >
                {{ lien.text }}
              </a>
            </li>
          </ul>
        </nav>
      </template>
    </DsfrHeader>

    <main class="fr-container fr-py-3w" role="main" id="content">
      <slot />
    </main>
    <DsfrFooter :logo-text="logoText">
      <template #description>
        Le site de la mission logiciels libres et communs numériques est une publication de la
        <a href="https://www.numerique.gouv.fr/" target="_blank"
          >direction interministérielle du numérique</a
        >. Le
        <a
          href="https://github.com/betagouv/depots-sauvages"
          title="code source - Nouvelle fenêtre"
          target="_blank"
          rel="noreferrer noopener"
        >
          code source de ce site
        </a>
        est publié sous licence libre.
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
import { DsfrFooter, DsfrFooterLinkList, DsfrHeader } from '@gouvminint/vue-dsfr'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getUserInfo } from '../services/api'
import { LOGIN_URL, LOGOUT_URL } from '../services/urls'
interface FooterLink {
  text: string
  href: string
}

interface BreadcrumbLink {
  text: string
  to: string
}

const route = useRoute()
const logoText = ['Ministère', 'de l’intérieur']
const breadcrumbLinks: BreadcrumbLink[] = []

const navLinks = computed(() => {
  const links = [
    { text: 'Accueil', href: '/' },
    { text: 'Comprendre la procédure', href: '/comprendre-la-procedure' },
  ]
  if (isAuthenticated.value) {
    links.push({ text: 'Mes procédures', href: '/mes-dossiers' })
  }
  links.push({ text: 'Contact', href: '/contact' })
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

const isProConnectEnabled = import.meta.env.VITE_PROCONNECT_ENABLED === 'true'

onMounted(async () => {
  try {
    const info = await getUserInfo()
    userInfo.value = info

    if (info.is_authenticated) {
      isAuthenticated.value = true
      quickLinks.value.push({
        label: 'Se déconnecter',
        icon: 'ri-logout-box-r-line',
        iconRight: false,
        href: LOGOUT_URL,
        to: LOGOUT_URL, // for styling
        onClick: goToLogout,
      })
    } else if (isProConnectEnabled) {
      quickLinks.value.push({
        label: 'Se connecter via ProConnect',
        icon: 'ri-login-box-line',
        iconRight: false,
        href: LOGIN_URL,
        to: LOGIN_URL, // for styling
        onClick: goToLogin,
      })
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)

    if (isProConnectEnabled) {
      quickLinks.value.push({
        label: 'Se connecter via ProConnect',
        icon: 'ri-login-box-line',
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
</script>

<style>
/* 
  Custom styles for mobile login button positioning.
  We keep these because standard utility classes cannot handle this specific 
  absolute positioning relative to the header structure.
*/
@media (max-width: 991px) {
  .mobile-login-btn {
    display: flex;
    position: absolute;
    top: 0.25rem; /* Checked for alignment with menu button */
    right: 3.5rem; /* Left of the burger menu (approx) */
    z-index: 1000;
  }

  /* Font size 0 to hide text, but keep icon visible */
  .mobile-login-btn .fr-btn {
    min-height: auto;
    font-size: 0;
  }

  .mobile-login-btn .fr-btn::before {
    margin: 0;
    font-size: 1.5rem;
  }

  /* Fix for mobile menu button alignment and styling */
  .fr-header__navbar .fr-btn--menu {
    border: 1px solid var(--border-default-grey);
    margin-right: 0.25rem;
    align-self: center;
  }
}
</style>
