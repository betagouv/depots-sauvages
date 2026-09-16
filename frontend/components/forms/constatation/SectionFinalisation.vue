<template>
  <fieldset class="fr-fieldset fr-my-0 fr-mt-4w">
    <legend class="fr-fieldset__legend">
      <h2 class="premium-h2">
        <span class="premium-badge">{{ sectionNumber }}</span>
        Finalisation de la démarche
      </h2>
    </legend>

    <div class="fr-fieldset__element">
      <fieldset class="fr-fieldset">
        <legend class="fr-fieldset__legend fr-text--bold">Traitement de vos données *</legend>
        <DsfrCheckbox
          v-model="store.formData.accepteTraitementDonnees"
          label="J'ai pris connaissance des informations ci-dessous et du traitement de mes données par Stop Dépôt Sauvage dans le cadre de ma procédure (rédaction du constat, génération de la lettre d'information, suivi du dossier)."
          name="accepteTraitementDonnees"
          :required="true"
          :error-message="store.errors.accepteTraitementDonnees"
          @update:model-value="store.clearFieldError('accepteTraitementDonnees')"
        />
      </fieldset>
      <div class="fr-ml-4w fr-mt-1w fr-text--sm fr-text--mention-grey">
        <p class="fr-mb-1v">Les informations saisies dans ce formulaire sont utilisées pour :</p>
        <ul class="fr-mb-0">
          <li>Générer les documents liés à votre procédure (constat et lettre d'information) ;</li>
          <li>Assurer le suivi de votre dossier.</li>
        </ul>
        <p class="fr-mt-1v">
          Vos données sont conservées le temps nécessaire au traitement de votre procédure, y compris
          en cas de recours devant le tribunal administratif, et au maximum 2 ans après sa clôture.
          Vous pouvez à tout moment demander la modification ou la suppression de ces données en nous
          contactant sur <a :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
        </p>
      </div>
    </div>

    <div class="fr-fieldset__element">
      <fieldset class="fr-fieldset">
        <legend class="fr-fieldset__legend fr-text--bold">
          Besoin d'un accompagnement ? (optionnel)
        </legend>
        <DsfrCheckbox
          v-model="store.formData.besoinAccompagnement"
          label="J'ai besoin d'aide pour la suite de cette procédure et je souhaite être recontacté(e) par mail ou téléphone par l'équipe Stop Dépôt Sauvage."
          name="besoinAccompagnement"
          @update:model-value="onBesoinAccompagnementChange"
        />
      </fieldset>
    </div>

    <div v-if="store.formData.besoinAccompagnement" class="fr-fieldset__element">
      <DsfrInputGroup
        v-model="store.formData.contactTelephone"
        type="tel"
        label="Numéro de téléphone (optionnel)"
        hint="Format attendu : Un numéro de téléphone valide. Exemple : 0612345678"
      />
      <p class="fr-text--sm fr-text--mention-grey fr-mt-1w">
        Si vous souhaitez être contacté(e) par téléphone dans le cadre de notre accompagnement, vous
        pouvez indiquer votre téléphone pour faciliter les échanges.
      </p>
    </div>

    <div class="fr-fieldset__element">
      <DsfrRadioButtonSet
        v-model="store.formData.ceciEstUnTest"
        :required="true"
        :options="[
          { label: 'C\'est un cas réel de dépôt sauvage', value: false, id: 'test-non' },
          { label: 'Il s\'agit d\'un test ou d\'une démonstration', value: true, id: 'test-oui' },
        ]"
        :error-message="store.errors.ceciEstUnTest"
        @update:model-value="store.clearFieldError('ceciEstUnTest')"
      >
        <template #legend>
          Concernant la démarche que vous venez de remplir : *
          <span class="fr-hint-text">
            Le dispositif <strong>Stop Dépôt Sauvage</strong> étant en expérimentation merci de nous préciser s'il s'agit
            d'un cas réel ou simplement d'un test.
          </span>
        </template>
      </DsfrRadioButtonSet>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { useConstatationStore } from '@/stores/constatation'
import { DsfrCheckbox, DsfrInputGroup, DsfrRadioButtonSet } from '@gouvminint/vue-dsfr'
import { computed } from 'vue'

const contactEmail = import.meta.env.VITE_CONTACT_EMAIL || 'contact@stopdepotsauvage.beta.gouv.fr'

const store = useConstatationStore()

// Sans demande d'accompagnement, il n'y a plus de finalité à conserver le numéro saisi
const onBesoinAccompagnementChange = (value: boolean) => {
  if (!value) store.formData.contactTelephone = ''
}

const showPrejudice = computed(() =>
  ['Déposée', 'Sera déposée'].includes(store.formData.plainteEtat)
)
const sectionNumber = computed(() => (showPrejudice.value ? 6 : 5))
</script>
