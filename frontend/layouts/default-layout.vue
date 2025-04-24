<template>
  <div class="layout-default">
    <DsfrHeader
      service-title="Protect Envi"
      service-description="Signalement des dépôts sauvages"
    />
    <div class="fr-container" role="main" id="content">
      <DsfrNotice>
        Votre avis compte
        <a
          href="#"
          rel="noopener noreferrer"
          target="_blank"
        >
          lien formulaire de feedback
        </a>
      </DsfrNotice>
      <slot />
    </div>
    <DsfrFooter>
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
interface FooterLink {
  text: string
  href: string
}

interface BreadcrumbLink {
  text: string
  to: string
}

const breadcrumbLinks: BreadcrumbLink[] = []

const footerLinks: FooterLink[] = [
  { text: 'legifrance.gouv.fr', href: 'https://legifrance.gouv.fr' },
  { text: 'gouvernement.fr', href: 'https://gouvernement.fr' },
  { text: 'service-public.fr', href: 'https://service-public.fr' },
  { text: 'data.gouv.fr', href: 'https://data.gouv.fr' },
]
</script>

<style scoped>
.layout-default {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.fr-container {
  padding: 2rem 1rem;
}

.layout-container {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .layout-container {
    padding: 2rem;
  }
}

@media (min-width: 1024px) {
  .layout-container {
    padding: 3rem;
  }
}
</style>
