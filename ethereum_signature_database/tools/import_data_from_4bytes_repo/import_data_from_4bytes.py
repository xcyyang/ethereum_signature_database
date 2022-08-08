import asyncio

import requests
from tqdm import tqdm

from ethereum_signature_database.db.dao.bytes4_dao import FunctionSignatureDAO
from ethereum_signature_database.db.dao.source_dao import SourceDao
from ethereum_signature_database.tools.database import get_db_session

LABEL = "4bytes"
URL = "https://github.com/ethereum-lists/4bytes/tree/master/signatures"
URL_TO_GET_FUNCTION = (
    "https://raw.githubusercontent.com/ethereum-lists/4bytes/master/signatures/"
)


async def main() -> None:
    # Establish session to database
    async_session = get_db_session()

    # Create source for 4bytes
    source_dao = SourceDao(async_session)
    if (
        len(
            await source_dao.query_source_model(
                label=LABEL,
                url=URL,
            ),
        )
        == 0
    ):
        print("Source not existed")
        await source_dao.create_source_model(
            label=LABEL,
            url=URL,
        )
    source_list = await source_dao.query_source_model(
        label=LABEL,
        url=URL,
    )
    source = source_list[0]

    # Import function to database
    function_signature_dao = FunctionSignatureDAO(async_session)

    with open("4bytes_list.txt", "r") as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        count = 30
        for i in tqdm(range(0, len(lines))):
            if count < 0:
                break
            count -= 1
            print(lines[i])
            function_signature_list_request = requests.get(
                URL_TO_GET_FUNCTION + lines[i],
            )
            for function_signature in function_signature_list_request.text.split(";"):
                await function_signature_dao.create_function_signature_without_checking_source(
                    function_name=function_signature,
                    return_type="Unknown",
                    source=source,
                )

    await async_session.close()


asyncio.run(main())
