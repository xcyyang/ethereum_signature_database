from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def convert_bytes_to_string(bytes_input: bytes) -> str:
    return bytes_input.decode("utf-16")


class SourceDTO(BaseModel):
    """DTO for source"""

    id: UUID = Field(default_factory=uuid4)
    label: str
    network: Optional[str] = ""
    address: Optional[str] = ""
    url: Optional[str] = ""
    original_function: Optional[UUID] = Field(default_factory=uuid4)

    class Config:
        orm_mode = True


class FunctionSignatureDTO(BaseModel):
    """DTO for function signature"""

    function_name: str
    hex_signature: str

    class Config:
        orm_mode = True


class FunctionSignatureInputDTO(BaseModel):
    """DTO for creating new function signature."""

    function_name: str


class Bytes4SignatureDTO(BaseModel):
    """
    DTO for 4bytes signature.

    It returned when accessing 4bytes signature from the API.
    """

    hex_signature: str

    class Config:
        orm_mode = True
