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
from ethereum_signature_database.db.models.source_model import Source
from ethereum_signature_database.web.api.bytes4_signature.schema import (
    Bytes4SignatureDTO,
    FunctionSignatureDTO,
    FunctionSignatureInputDTO,
    SourceDTO,
)

router = APIRouter()


@router.get("/", response_model=List[Bytes4SignatureDTO])
async def get_all_hex_signatures(
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
    return await bytes4_signature_dao.get_all_hex_signatures(limit=limit, offset=offset)


@router.get("/hex_signature", response_model=List[FunctionSignatureDTO])
async def get_functions_from_hex_signature(
    hex_signature: str,
    bytes4_signature_dao: Bytes4SignatureDAO = Depends(),
) -> List[FunctionSignature]:

    bytes4_list = await bytes4_signature_dao.get_hex_signature_and_functions(
        hex_signature=hex_signature,
    )
    if len(bytes4_list) == 0:
        return []
    return list(bytes4_list[0].function_signature)


@router.get("/sources", response_model=List[SourceDTO])
async def get_sources_of_function(
    function_name: str,
    function_signature_dao: FunctionSignatureDAO = Depends(),
) -> List[Source]:

    function_signature_list = await function_signature_dao.get_sources_of_function(
        function_name=function_name,
    )
    if len(function_signature_list) == 0:
        return []
    print(function_signature_list[0].source)
    return list(function_signature_list[0].source)


@router.post("/function", response_model=FunctionSignatureDTO)
async def create_function_signature(
    function_signature_input: FunctionSignatureInputDTO,
    function_signature_dao: FunctionSignatureDAO = Depends(),
) -> FunctionSignature:

    function_signature = (
        await function_signature_dao.create_function_signature_model_from_api(
            function_name=function_signature_input.function_name,
        )
    )

    return function_signature
