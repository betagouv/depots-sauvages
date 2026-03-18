<template>
  <div class="step-suivi">
    <DsfrHighlight class="fr-ml-0 fr-mb-4w">
      <p>
        La période du contradictoire s'étend sur un minimum de <strong>10 jours</strong> à compter
        de la réception de la lettre d'information. Une fois ce délai écoulé, deux issues sont
        possibles selon la réponse de l'auteur présumé :
      </p>
      <ul class="fr-mb-0">
        <li>
          <strong>Soit sanctionner l'auteur du dépôt sauvage</strong>
          <ul>
            <li>S'il a reconnu les faits ;</li>
            <li>
              S'il n'a pas répondu à la lettre d'information avant la fin de la période du
              contradictoire ;
            </li>
            <li>S'il nie les faits, mais les preuves contre lui sont accablantes.</li>
          </ul>
        </li>
        <li class="fr-mt-1w">
          <strong>Soit abandonner les poursuites</strong>
          <ul>
            <li>S'il y a un doute sur sa culpabilité ;</li>
            <li>Si l'on souhaite faire preuve d'indulgence ;</li>
            <li>Si la réponse à la lettre d'information désigne un autre auteur présumé.</li>
          </ul>
        </li>
      </ul>
    </DsfrHighlight>

    <div class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">1. Sanctionner l'auteur</h5>
          <ul class="fr-p-0 fr-m-0" style="list-style: none">
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Fixer le montant de l'amende administrative (montant proportionné à la gravité des
                faits, jusqu'à 15 000 € maximum).
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/df51fe02-90dd-4afc-9346-8ae9b56fcea4"
                  target="_blank"
                >
                  Consulter l'aide à l'évaluation de l'amende</a
                >
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Rédiger l'arrêté de sanction administrative relatif à l'amende et le soumettre au
                contrôle de légalité
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/7b97c0e9-ffc9-4863-834f-759821aa1e0a"
                  target="_blank"
                  >Voir le modèle d'arrêté</a
                >
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span> Émettre un titre de recette à destination du Trésor public </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Notifier l'auteur.
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/563be397-7e6d-4d69-b1aa-42598d2f71c6"
                  target="_blank"
                >
                  Voir le modèle de courrier de notification d'amende.</a
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
              <span>
                Notifier la personne concernée de la décision d'abandon de la procédure
                administrative
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/25afb89c-abbe-434c-b498-596c12eb60bd"
                  target="_blank"
                >
                  Voir le modèle de courrier de notification</a
                >
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Le cas échéant, la procédure peut être établie à l'encontre d'un autre auteur
                identifié (ex. prestataire, sous-traitant, fournisseur, client, intermédiaire).
                <a :href="modifyUrl" target="_blank">
                  Modifier la procédure sur Démarche Numérique.</a
                >
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

defineProps<{
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

.action-icon {
  color: var(--text-active-blue-france);
  flex-shrink: 0;
  margin-top: 0.125rem;
}

li.fr-display-flex {
  align-items: flex-start;
}
</style>
