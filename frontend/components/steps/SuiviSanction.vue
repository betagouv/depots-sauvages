<template>
  <div class="step-suivi">
    <DsfrHighlight class="fr-ml-0 fr-mb-4w">
      Le délai de contradictoire s’étend sur un minimum de <strong>10 jours</strong> à compter de la
      réception de la lettre d'information. Une fois ce délai écoulé, vous pouvez agir en fonction
      des éventuelles observations formulées par l’auteur. Plusieurs scénarios sont alors
      possibles : <strong>Poursuivre la procédure contre l'auteur du dépôt sauvage</strong> ou
      <strong>abandonner les poursuites</strong>.
    </DsfrHighlight>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">1. Poursuivre la procédure</h5>
          <ul class="fr-p-0 fr-m-0" style="list-style: none">
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Fixer le montant de l'amende administrative (montant proportionné avec un maximum de
                15 000 €).
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/df51fe02-90dd-4afc-9346-8ae9b56fcea4"
                  target="_blank"
                >
                  Voir l'exemple de grille d'amende.</a
                >
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Rédiger l'arrêté de sanction administrative relatif à l'amende.
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/7b97c0e9-ffc9-4863-834f-759821aa1e0a"
                  target="_blank"
                  >Voir le modèle d'arrêté</a
                >.
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Émettre un titre de recette (copie de l'arrêté d'amende à transmettre au Trésor
                Public)
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Notifier l'auteur.
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/50055a0b-bcfc-472c-8ec1-9f267a11e2c4"
                  target="_blank"
                >
                  Voir le modèle de courrier de notification d'amende</a
                >
              </span>
            </li>
          </ul>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">2. Abandonner les poursuites</h5>
          <ul class="fr-p-0 fr-m-0" style="list-style: none">
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span
                >L'auteur a fourni des preuves suffisantes démontrant qu'il n'est pas responsable ou
                l'auteur est responsable du dépôt mais la collectivité décide de faire preuve
                d'indulgence</span
              >
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Un courrier lui est adressé pour le notifier de la décision d'abandon de la
                procédure administrative.
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/25afb89c-abbe-434c-b498-596c12eb60bd"
                  target="_blank"
                >
                  Voir le modèle de courrier de notification</a
                >.
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Le cas échéant, une nouvelle procédure peut être initiée à l'encontre d'un autre
                auteur identifié (ex. prestataire, sous-traitant, fournisseur, client,
                intermédiaire).
                <a href="https://protect-envi.beta.gouv.fr/" target="_blank">
                  Démarrer une nouvelle procédure</a
                >.
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { DsfrHighlight } from '@gouvminint/vue-dsfr'
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

.action-icon {
  color: var(--text-active-blue-france);
  flex-shrink: 0;
  margin-top: 0.125rem;
}

li.fr-display-flex {
  align-items: flex-start;
}
</style>
