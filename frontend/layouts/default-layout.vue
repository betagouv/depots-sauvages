<template>
  <div>
    <DsfrHeader
      service-title="Protect’Envi"
      service-description="Agir contre les dépôts sauvages"
      :logoText="logoText"
    />
    <div class="fr-container fr-py-3w" role="main" id="content">
      <DsfrNotice>
        <a
          href="https://docs.google.com/forms/d/e/1FAIpQLSe73qnFQje6_hdhKv1VeyZVQOIeRzn0Q7ahRI4hlBjq8atG8Q/viewform"
          rel="noopener noreferrer"
          target="_blank"
        >
          Partagez-vous votre avis !
        </a>
        Cette version démo est en test et disponible jusqu'au 7 mai. Vos retours sont précieux pour
        faire évoluer l'outil.
      </DsfrNotice>
      <slot />
    </div>
    <DsfrFooter
      :logo-text="logoText"
    >
      <template #description>
        Le site de la mission logiciels libres et communs numériques est une publication de la
        <a href="https://www.numerique.gouv.fr/" target="_blank">direction interministérielle du numérique</a>.
        Le
        <a href="https://github.com/betagouv/depots-sauvages"
           title="code source - Nouvelle fenêtre"
           target="_blank"
           rel="noreferrer noopener"
        >
          code source de ce site
        </a>
        est publié sous licence libre.
      </template>
      <template #bottom-link>
        <DsfrFooterLinkList :links="footerLinks"/>
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
import { DsfrFooter, DsfrFooterLinkList, DsfrHeader, DsfrNotice } from '@gouvminint/vue-dsfr'

interface FooterLink {
  text: string
  href: string
}

interface BreadcrumbLink {
  text: string
  to: string
}

const logoText = ["Ministère","de l’intérieur"];
const breadcrumbLinks: BreadcrumbLink[] = []

const footerLinks: FooterLink[] = [
  { text: 'legifrance.gouv.fr', href: 'https://legifrance.gouv.fr' },
  { text: 'gouvernement.fr', href: 'https://gouvernement.fr' },
  { text: 'service-public.fr', href: 'https://service-public.fr' },
  { text: 'data.gouv.fr', href: 'https://data.gouv.fr' },
]
</script>
