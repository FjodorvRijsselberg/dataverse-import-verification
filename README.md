# dataverse-import-verification
The dataverse-import-verification API can be used to verify imported JSON metadata.
You can import metadata using the [dataverse-importer](https://github.com/odissei-data/dataverse-importer) API.

## Frameworks
This project uses:
- Python 3.9
- FastAPI
- Poetry

## Setup
The default port in the example .env is 8090, change it to fit your needs.
1. `cp dot_env_example .env`
2. `make build`


## End-points
The following endpoints are available.

### Version
Returns the current version of the API

### Verify
Verifies if metadata has been imported correctly.

#### Parameters

- "doi": "hdl:10622/8KCCXB",
- "source_url": "https://datasets.iisg.amsterdam",
- "source_api_token": "46f3b381-6d58-461a-8b46-b884a1bdc1f0",
- "destination_url": "http://localhost:8080",
- "destination_api_token": "7322d16a-beb1-48c7-92ec-a278015cbd52"

> Tip: login to the Dataverse instance as admin and click your username in the top right to find your token

#### Return value
When successful, the API call will return a confirmation message containing the dataset's PID and database id.
The call will return an exception on a failed attempt further elaborating what went wrong.
