<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Déclaration d’accessibilité</h1>
        <p class="fr-text fr-text--lead fr-mb-0">Établie le 24 juin 2026.</p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <p>
            CESAN - Gendarmerie Nationale (Ministère de l'intérieur) s’engage à rendre son service
            accessible, conformément à l’article 47 de la loi n° 2005-102 du 11 février 2005.
          </p>
          <p>
            Cette déclaration d’accessibilité s’applique à Portect'Envi (<a
              href="https://protect-envi.beta.gouv.fr/"
              >Protect’Envi - Accompagner les collectivités pour mieux lutter contre les dépôts
              sauvages</a
            >).
          </p>

          <hr class="fr-my-4w" />

          <h2>État de conformité</h2>
          <p>
            <strong>Portect'Envi</strong> est <strong>non conforme</strong> avec le RGAA. Le site
            n’a encore pas été audité.
          </p>

          <hr class="fr-my-4w" />

          <h2>Amélioration et contact</h2>
          <p>
            Si vous n’arrivez pas à accéder à un contenu ou à un service, vous pouvez contacter le
            responsable de Portect'Envi pour être orienté vers une alternative accessible ou obtenir
            le contenu sous une autre forme.
          </p>
          <p class="fr-mb-1w">
            <strong>E-mail : </strong>
            <a class="fr-link" :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
          </p>
          <p class="fr-mb-1w">
            <strong>Formulaire de contact : </strong>
            <router-link class="fr-link" to="/contact">Cliquer ici pour nous contacter</router-link>
          </p>
          <p class="fr-mt-2w">Nous essayons de répondre dans les 2 jours ouvrés.</p>

          <hr class="fr-my-4w" />

          <h2>Voie de recours</h2>
          <p>
            Cette procédure est à utiliser dans le cas suivant : vous avez signalé au responsable du
            site internet un défaut d’accessibilité qui vous empêche d’accéder à un contenu ou à un
            des services du portail et vous n’avez pas obtenu de réponse satisfaisante.
          </p>
          <p>Vous pouvez :</p>
          <ul class="fr-pl-3w">
            <li class="fr-mb-1w">
              <a
                class="fr-link"
                href="https://formulaire.defenseurdesdroits.fr/"
                target="_blank"
                rel="noopener"
                >Écrire un message au Défenseur des droits</a
              >
            </li>
            <li class="fr-mb-1w">
              <a
                class="fr-link"
                href="https://www.defenseurdesdroits.fr/carte-des-delegues"
                target="_blank"
                rel="noopener"
                >Contacter le délégué du Défenseur des droits dans votre région</a
              >
            </li>
            <li>
              Envoyer un courrier par la poste (gratuit, ne pas mettre de timbre) :<br />
              Défenseur des droits<br />
              Libre réponse 71120 75342 Paris CEDEX 07
            </li>
          </ul>

          <hr class="fr-my-4w" />

          <p class="fr-text--xs fr-mt-4w">
            Cette déclaration d’accessibilité a été créé le 24 juin 2026 grâce au Générateur de
            Déclaration d’Accessibilité.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const contactEmail = import.meta.env.VITE_CONTACT_EMAIL
</script>
