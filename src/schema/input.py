from typing import Any
from pydantic import BaseModel, Field


class DataverseInformation(BaseModel):
    source_url: str = Field(example="https://portal.odissei.nl")
    source_api_token: str = Field(example="12345678-ab12-12ab-abcd-a1b2c3d4e5g6")
    destination_url: str = Field(example="https://portal.odissei.nl")
    destination_api_token: str = Field(example="12345678-ab12-12ab-abcd-a1b2c3d4e5g6")


class VerifyInput(BaseModel):
    doi: str = None
    dataverse_information: DataverseInformation
