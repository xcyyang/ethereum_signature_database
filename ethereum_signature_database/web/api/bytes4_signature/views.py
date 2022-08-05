from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from ethereum_signature_database.db.dao.bytes4_dao import (
    Bytes4SignatureDAO,
    FunctionSignatureDAO,
)
from ethereum_signature_database.db.models.bytes4_model import (
    Bytes4Signature,
    FunctionSignature,
)
from ethereum_signature_database.web.api.bytes4_signature.schema import (
    Bytes4SignatureDTO,
    FunctionSignatureDTO,
    FunctionSignatureInputDTO,
)

router = APIRouter()


@router.get("/", response_model=List[Bytes4SignatureDTO])
async def get_4bytes_signature(
    limit: int = 10,
    offset: int = 0,
    bytes4_signature_dao: Bytes4SignatureDAO = Depends(),
) -> List[Bytes4Signature]:
    """
    Retrieve all 4 bytes signature objects from the database.

    :param limit: limit of 4 bytes signature objects, defaults to 10.
    :param offset: offset of 4 bytes signature objects, defaults to 0.
    :param bytes_signatures_dao: DAO for 4 bytes signature models.
    :return: list of 4 bytes signature obbjects from database.
    """
    return await bytes4_signature_dao.get_all_4bytes(limit=limit, offset=offset)


@router.get("/hex_signature", response_model=List[FunctionSignatureDTO])
async def get_functions_from_hex_signature(
    hex_signature: str,
    bytes4_signature_dao: Bytes4SignatureDAO = Depends(),
) -> List[FunctionSignature]:
    bytes4_list = await bytes4_signature_dao.get_4bytes_from_hex_signature(
        hex_signature=hex_signature,
    )

    if len(bytes4_list) == 0:
        return []

    return list(bytes4_list[0].function_signature)


@router.post("/function", response_model=FunctionSignatureDTO)
async def create_function_signature(
    function_signature_input: FunctionSignatureInputDTO,
    function_signature_dao: FunctionSignatureDAO = Depends(),
) -> FunctionSignature:

    function_signature = await function_signature_dao.create_function_signature_model(
        function_name=function_signature_input.function_name,
        return_type=function_signature_input.return_type,
    )

    return function_signature
