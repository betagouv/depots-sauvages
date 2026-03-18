<template>
  <div class="step-identification">
    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">Identifier l'auteur via l'immatriculation</h5>
          <p class="fr-text--sm">
            Vous avez l'immatriculation du véhicule de l'auteur présumé, mais vous n'avez pas
            l'identité complète (Nom, prénom, adresse postale) :
          </p>
          <ul class="fr-pl-2w fr-mb-2w fr-text--sm">
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
              informations du SIV (système d’immatriculation des véhicules).
            </li>
            <li class="fr-mb-1w">
              Si la mairie n’a pas de police municipale, rapprochez-vous de la brigade de
              gendarmerie pour connaître les modalités de communication d’identité (selon la
              politique pénale locale).
              <a
                href="https://fichiers.numerique.gouv.fr/explorer/items/50055a0b-bcfc-472c-8ec1-9f267a11e2c4"
                target="_blank"
                >(Modèle de courrier)</a
              >.
            </li>
          </ul>
          <p class="fr-text--sm fr-mb-0">
            Une fois l'identité déterminée, vous pouvez mettre à jour votre procédure :
            <a
              :href="modifyUrl"
              target="_blank"
              class="fr-link fr-icon-external-link-line fr-link--icon-right"
            >
              Modifier la procédure sur Démarche Numérique
            </a>
          </p>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">Identifier l'auteur via une enquête judiciaire</h5>
          <p class="fr-text--sm">
            Vous n'avez pas l'identité complète (Nom, Prénom, adresse postale), vous pouvez porter
            plainte pour que l'auteur soit identifié par une enquête judiciaire.
          </p>
          <ul class="fr-pl-2w fr-mb-2w fr-text--sm">
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
              En tant qu’OPJ, le maire peut demander la communication de l’adresse de l’auteur
              potentiel au procureur de la République.
              <a
                href="https://docs.numerique.gouv.fr/docs/a89aad6d-bcdf-4f28-b6f2-e34c83e62313/"
                target="_blank"
                >(Modèle de courrier)</a
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  auteurIdentifie?: boolean
  modifyUrl?: string
}>()
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
</style>
