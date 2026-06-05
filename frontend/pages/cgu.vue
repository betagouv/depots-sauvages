<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Conditions générales d’utilisation</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Modalités et règles d'utilisation de la plateforme Protect’Envi.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <p>
            Les présentes conditions générales d'utilisation (ci-après désignées « CGU ») définissent
            le cadre juridique de l'utilisation de la plateforme <strong>Protect’Envi</strong> par les utilisateurs.
          </p>

          <h2>1. Présentation du service</h2>
          <p>
            Protect’Envi est un service public numérique développé par le <strong>Commandement pour l’environnement et la santé (CESAN)</strong>
            de la Gendarmerie nationale.
          </p>
          <p>
            La plateforme a pour objectif d'accompagner les collectivités territoriales dans la lutte contre les dépôts sauvages
            de déchets, en facilitant la constatation des infractions, la constitution de dossiers de procédure administrative
            ou pénale, et le suivi des actions engagées.
          </p>

          <h2>2. Accès et inscription</h2>
          <p>
            L'utilisation de la plateforme est réservée aux personnes physiques habilitées agissant dans le cadre de leurs fonctions officielles :
          </p>
          <ul class="fr-pl-3w fr-mb-3w">
            <li>Les maires, élus locaux et agents des collectivités territoriales dûment habilités.</li>
            <li>Les personnels de la Gendarmerie nationale et de la Police nationale en charge de la police de l'environnement.</li>
            <li>Les agents assermentés des parcs nationaux, réserves naturelles ou autres administrations compétentes en matière de police des déchets.</li>
          </ul>
          <p>
            L'accès s'effectue via un système d'authentification sécurisé (notamment ProConnect). L'utilisateur s'engage à conserver la confidentialité de ses accès et à signaler immédiatement toute utilisation frauduleuse de son compte.
          </p>

          <h2>3. Responsabilité de l'utilisateur</h2>
          <p>
            L'utilisateur est seul responsable des informations, contenus et documents qu'il saisit ou téléverse sur la plateforme (notamment la localisation des dépôts, les photographies, la description des faits).
          </p>
          <p>
            L'utilisateur s'engage à :
          </p>
          <DsfrHighlight class="fr-ml-0 fr-mb-4w">
            <ul class="fr-pl-2w fr-mb-0">
              <li>
                Fournir des informations exactes et fidèles à la réalité des faits constatés.
              </li>
              <li>
                Ne pas renseigner de données inappropriées ou hors de propos, notamment des commentaires injurieux ou diffamatoires.
              </li>
              <li>
                Veiller à respecter la vie privée des tiers (notamment en évitant, dans la mesure du possible, de photographier de manière lisible des visages de personnes tierces non concernées par l'infraction dans les pièces justificatives).
              </li>
            </ul>
          </DsfrHighlight>

          <h2>4. Responsabilité de l'éditeur</h2>
          <p>
            Protect’Envi met tout en œuvre pour assurer la disponibilité du service. Toutefois, le service étant en constante évolution (mode "bêta"), l'éditeur ne peut garantir une accessibilité ininterrompue ou une absence totale d'anomalies.
          </p>
          <p>
            L'éditeur ne saurait être tenu responsable :
          </p>
          <ul class="fr-pl-3w fr-mb-3w">
            <li>Des interruptions temporaires du service pour maintenance ou mise à jour.</li>
            <li>De la perte éventuelle de données saisies (il est recommandé aux utilisateurs de conserver une copie des procès-verbaux et rapports générés).</li>
            <li>De l'issue des procédures administratives ou judiciaires engagées à la suite de l'utilisation de la plateforme. Protect’Envi fournit un outil d'accompagnement juridique et technique, mais la responsabilité finale des actes de poursuite ou de sanction incombe exclusivement aux autorités compétentes.</li>
          </ul>

          <h2>5. Propriété intellectuelle</h2>
          <p>
            Les contenus de la plateforme sont protégés par le droit d'auteur. Sauf mention contraire, les textes et éléments graphiques produits par Protect’Envi sont mis à disposition sous licence ouverte <a href="https://github.com/etalab/licence-ouverte/blob/master/LO.md" target="_blank" rel="noopener">licence etalab-2.0</a>.
          </p>

          <h2>6. Modification des conditions</h2>
          <p>
            L'éditeur se réserve le droit de modifier les présentes CGU à tout moment pour les adapter aux évolutions du service ou de la réglementation. Les utilisateurs en seront informés par tout moyen utile.
          </p>

          <DsfrAlert type="info" title="Nous contacter" class="fr-mb-4w">
            Pour toute question concernant ces CGU, vous pouvez nous écrire à l'adresse e-mail suivante :
            <br />
            <a class="fr-link" :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
          </DsfrAlert>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrAlert, DsfrHighlight } from '@gouvminint/vue-dsfr'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL
</script>
