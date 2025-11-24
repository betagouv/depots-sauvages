import json
import logging

import requests
from django.conf import settings

from backend.ds.queries import GET_SIGNALEMENT_DOSSIER_QUERY

logger = logging.getLogger(__name__)


class DSGraphQLClient:
    """
    Client for DS GraphQL API.
    """

    def __init__(self, api_token=None):
        """
        Configure DS GraphQL client.
        """
        self.api_token = api_token or settings.DS_API_TOKEN
        if not self.api_token:
            raise ValueError("API token is required")
        self.endpoint = settings.DS_GRAPHQL_ENDPOINT
        self.timeout = settings.DS_REQUEST_TIMEOUT

    def _make_request(self, query, params=None):
        """
        Execute GraphQL request.
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_token}"}
        payload = {"query": query, "variables": params or {}}
        try:
            logger.debug(f"Calling DS GraphQL endpoint: {query[:100]}...")
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
            logger.error("DS API request failed: %s", error)
            raise
        except json.JSONDecodeError as error:
            logger.error("Failed to parse DS API response: %s", error)
            raise ValueError("Invalid JSON response from DS API") from error

    def get_dossier(self, numero_dossier):
        """
        Fetch dossier data.
        """
        params = {"dossierNumber": numero_dossier}
        data = self._make_request(GET_SIGNALEMENT_DOSSIER_QUERY, params)
        return data.get("dossier", {})
