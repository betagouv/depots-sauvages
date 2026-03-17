<template>
  <div class="step-suivi">
    <DsfrHighlight class="fr-ml-0 fr-mb-4w">
      La période du contradictoire de 10 jours minimum est écoulée. Il faut maintenant analyser les
      éventuelles observations de l'auteur et déterminer les actions à entreprendre, il y a deux
      situations possibles : <b>poursuivre la procédure</b> ou <b>abandonner les poursuites</b>.
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
                Fixer le montant de l'amende administrative : un montant proportionné avec un
                maximum de 15 000 €.
                <a
                  href="https://fichiers.numerique.gouv.fr/explorer/items/files/df51fe02-90dd-4afc-9346-8ae9b56fcea4"
                  target="_blank"
                  >Voir l'exemple de grille d'amende.></a
                >
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Rédiger l'arrêté de sanction administrative relatif à l'amende
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
                Émettre un titre de recette (copie de l'arrêté d'amende à transmettre au trésor
                public)
              </span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>Notifier l'auteur</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="fr-col-12 fr-col-md-6">
        <div class="procedure-choice fr-p-3w">
          <h5 class="fr-h5 fr-mb-2w">2. Abandon</h5>
          <ul class="fr-p-0 fr-m-0" style="list-style: none">
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>Envoyer un courrier pour informer la personne mise en cause.</span>
            </li>
            <li class="fr-mb-2w fr-display-flex">
              <span
                class="fr-icon-checkbox-circle-line fr-mr-1v action-icon"
                aria-hidden="true"
              ></span>
              <span>
                Noter les raisons de l'abandon : l'auteur a fourni des preuves, indulgence, autres.
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
}
</style>
