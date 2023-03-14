import copy
import json
from collections.abc import MutableMapping
from contextlib import suppress

import requests
import uvicorn
from fastapi import FastAPI, HTTPException

from schema.input import VerifyInput
from version import get_version

description = """This dataverse-import-verification API can be used to verify
metadata that has been imported into Dataverse."""

tags_metadata = [
    {
        "name": "version",
        "description": "Returns the version of this API",
    },
    {
        "name": "importer",
        "description": "Verifies metadata imported into Dataverse",
        "externalDocs": {
            "description": "This API uses the Dataverse Native API",
            "url": "https://guides.dataverse.org/en/latest/api/",
        },
    },
]

app = FastAPI(
    title="dataverse-import-verification",
    description=description,
    version="0.1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)


@app.get("/version", tags=["version"])
async def info():
    result = get_version()
    return {"version": result}


@app.post("/verify", tags=["verify"])
def verify_metadata(verify_input: VerifyInput):
    """
    Verifies ingested metadata by comparing the json from the source and
    destination dataverse to each other.

    :param verify_input: pydantinc basemodel
    :return:
    """
    source_response = get_dataverse_json(
        verify_input.dataverse_information.source_url,
        verify_input.dataverse_information.source_api_token,
        verify_input.doi
    )

    destination_response = get_dataverse_json(
        verify_input.dataverse_information.destination_url,
        verify_input.dataverse_information.destination_api_token,
        verify_input.doi
    )

    if source_response.ok and destination_response.ok:
        source_metadata = source_response.json()\
            ['data']['latestVersion']['metadataBlocks']['citation']['fields']
        destination_metadata = destination_response.json()\
            ['data']['latestVersion']['metadataBlocks']['citation']['fields']

        print(f"\n\n{source_metadata} \n\n")
        print(f"{destination_metadata} \n\n")

        result = compare_metadata(
            source_metadata,
            destination_metadata
        )

        if result is True:
            response = {"message": "Metadata matches."}
        else:
            msg = "Source and destination json do not match."
            response = HTTPException(
                status_code=422,
                detail=msg
            )

    else:
        msg = "Unable to retrieve json from source or destination dataverse."
        response = HTTPException(
            status_code=422,
            detail=msg
        )

    return response


def get_dataverse_json(base_url, api_token, doi):
    """
    Get metadata from a dataverse in json format.

    :param base_url: string, url to dataverse
    :param api_token: string, api for dataverse
    :param doi: string, identifier for dataverse record
    :return: json
    """
    headers = {'X-Dataverse-key': api_token}
    params = {'persistentId': doi}
    response = requests.get(
        url=f"{base_url}/api/datasets/:persistentId/",
        params=params,
        headers=headers
    )

    return response


def compare_metadata(source_metadata, destination_metadata):
    """
    Compare the source and destination metadata. These should match.

    :param source_metadata: list of dicts
    :param destination_metadata: list of dicts
    :return: bool
    """
    source_metadata = delete_unused_values(source_metadata)
    destination_metadata = delete_unused_values(destination_metadata)

    print(f"\n\n{source_metadata} \n\n")
    print(f"{destination_metadata} \n\n")

    return ordered(source_metadata) == ordered(destination_metadata)


def delete_unused_values(metadata):
    """
    Removes entire list of metadata that should not be used during comparison.
    For example, contact information will not match between the source and the
    destination.

    :param metadata: list
    :return: list
    """
    unused_keys = [
        "metadataLanguage",
        "datasetContact"
    ]

    new_list = []
    for count, dictionary in enumerate(metadata):
        if dictionary['typeName'] not in unused_keys:
            new_list.append(dictionary)

    return new_list


def ordered(obj):
    """
    This method makes sure that the order of items in the dicts and lists are
    the same.

    :param obj:
    :return: obj
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
