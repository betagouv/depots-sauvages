<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h3 class="fr-h2">5. Finalisation de la démarche</h3>
    </legend>

    <div class="fr-fieldset__element">
      <DsfrCheckbox
        v-model="store.formData.accepteAccompagnement"
        :required="true"
        label="Je comprends que je peux être recontacté(e) dans le cadre d'un accompagnement personnalisé."
        name="accepteAccompagnement"
      />
      <div class="fr-ml-4w fr-mt-1w fr-text--sm fr-text--mention-grey">
        <p class="fr-mb-1v">
          Les informations saisies dans ce formulaire sont uniquement utilisées pour :
        </p>
        <ul class="fr-mb-0">
          <li>Vous transmettre les documents demandés (rapport et lettre d'information) ;</li>
          <li>
            Échanger avec vous et assurer le suivi de votre demande si vous avez accepté un
            accompagnement personnalisé.
          </li>
        </ul>
        <p class="fr-mt-1v">
          Vos données seront conservées pendant 12 mois puis supprimées. Vous pouvez à tout moment
          réclamer la modification ou la suppression de ces données en nous contactant sur
          <a href="mailto:contact@protect-envi.beta.gouv.fr">contact@protect-envi.beta.gouv.fr</a>
        </p>
      </div>
    </div>

    <div v-if="store.formData.accepteAccompagnement" class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.contactTelephone"
        type="tel"
        label="Numéro de téléphone (optionnel)"
        hint="Format attendu : Un numéro de téléphone valide. Exemple : 0612345678"
      />
      <p class="fr-text--sm fr-text--mention-grey fr-mt-1w">
        Si vous souhaitez être contacter par téléphone dans le cadre de notre accompagnement, vous
        pouvez indiquer votre téléphone pour faciliter les échanges.
      </p>
    </div>

    <div class="fr-fieldset__element">
      <DsfrRadioButtonSet
        v-model="store.formData.ceciEstUnTest"
        legend="Concernant la démarche que vous venez de remplir :"
        hint="Le dispositif Protect'Envi étant en expérimentation merci de nous préciser s'il s'agit d'un cas réel ou simplement d'un test."
        :required="true"
        :options="[
          { label: 'C\'est un cas réel de dépôt sauvage', value: false, id: 'test-non' },
          { label: 'Il s\'agit d\'un test ou d\'une démonstration', value: true, id: 'test-oui' },
        ]"
      />
    </div>

    <div class="fr-callout fr-mb-2w fr-callout--blue-cumulus">
      <h3 class="fr-callout__title">
        Merci pour toutes ces informations, vous pouvez valider votre dossier pour recevoir votre
        rapport de constatation par courriel
      </h3>
      <p class="fr-callout__text fr-text--bold">
        ⚠️ Attention cette démarche n'est pas automatisée !
      </p>
      <p class="fr-callout__text">Après avoir déposé votre dossier :</p>
      <ul class="fr-callout__text">
        <li>✉️ Les pièces de procédure pré-remplies vous</li>
        <li>
          ✍️ Le rapport de constatation est envoyé par courriel. Il doit être signé par l'autorité
          compétente.
        </li>
      </ul>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { useConstatationStore } from '@/stores/constatation'
import { DsfrCheckbox, DsfrInputGroup, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'

const store = useConstatationStore()
</script>
