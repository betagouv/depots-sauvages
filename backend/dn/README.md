# DN Integration

Django app for integrating with Démarche Numérique (DN) GraphQL API.

## Features

- GraphQL client for DN API
- Simple data retrieval : demarche and dossier information

## Configuration

### Base Settings

```python
# backend/settings/base.py
DN_GRAPHQL_ENDPOINT = "https://demarche.numerique.gouv.fr/api/v2/graphql"
DN_REQUEST_TIMEOUT = 30
DN_MAX_RETRIES = 3
```

### Environment-Specific Settings

```python
DN_API_TOKEN = "SOME-KEY"
```

## Usage

```python
from backend.dn.client import DNGraphQLClient

client = DNGraphQLClient()
dossier = client.get_dossier(123456)
```
