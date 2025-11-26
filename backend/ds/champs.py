from django.utils import dateparse


class DSChamp:
    """
    Wrapper class for accessing DS dossier champs easily.
    """

    def __init__(self, dossier):
        self.champs = dossier.get("champs", [])

    def get_data(self):
        """
        Return a dictionary with champ IDs as keys and their extracted values.
        """
        data = {}
        for champ in self.champs:
            champ_id = champ.get("id")
            if champ_id:
                data[champ_id] = self.get_champ_value(champ)
        return data

    def get_champ_value(self, champ):
        """
        Extract the value from a DS GraphQL champ based on its type.
        """
        typename = champ.get("__typename") or ""
        if typename == "MultipleDropDownListChamp":
            return self.get_champ_list_value(champ)
        elif typename in ("YesNoChamp", "CheckboxChamp"):
            return self.get_champ_boolean_value(champ)
        elif typename in ("IntegerNumberChamp", "DecimalNumberChamp"):
            return self.get_champ_integer_value(champ)
        elif typename == "DatetimeChamp":
            return self.get_champ_datetime(champ)
        else:
            return self.get_champ_string_value(champ)

    def get_champ_string_value(self, champ):
        if champ.get("stringValue"):
            return champ["stringValue"]
        if champ.get("value") is not None:
            return str(champ["value"])
        return ""

    def get_champ_boolean_value(self, champ):
        if champ.get("value") is not None:
            return bool(champ["value"])
        string_value = champ.get("stringValue", "").lower()
        if string_value in ("true", "1", "yes", "oui"):
            return True
        return False

    def get_champ_list_value(self, champ):
        if champ.get("values"):
            return champ["values"]
        if champ.get("stringValue"):
            return [champ["stringValue"]]
        return []

    def get_champ_integer_value(self, champ):
        if champ.get("value") is not None:
            try:
                return int(float(champ["value"]))
            except (ValueError, TypeError):
                pass
        string_value = champ.get("stringValue")
        try:
            return int(float(string_value))
        except (ValueError, TypeError):
            pass
        return None

    def get_champ_datetime(self, champ):
        if champ.get("datetime"):
            return dateparse.parse_datetime(champ["datetime"])
        return None
