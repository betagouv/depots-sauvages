<template>
  <div class="step-identification">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">Identifier avec l'immatriculation</h5>

          <DsfrAlert type="info" title="Modèle de document" class="fr-mb-2w">
            <a
              href="https://fichiers.numerique.gouv.fr/explorer/items/files/c7935d81-0c1d-488f-b7ab-9e3686cc7858"
              target="_blank"
              class="fr-btn fr-btn--secondary fr-btn--sm"
            >
              Demander l'identité à la gendarmerie
            </a>
          </DsfrAlert>

          <p class="fr-text--sm">
            Vous avez l'immatriculation du véhicule de l'auteur présumé, mais vous n'avez pas
            l'identité complète (Nom, prénom, adresse postale) :
          </p>
          <ul class="fr-pl-2w fr-mb-0 fr-text--sm">
            <li class="fr-mb-1w">
              La Police municipale, si elle est habilitée et équipée,
              <a
                href="https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043258386?r=VjMKmD4WYh#:~:text=Notice%20%3A%20le%20d%C3%A9cret%20permet%20aux,%C3%A0%20l'abandon%20ou%20au"
                target="_blank"
                >peut consulter les informations du SIV</a
              >.
            </li>
            <li class="fr-mb-1w">
              La <strong>gendarmerie peut communiquer à la police municipale</strong> les
              informations du SIV (système d'immatriculation des véhicules).
            </li>
            <li class="fr-mb-1w">
              Si la mairie n'a pas de police municipale, rapprochez-vous de la brigade de
              gendarmerie pour connaître les modalités de communication d'identité (selon la
              politique pénale locale).
            </li>
          </ul>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">Identifier par l'enquête judiciaire</h5>

          <DsfrAlert type="info" title="Modèle de document" class="fr-mb-2w">
            <a
              href="https://docs.numerique.gouv.fr/docs/a89aad6d-bcdf-4f28-b6f2-e34c83e62313/"
              target="_blank"
              class="fr-btn fr-btn--secondary fr-btn--sm"
            >
              Demander l'adresse au Procureur
            </a>
          </DsfrAlert>

          <p class="fr-text--sm">
            Vous n'avez pas l'identité complète (Nom, Prénom, adresse postale), vous pouvez porter
            plainte pour que l'auteur soit identifié par une enquête judiciaire.
          </p>
          <ul class="fr-pl-2w fr-mb-0 fr-text--sm">
            <li class="fr-mb-1w">
              Prenez rendez-vous
              <a
                href="https://www.masecurite.interieur.gouv.fr/fr/trouver-un-commissariat-une-gendarmerie"
                target="_blank"
                >auprès de la brigade de gendarmerie ou du commissariat</a
              >
              pour <strong>déposer plainte</strong>.
            </li>
            <li class="fr-mb-1w">
              <strong>Transmettez</strong> une copie du rapport de constatation lors de votre dépôt
              de plainte.
            </li>
            <li class="fr-mb-1w">
              En tant que victime du dépôt, le maire peut demander la communication de la procédure
              judiciaire au procureur de la République.
            </li>
          </ul>
        </div>
      </div>

      <div class="fr-col-12">
        <div class="identification-outcome fr-p-3w fr-mt-4w">
          <h5 class="fr-h5 fr-mb-2w text-center">Avez-vous réussi à identifier l'auteur ?</h5>
          <div class="fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-grid-row--stretch">
            <div class="fr-col-12 fr-col-md-6">
              <DsfrCheckbox
                name="id-reussie-oui"
                label="Oui, j'ai identifié l'auteur"
                :model-value="suivi.identification_reussie === true"
                @update:model-value="toggleChoice(true)"
              />
            </div>
            <div class="fr-col-12 fr-col-md-6">
              <DsfrCheckbox
                name="id-reussie-non"
                label="Non, je n'ai pas pu identifier l'auteur"
                :model-value="suivi.identification_reussie === false"
                @update:model-value="toggleChoice(false)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SuiviProcedure } from '../../stores/suivi-procedure'

const props = defineProps<{
  suivi: SuiviProcedure
  auteurIdentifie?: boolean
  modifyUrl?: string
}>()

const toggleChoice = (val: boolean) => {
  if (props.suivi.identification_reussie === val) {
    props.suivi.identification_reussie = null
  } else {
    props.suivi.identification_reussie = val
  }
}
</script>

<style scoped>
.procedure-choice {
  background-color: var(--background-alt-grey);
  border-radius: 8px;
  height: 100%;
  border: 1px solid var(--border-default-grey);
}

.procedure-choice:hover {
  background-color: var(--background-alt-grey-hover);
}

.identification-outcome {
  background-color: var(--background-alt-blue-france);
  border-radius: 12px;
  border: 1px solid var(--border-default-blue-france);
  box-shadow: 0 4px 12px rgba(0, 0, 145, 0.05);
}

.identification-outcome :deep(.fr-checkbox-group) {
  background-color: var(--background-default-grey);
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-default-grey);
  transition: all 0.2s ease;
  height: 100%;
  margin-bottom: 0;
}

.identification-outcome :deep(.fr-checkbox-group:hover) {
  background-color: var(--background-alt-grey-hover);
}

.identification-outcome :deep(.fr-checkbox-group input[type='checkbox']:checked + label) {
  font-weight: bold;
}

.text-center {
  text-align: center;
}
</style>
