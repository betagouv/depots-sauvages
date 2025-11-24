class PrejudiceMixin:
    AGENT_HOURLY_RATE = 18.03  # In euros, the hourly rate of a person
    VEHICLE_USAGE_RATE = 1.30  # In euros, the usage rate of a vehicle

    def get_prejudice_montant_calcule(self):
        """
        Calculate the total amount of prejudice when the amount is unknown.
        """
        if self.prejudice_montant_connu:
            return self.prejudice_montant
        nombre_personnes = self.prejudice_nombre_personnes or 0
        nombre_heures = self.prejudice_nombre_heures or 0
        kilometrage = self.prejudice_kilometrage or 0
        nombre_vehicules = self.prejudice_nombre_vehicules or 0
        autres_couts = self.prejudice_autres_couts or 0
        agent_cost = nombre_personnes * self.AGENT_HOURLY_RATE
        total_agent_cost = agent_cost * nombre_heures
        vehicle_cost = kilometrage * self.VEHICLE_USAGE_RATE
        total_vehicle_cost = vehicle_cost * nombre_vehicules
        total_cost = autres_couts + total_agent_cost + total_vehicle_cost
        return total_cost
