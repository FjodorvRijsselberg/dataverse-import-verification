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
- doi - e.g. doi:10.5072/FK2/1YCZOL - DOI of the dataset
- metadata - [link to example](https://guides.dataverse.org/en/latest/_downloads/4e04c8120d51efab20e480c6427f139c/dataset-create-new-all-default-fields.json)  - The metadata describing a dataset in JSON formatted for Dataverse
- base_url - e.g. _https://portal.odissei.nl/_ - The URL of the Dataverse instance
- api_token - e.g. _12345678-ab12-12ab-abcd-a1b2c3d4e5g6_ - API token of the specific Dataverse- 

> Tip: login to the Dataverse instance as admin and click your username in the top right to find your token

#### Return value
When successful, the API call will return a confirmation message containing the dataset's PID and database id.
The call will return an exception on a failed attempt further elaborating what went wrong.
