GET_SIGNALEMENT_DOSSIER_QUERY = """
query GetSignalementDossier($dossierNumber: Int!) {
    dossier(number: $dossierNumber) {
        id
        number
        state
        dateDepot
        dateDerniereModification
        usager {
            email
        }
        champs {
            id
            label
            stringValue
            __typename
            ... on TextChamp {
                stringValue
            }
            ... on YesNoChamp {
                value
            }
            ... on MultipleDropDownListChamp {
                values
            }
            ... on CommuneChamp {
                commune {
                    name
                    code
                    postalCode
                }
            }
            ... on AddressChamp {
                address {
                    label
                    streetAddress
                    postalCode
                    cityName
                }
            }
            ... on DatetimeChamp {
                datetime
            }
            ... on DecimalNumberChamp {
                value
            }
        }
    }
}
"""

__all__ = ["GET_SIGNALEMENT_DOSSIER_QUERY"]
# End of queries
