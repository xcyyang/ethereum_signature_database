from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


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

    id: UUID = Field(default_factory=uuid4)
    function_name: str
    return_type: str
    bytes4_signature: bytes
    hex_signature: str

    _convert_bytes = validator(
        "bytes4_signature",
        allow_reuse=True,
    )(convert_bytes_to_string)

    class Config:
        orm_mode = True


class FunctionSignatureInputDTO(BaseModel):
    """DTO for creating new function signature."""

    function_name: str
    return_type: str


class Bytes4SignatureDTO(BaseModel):
    """
    DTO for 4bytes signature.

    It returned when accessing 4bytes signature from the API.
    """

    bytes4_signature: bytes
    hex_signature: str

    _convert_bytes = validator(
        "bytes4_signature",
        allow_reuse=True,
    )(convert_bytes_to_string)

    class Config:
        orm_mode = True
