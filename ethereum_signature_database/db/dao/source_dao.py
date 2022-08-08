from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ethereum_signature_database.db.dependencies import get_db_session
from ethereum_signature_database.db.models.source_model import Source


class SourceDao:
    """Class for accessing source table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_source_model(
        self,
        label: str,
        network: str = None,
        address: str = None,
        url: str = None,
        original_function: str = None,
    ) -> None:
        """
        Add single source to session

        :param label: the type of source (mainnet/mutation/github/certik/4bytes/api)
        :param network: the network of source (eth/bsc)
        :param address: the address of source (0x1234...)
        :param url: the url to source contract (https://...)
        :param original_function: the uuid of original function, if this function is mutated from other function
        """
        self.session.add(
            Source(
                label=label,
                network=network,
                address=address,
                url=url,
                original_function=original_function,
            ),
        )

    async def query_source_model(
        self,
        label: str,
        network: str = None,
        address: str = None,
        url: str = None,
        original_function: str = None,
    ) -> List[Source]:

        statement = select(Source).filter_by(
            label=label,
            network=network,
            address=address,
            url=url,
            original_function=original_function,
        )
        result = await self.session.execute(statement)
        return result.scalars().fetchall()
