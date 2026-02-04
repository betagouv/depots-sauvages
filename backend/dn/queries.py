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
        demandeur {
            ... on PersonnePhysique {
                nom
                prenom
            }
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
            ... on DatetimeChamp {
                datetime
            }
            ... on DecimalNumberChamp {
                value
            }
            ... on IntegerNumberChamp {
                value
            }
            ... on CheckboxChamp {
                value
            }
            ... on SiretChamp {
                stringValue
            }
            ... on AddressChamp {
                address {
                    postalCode
                    cityName
                    cityCode
                    label
                    streetAddress
                    streetName
                    streetNumber
                }
            }
        }
    }
}
"""


GET_DEMARCHE_DOSSIERS_QUERY = """
query GetDemarcheDossiers($demarcheNumber: Int!, $after: String) {
    demarche(number: $demarcheNumber) {
        dossiers(after: $after) {
            pageInfo {
                endCursor
                hasNextPage
            }
            nodes {
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
                    ... on DatetimeChamp {
                        datetime
                    }
                    ... on DecimalNumberChamp {
                        value
                    }
                    ... on IntegerNumberChamp {
                        value
                    }
                    ... on CheckboxChamp {
                        value
                    }
                    ... on SiretChamp {
                        stringValue
                    }
                    ... on AddressChamp {
                        address {
                            postalCode
                            cityName
                            cityCode
                            label
                            streetAddress
                            streetName
                            streetNumber
                        }
                    }
                }
            }
        }
    }
}
"""
