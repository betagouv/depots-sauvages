from django.utils import dateparse


class DNField:
    """Wrapper class for accessing DN dossier fields easily."""

    def __init__(self, dossier):
        self.raw_fields = dossier.get("champs", [])

    def get_data(self):
        """Return a dictionary with field IDs as keys and their extracted values."""
        data = {}
        for field in self.raw_fields:
            field_id = field.get("id")
            if field_id:
                data[field_id] = self.get_field_value(field)
        return data

    def get_field_value(self, field):
        """Extract the value from a DN GraphQL field based on its type."""
        typename = field.get("__typename") or ""
        if typename == "MultipleDropDownListChamp":
            return self.get_list_value(field)
        elif typename in ("YesNoChamp", "CheckboxChamp"):
            return self.get_boolean_value(field)
        elif typename in ("IntegerNumberChamp", "DecimalNumberChamp"):
            return self.get_numeric_value(field)
        elif typename == "DatetimeChamp":
            return self.get_datetime_value(field)
        elif typename == "AddressChamp":
            return self.get_address_value(field)
        elif typename == "SiretChamp":
            return self.get_siret_value(field)
        else:
            return self.get_string_value(field)

    def get_string_value(self, field):
        if field.get("stringValue"):
            return field["stringValue"]
        if field.get("value") is not None:
            return str(field["value"])
        return ""

    def get_boolean_value(self, field):
        if field.get("value") is not None:
            return bool(field["value"])
        string_value = field.get("stringValue", "").lower()
        if string_value in ("true", "1", "yes", "oui"):
            return True
        return False

    def get_list_value(self, field):
        if field.get("values"):
            return field["values"]
        if field.get("stringValue"):
            return [field["stringValue"]]
        return []

    def get_numeric_value(self, field):
        if field.get("value") is not None:
            try:
                return int(float(field["value"]))
            except (ValueError, TypeError):
                pass
        string_value = field.get("stringValue")
        try:
            return int(float(string_value))
        except (ValueError, TypeError):
            pass
        return None

    def get_datetime_value(self, field):
        if field.get("datetime"):
            return dateparse.parse_datetime(field["datetime"])
        return None

    def get_address_value(self, field):
        if field.get("address"):
            return field["address"]
        return None

    def get_siret_value(self, field):
        data = {"siret": field.get("stringValue") or ""}
        etablissement = field.get("etablissement")
        if etablissement:
            if etablissement.get("entreprise"):
                data["nom"] = etablissement["entreprise"].get("raisonSociale")
            if etablissement.get("address"):
                data["adresse_dict"] = etablissement["address"]
                data["adresse"] = etablissement["address"].get("label")
        return data
