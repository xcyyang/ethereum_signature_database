from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ethereum_signature_database.db.dao.source_dao import SourceDao
from ethereum_signature_database.db.dependencies import get_db_session
from ethereum_signature_database.db.models.bytes4_model import (
    Bytes4Signature,
    FunctionSignature,
)
from ethereum_signature_database.db.models.source_model import Source
from ethereum_signature_database.utils.abi import make_4byte_signature
from ethereum_signature_database.utils.encoding import (
    encode_hex,
    force_text,
    remove_0x_prefix,
)


class Bytes4SignatureDAO:
    """Class for accessing 4bytes table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_hex_signature(self, hex_signature: str) -> None:
        """
        Add single 4bytes signatures to session

        :param hex_signature: 4 bytes signature
        """
        # hex_signature_bytes = force_bytes(hex_signature)
        # print(bytes4_signature_bytes)
        # print(encode_hex(bytes4_signature_bytes))
        # print(remove_0x_prefix(encode_hex(bytes4_signature_bytes)))
        self.session.add(
            Bytes4Signature(
                hex_signature=force_text(
                    remove_0x_prefix(hex_signature),
                ),
            ),
        )

    async def get_all_hex_signatures(
        self,
        limit: int,
        offset: int,
    ) -> List[Bytes4Signature]:
        """
        Get all 4 bytes signatures with limit/offset pagination.

        :param limit: limit of bytes signatures.
        :param offset: offset of bytes signatures.
        :return: stream of bytes signatures.
        """
        raw_bytes4 = await self.session.execute(
            select(Bytes4Signature).limit(limit).offset(offset),
        )
        return raw_bytes4.scalars().fetchall()

    async def query_hex_signature(
        self,
        hex_signature: str,
    ) -> Bytes4Signature:

        statement = select(Bytes4Signature).filter_by(hex_signature=hex_signature)
        result = await self.session.execute(statement)
        return result.scalars().fetchall()

    async def get_hex_signature_and_functions(
        self,
        hex_signature: str,
    ) -> List[Bytes4Signature]:
        """
        Get 4 bytes signatures from hex signature string

        :param hex_signature: hex signature string
        :return: Bytes4Signature
        """
        raw_bytes4 = await self.session.execute(
            select(Bytes4Signature)
            .filter_by(hex_signature=force_text(remove_0x_prefix(hex_signature)))
            .options(selectinload(Bytes4Signature.function_signature)),
        )
        return raw_bytes4.scalars().fetchall()


class FunctionSignatureDAO:
    """Class for accessing Function Signature"""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_function_signature_model_from_api(
        self,
        function_name: str,
    ) -> FunctionSignature:
        """
        Add single function signatures to session

        :param function_name: string of function name with types of parameters
        :param return_type: string of return type
        :return: FunctionSignature
        """
        source_dao = SourceDao(self.session)
        bytes4_signature_dao = Bytes4SignatureDAO(self.session)

        function_signature_list = await self.query_function_signature(
            function_name=function_name,
        )
        if len(function_signature_list) > 0:
            function_signature = function_signature_list[0]
            return function_signature_list[0]

        bytes4_signature = make_4byte_signature(function_name)
        hex_signature = force_text(remove_0x_prefix(encode_hex(bytes4_signature)))

        if (
            len(
                await bytes4_signature_dao.query_hex_signature(
                    hex_signature=hex_signature,
                ),
            )
            == 0
        ):
            bytes4 = Bytes4Signature(
                hex_signature=hex_signature,
            )
            self.session.add(bytes4)

        source_list = await source_dao.query_source_model(label="api")
        source = None
        if len(source_list) == 0:
            source = Source(label="api")
            self.session.add(source)
        else:
            source = source_list[0]

        function_signature = FunctionSignature(
            function_name=function_name,
            hex_signature=hex_signature,
        )
        function_signature.source.append(source)
        self.session.add(function_signature)

        await self.session.commit()

        return function_signature

    async def query_function_signature(
        self,
        function_name: str,
    ) -> List[FunctionSignature]:

        statement = select(FunctionSignature).filter_by(
            function_name=function_name,
        )
        result = await self.session.execute(statement)
        return result.scalars().fetchall()

    async def get_sources_of_function(
        self,
        function_name: str,
    ) -> List[FunctionSignature]:

        statement = (
            select(FunctionSignature)
            .filter_by(
                function_name=function_name,
            )
            .options(selectinload(FunctionSignature.source))
        )

        result = await self.session.execute(statement)
        return result.scalars().fetchall()
