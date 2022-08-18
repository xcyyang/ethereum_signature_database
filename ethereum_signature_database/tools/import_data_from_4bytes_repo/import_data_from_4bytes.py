import asyncio
from io import StringIO

import psycopg2
from tqdm import tqdm

from ethereum_signature_database.db.models.bytes4_model import FunctionSignature
from ethereum_signature_database.db.models.source_model import Source
from ethereum_signature_database.settings import settings
from ethereum_signature_database.tools.database import get_db_session

LABEL = "4bytes"
URL = "https://github.com/ethereum-lists/4bytes/tree/master/signatures"
URL_TO_GET_FUNCTION = (
    "https://raw.githubusercontent.com/ethereum-lists/4bytes/master/signatures/"
)


async def main() -> None:
    # Establish connection
    async_session = get_db_session()

    conn = psycopg2.connect(
        host=settings.db_host,
        database=settings.db_base,
        user=settings.db_user,
        password=settings.db_pass,
        port=settings.db_port,
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Read the 4bytes_list.txt and insert 4bytes
    # Cannot ignure duplicate one
    # TODO: Stage table could be a solution

    with open("4bytes_list.txt", "r") as file:
        lines = file.readlines()
        bytes4_list = ""
        for line in lines:
            bytes4_list += line.split()[0] + "\n"

    stringIO = StringIO(bytes4_list)
    cur.copy_from(stringIO, "4bytes")
    conn.commit()

    # Insert source

    source = Source(label=LABEL, url=URL)
    async_session.add(source)

    # Insert function
    function_signature_list = []
    for i in tqdm(range(0, len(lines))):

        function_name_list = lines[i].split()[1]
        for function_name in function_name_list.split(";"):

            function_signature = FunctionSignature(
                function_name=function_name,
                hex_signature=lines[i].split()[0],
            )

            function_signature.source.append(source)
            function_signature_list.append(function_signature)

    async_session.add_all(function_signature_list)
    await async_session.commit()
    return None


asyncio.run(main())
