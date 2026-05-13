<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">6</span>
        Finalisation de la démarche
      </h2>
    </legend>

    <div class="fr-fieldset__element">
      <fieldset class="fr-fieldset">
        <legend class="fr-fieldset__legend fr-text--bold">
          Accompagnement personnalisé
        </legend>
        <DsfrCheckbox
          v-model="store.formData.accepteAccompagnement"
          label="Je comprends que je peux être recontacté(e) dans le cadre d'un accompagnement personnalisé."
          name="accepteAccompagnement"
        />
      </fieldset>
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
        :required="false"
        :options="[
          { label: 'C\'est un cas réel de dépôt sauvage', value: false, id: 'test-non' },
          { label: 'Il s\'agit d\'un test ou d\'une démonstration', value: true, id: 'test-oui' },
        ]"
      >
        <template #legend>
          Concernant la démarche que vous venez de remplir : *
          <span class="fr-hint-text">
            Le dispositif Protect'Envi étant en expérimentation merci de nous préciser s'il s'agit
            d'un cas réel ou simplement d'un test.
          </span>
        </template>
      </DsfrRadioButtonSet>
    </div>

    <DsfrCallout title="Merci pour toutes ces informations." class="fr-mb-2w">
      <p>
        Une fois votre constatation enregistrée, vous pourrez accéder au suivi de votre dossier et
        télécharger votre rapport de constatation directement depuis votre
        <router-link to="/mes-procedures">espace de suivi</router-link>.
      </p>
      <p class="fr-text--bold fr-mt-2w">Attention la procédure n'est pas terminée !</p>
      <p>
        Le rapport de constatation généré devra être signé par l'autorité compétente pour avoir une
        valeur juridique.
      </p>
    </DsfrCallout>
  </fieldset>
</template>

<script setup lang="ts">
import { useConstatationStore } from '@/stores/constatation'
import { DsfrCallout, DsfrCheckbox, DsfrInputGroup, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'

const store = useConstatationStore()
</script>
