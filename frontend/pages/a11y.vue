<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Déclaration d'accessibilité</h1>
        <p class="fr-text fr-text--lead fr-mb-0">Engagement de conformité RGAA de Protect’Envi.</p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <p>
            Le Commandement pour l’environnement et la santé (CESAN) de la Gendarmerie nationale
            s’engage à rendre ses sites internet, applications mobiles et progiciels accessibles
            conformément à l’article 47 de la loi n° 2005-102 du 11 février 2005.
          </p>
          <p>
            À cette fin, il met en œuvre la stratégie et les actions suivantes : la conception de
            l'application selon les critères du RGAA, l'utilisation de la bibliothèque de composants
            officielle de l'État (DSFR) et l'amélioration continue de l'ergonomie.
          </p>

          <DsfrAlert type="info" title="Statut de conformité : non conforme" class="fr-mb-4w">
            L'application Protect’Envi est non conforme avec le référentiel général d’amélioration
            de l’accessibilité (RGAA), en l'absence d'audit formel réalisé à ce jour. Des travaux de
            correction et d'optimisation sont continuellement menés pour accroître l'accessibilité
            globale du service.
          </DsfrAlert>

          <hr class="fr-my-4w" />

          <h2>Retour d’information et contact</h2>
          <DsfrHighlight class="fr-ml-0 fr-mb-3w">
            Si vous n’avez pas accès à un contenu ou à un service, vous pouvez contacter le
            responsable de Protect’Envi pour être orienté vers une alternative accessible ou obtenir
            le contenu sous une autre forme :
            <br />
            <strong>E-mail : </strong>
            <a class="fr-link" :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
          </DsfrHighlight>

          <hr class="fr-my-4w" />

          <h2>Voies de recours</h2>
          <p>
            Cette procédure est à utiliser dans le cas suivant : vous avez signalé au responsable du
            site internet un défaut d’accessibilité qui vous empêche d’accéder à un contenu ou à un
            des services du portail et vous n’avez pas obtenu de réponse satisfaisante.
          </p>
          <p>Vous pouvez :</p>
          <ul class="fr-pl-3w">
            <li>
              Écrire un message au
              <a class="fr-link" href="https://formulaire.defenseurdesdroits.fr/" target="_blank" rel="noopener"
                >Défenseur des droits</a
              >
            </li>
            <li>Contacter le délégué du Défenseur des droits dans votre région</li>
            <li>
              Envoyer un courrier postal (gratuit, sans affranchissement) à l'adresse : Défenseur
              des droits, Libre réponse 71120, 75342 Paris CEDEX 07
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert, DsfrHighlight } from '@gouvminint/vue-dsfr'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL
</script>
