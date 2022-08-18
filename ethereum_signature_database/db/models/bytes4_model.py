from typing import List

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import String

from ethereum_signature_database.db.base import Base
from ethereum_signature_database.db.models.source_model import Source

association_table_for_function_and_source = Table(
    "function_source",
    Base.metadata,
    Column("function_name", ForeignKey("function.function_name")),
    Column("source_id", ForeignKey("source.id")),
)


class FunctionSignature(Base):
    """Model for function"""

    __tablename__ = "function"

    function_name = Column(String(), primary_key=True)
    hex_signature = Column(String(length=8), ForeignKey("4bytes.hex_signature"))
    source: List[Source] = relationship(
        "Source",
        secondary=association_table_for_function_and_source,
        backref="functions",
    )


class Bytes4Signature(Base):
    """Model for 4 bytes"""

    __tablename__ = "4bytes"

    hex_signature = Column(String(length=8), primary_key=True)
    function_signature: List[FunctionSignature] = relationship(
        "FunctionSignature",
        backref="4bytes",
    )
