class PrejudiceMixin:
    AGENT_HOURLY_RATE = 18.03  # In euros, the hourly rate of a person
    VEHICLE_USAGE_RATE = 1.30  # In euros, the usage rate of a vehicle

    def get_prejudice_montant_calcule(self):
        """
        Calculate the total amount of prejudice when the amount is unknown.
        """
        if self.prejudice_montant_connu:
            return self.prejudice_montant
        agent_cost = self.prejudice_nombre_personnes * self.AGENT_HOURLY_RATE
        total_agent_cost = agent_cost * self.prejudice_nombre_heures
        vehicle_cost = self.prejudice_kilometrage * self.VEHICLE_USAGE_RATE
        total_vehicle_cost = vehicle_cost * self.prejudice_nombre_vehicules
        total_cost = self.prejudice_autres_couts + total_agent_cost + total_vehicle_cost
        return total_cost
