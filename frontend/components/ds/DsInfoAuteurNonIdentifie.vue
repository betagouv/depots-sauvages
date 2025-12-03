<template>
  <div class="fr-container fr-mt-4w">
    <section class="fr-p-4w fr-bg--g100 fr-mb-4w">
      <h2 class="fr-h3 fr-mb-2w">Télécharger et compléter les documents</h2>
      <p>
        Vous trouverez ci-dessous des pièces de procédure
        <span class="fr-text--bold">pré-remplies</span>, à compléter avec les éléments manquants
        (charte graphique de la mairie, date et signature du rédacteur du document, etc.).
      </p>

      <h3 class="fr-h4 fr-mt-3w fr-mb-2w">Rapport de constatation</h3>
      <p>Résumé des observations de terrain et des préjudices causés</p>
      <p>
        <span aria-hidden="true">📄</span> à conserver en mairie ou à transmettre lors d'un dépôt de
        plainte
      </p>

      <p v-if="modifyUrl" class="fr-mt-3w">
        Si vous avez besoin de modifier les informations merci de
        <a
          :href="modifyUrl"
          class="fr-link fr-icon-external-link-line fr-link--icon-right"
          target="_blank"
          rel="nopener"
        >
          modifier votre dossier sur votre démarche numérique
        </a>
      </p>
    </section>

    <section class="fr-p-4w fr-bg--g100 fr-mb-4w">
      <h2 class="fr-h3 fr-mb-2w"><span aria-hidden="true">📌</span> Ce qu'il vous reste à faire</h2>

      <h3 class="fr-h4 fr-mb-2w">Avant d'entamer la procédure</h3>
      <p>
        Pour lancer officiellement une procédure à l'encontre de l'auteur présumé de ce dépôt
        sauvage :
      </p>
      <ul class="fr-mb-3w">
        <li><span aria-hidden="true">📥</span> Téléchargez le rapport de constatation</li>
        <li>
          <span aria-hidden="true">✍️</span> Relisez, complétez et signez ce document (ou faites-le
          signer par votre autorité compétente : maire ou personne habilitée à réaliser des
          constatations).
        </li>
      </ul>

      <div class="fr-alert fr-alert--info fr-alert--sm fr-mt-3w" role="status">
        <h4 class="fr-alert__title">Procédure judiciaire</h4>
        <ul class="fr-mb-0">
          <li>
            <span aria-hidden="true">📝</span> Envoyez le rapport de constatation à la brigade ;
          </li>
          <li>
            <span aria-hidden="true">🧾</span> Prenez rendez-vous
            <a
              href="https://www.masecurite.interieur.gouv.fr/fr/trouver-un-commissariat-une-gendarmerie"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
              target="_blank"
              rel="noreferrer noopener"
            >
              auprès de la brigade de gendarmerie ou du commissariat
            </a>
            pour déposer plainte.
          </li>
        </ul>
      </div>

      <div class="fr-alert fr-alert--info fr-alert--sm fr-mt-3w" role="status">
        <h4 class="fr-alert__title">Procédure administrative</h4>
        <p class="fr-mb-2w">
          Sans auteur identifié, la procédure administrative ne peut pas être initiée.
        </p>
        <p class="fr-mb-2w">
          Si la procédure judiciaire ou de nouveaux éléments permettent d'identifier un auteur vous
          pourrez alors initier une procédure administrative.
        </p>
        <p v-if="modifyUrl" class="fr-mb-0">
          Vous pourrez alors
          <a
            :href="modifyUrl"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
            rel="nopener"
          >
            modifier les informations sur votre démarche numérique
          </a>
          pour mettre à jour vos documents.
        </p>
      </div>
    </section>

    <section class="fr-p-4w fr-bg--g100">
      <h3 class="fr-h3 fr-mb-2w">Ressources utiles</h3>
      <p class="fr-mt-3w">
        <span aria-hidden="true">👉</span> Pour un accompagnement pas à pas, consultez le
        <a
          href="https://acdechets.smartidf.services/aide-verbalisation"
          class="fr-link fr-icon-external-link-line fr-link--icon-right"
          target="_blank"
          rel="nopener"
        >
          guide ACDéchets de la Région Île-de-France
        </a>
      </p>
      <p>
        <span aria-hidden="true">👉</span> Retrouvez des conseils pratiques sur l'application à
        destination des élus, Gend'élus, accessible à tout le monde :
      </p>
      <ul>
        <li>
          <a
            href="https://play.google.com/store/apps/details?id=com.gendelus&hl=fr&pli=1"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
            rel="noreferrer noopener"
          >
            Télécharger sur le Play Store
          </a>
        </li>
        <li>
          <a
            href="https://apps.apple.com/fr/app/gend%C3%A9lus/id6444316373"
            class="fr-link fr-icon-external-link-line fr-link--icon-right"
            target="_blank"
            rel="noreferrer noopener"
          >
            Télécharger sur l'App Store
          </a>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modifyUrl?: string | null
}>()
</script>
