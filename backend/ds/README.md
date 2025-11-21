# DS Integration

Django app for integrating with Démarches Simplifiées (DS) GraphQL API.

## Features

- GraphQL client for DS API
- Simple data retrieval : demarche and dossier information

## Configuration

### Base Settings

```python
# backend/settings/base.py
DS_GRAPHQL_ENDPOINT = "https://www.demarches-simplifiees.fr/api/v2/graphql"
DS_REQUEST_TIMEOUT = 30
DS_MAX_RETRIES = 3
```

### Environment-Specific Settings

```python
DS_API_TOKEN = "SOME-KEY"
```

## Usage

```python
from backend.ds.client import DSGraphQLClient

client = DSGraphQLClient()
dossier = client.get_dossier(123456)
```
