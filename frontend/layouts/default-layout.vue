<template>
  <div>
    <DsfrHeader
      service-title="Protect’Envi"
      service-description="Accompagner les collectivités pour mieux lutter contre les dépôts sauvages."
      :logoText="logoText"
      :quick-links="quickLinks"
    />

    <nav
      v-if="!route.meta.hideNavigation"
      class="fr-container"
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

onMounted(async () => {
  try {
    const userInfo = await getUserInfo()
    if (userInfo.is_authenticated) {
      isAuthenticated.value = true
      quickLinks.value.push({
        label: 'Se déconnecter',
        button: true,
        icon: 'ri-logout-box-r-line',
        iconRight: false,
        onClick: () => {
          window.location.href = LOGOUT_URL
        },
      })
    } else if (userInfo.proconnect_enabled) {
      quickLinks.value.push({
        label: 'Se connecter via ProConnect',
        button: true,
        icon: 'ri-login-box-line',
        iconRight: false,
        onClick: () => {
          window.location.href = LOGIN_URL
        },
      })
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  }
})

const footerLinks: FooterLink[] = [
  { text: 'legifrance.gouv.fr', href: 'https://legifrance.gouv.fr' },
  { text: 'gouvernement.fr', href: 'https://gouvernement.fr' },
  { text: 'service-public.fr', href: 'https://service-public.fr' },
  { text: 'data.gouv.fr', href: 'https://data.gouv.fr' },
]
</script>
