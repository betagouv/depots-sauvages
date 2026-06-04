<template>
  <div>
    <div class="fr-background-alt--blue-france fr-mb-6w fr-py-6w">
      <div class="fr-container">
        <h1 class="fr-h1 fr-mb-3w">Données personnelles et confidentialité</h1>
        <p class="fr-text fr-text--lead fr-mb-0">
          Politique de protection des données et respect de votre vie privée.
        </p>
      </div>
    </div>

    <div class="fr-container fr-pb-8w">
      <div class="fr-grid-row">
        <div class="fr-col-12 fr-col-md-8">
          <p>
            Le service Protect’Envi est développé par le CESAN de la Gendarmerie nationale. Nous accordons une grande importance à la protection et à la confidentialité de vos données personnelles conformément au Règlement Général sur la Protection des Données (RGPD) et à la loi Informatique et Libertés.
          </p>

          <h2>Responsable de traitement</h2>
          <p>
            Le traitement des données est mis en œuvre sous la responsabilité du Commandant du CESAN de la Gendarmerie nationale.
          </p>

          <h2>Données collectées et finalités</h2>
          <p>Protect’Envi traite des données personnelles pour les finalités suivantes :</p>
          
          <DsfrHighlight class="fr-ml-0 fr-mb-4w">
            <ul class="fr-pl-2w fr-mb-0">
              <li>
                <strong>Gestion des accès des utilisateurs (agents habilités, élus locaux) :</strong> nom, prénom, adresse e-mail professionnelle, rôle, collectivité de rattachement.
              </li>
              <li>
                <strong>Constitution des signalements et procédures administratives / pénales :</strong> informations géographiques des dépôts sauvages, photos des constatations, détails sur les infractions, et le cas échéant, l'identité et les coordonnées des auteurs suspectés d'infraction environnementale (si identifiés lors de la procédure).
              </li>
              <li>
                <strong>Support et statistiques d'utilisation :</strong> suivi des demandes d'accompagnement et statistiques anonymisées.
              </li>
            </ul>
          </DsfrHighlight>

          <h2>Destinataires des données</h2>
          <p>Les données sont destinées exclusivement :</p>
          <ul class="fr-pl-3w fr-mb-3w">
            <li>Aux agents habilités des collectivités territoriales en charge du traitement des dépôts sauvages.</li>
            <li>Aux personnels habilités du CESAN de la Gendarmerie nationale et des unités locales de Gendarmerie ou de police compétentes pour faire suite aux procédures.</li>
            <li>À notre équipe technique (uniquement dans la limite stricte de la maintenance du service).</li>
          </ul>

          <h2>Durée de conservation</h2>
          <p>
            Les comptes d'utilisateurs inactifs sont supprimés au bout de 2 ans. Les données relatives aux procédures et aux constatations d'infractions sont conservées pendant les durées de prescription légale applicables aux procédures administratives ou judiciaires engagées.
          </p>

          <h2>Vos droits</h2>
          <p>
            Conformément à la réglementation, vous disposez d'un droit d'accès, de rectification, de limitation et d'opposition au traitement de vos données personnelles.
          </p>

          <DsfrAlert type="info" title="Exercer vos droits" class="fr-mb-4w">
            Pour exercer vos droits ou pour toute question relative au traitement de vos données, vous pouvez nous contacter à l'adresse e-mail suivante :
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
