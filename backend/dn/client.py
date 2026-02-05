import json
import logging

import requests
from django.conf import settings

from backend.dn.queries import GET_DEMARCHE_DOSSIERS_QUERY, GET_SIGNALEMENT_DOSSIER_QUERY

logger = logging.getLogger(__name__)


class DNGraphQLClient:
    """
    Client for DN GraphQL API.
    """

    def __init__(self, api_token=None):
        """
        Configure DN GraphQL client.
        """
        self.api_token = api_token or settings.DN_API_TOKEN
        if not self.api_token:
            raise ValueError("API token is required")
        self.endpoint = settings.DN_GRAPHQL_ENDPOINT
        self.timeout = settings.DN_REQUEST_TIMEOUT
        self.demarche_number = settings.DN_DEMARCHE_NUMBER

    def make_request(self, query, params=None):
        """
        Execute GraphQL request.
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_token}"}
        payload = {"query": query, "variables": params or {}}
        try:
            logger.debug(f"Calling DN GraphQL endpoint: {query[:100]}...")
            response = requests.post(
                self.endpoint, headers=headers, json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                messages = [error.get("message", "Unknown error") for error in data["errors"]]
                raise ValueError(f"GraphQL errors: {'; '.join(messages)}")
            return data.get("data", {})
        except requests.RequestException as error:
            logger.error("DN API request failed: %s", error)
            raise
        except json.JSONDecodeError as error:
            logger.error("Failed to parse DN API response: %s", error)
            raise ValueError("Invalid JSON response from DN API") from error

    def get_dossier(self, numero_dossier):
        """
        Fetch dossier data.
        """
        params = {"dossierNumber": numero_dossier}
        data = self.make_request(GET_SIGNALEMENT_DOSSIER_QUERY, params)
        return data.get("dossier", {})

    def get_dossiers_for_demarche(self, demarche_number=None):
        """
        Fetch all dossiers for a given demarche.
        """
        if not demarche_number:
            demarche_number = self.demarche_number
        if not demarche_number:
            raise ValueError("Demarche number is required")
        dossiers = []
        has_next_page = True
        after_cursor = None
        while has_next_page:
            params = {"demarcheNumber": demarche_number, "after": after_cursor}
            data = self.make_request(GET_DEMARCHE_DOSSIERS_QUERY, params)
            demarche_data = data.get("demarche", {})
            if not demarche_data:
                break
            dossiers_connection = demarche_data.get("dossiers", {})
            nodes = dossiers_connection.get("nodes", [])
            dossiers.extend(nodes)
            page_info = dossiers_connection.get("pageInfo", {})
            has_next_page = page_info.get("hasNextPage", False)
            after_cursor = page_info.get("endCursor")

        return dossiers

    def get_dossiers_for_user(self, user_email):
        """
        Fetch dossiers for a specific user email.
        """
        if not user_email:
            return []
        # Optimize: Filter on client side for now as API might not support email filter
        all_dossiers = self.get_dossiers_for_demarche()
        user_dossiers = [
            d
            for d in all_dossiers
            if d.get("usager", {}).get("email", "").lower() == user_email.lower()
        ]
        return user_dossiers
