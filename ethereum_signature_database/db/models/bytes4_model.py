import uuid
from typing import List

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import LargeBinary

from ethereum_signature_database.db.base import Base
from ethereum_signature_database.db.models.source_model import Source

association_table_for_function_and_source = Table(
    "function_source",
    Base.metadata,
    Column("function_signature_id", ForeignKey("function.id")),
    Column("source_id", ForeignKey("source.id")),
)


class FunctionSignature(Base):
    """Model for function"""

    __tablename__ = "function"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    function_name = Column(String())
    return_type = Column(String())
    hex_signature = Column(String(length=8))
    bytes4_signature = Column(LargeBinary(4), ForeignKey("4bytes.bytes4_signature"))
    source: List[Source] = relationship(
        "Source",
        secondary=association_table_for_function_and_source,
        backref="functions",
    )


class Bytes4Signature(Base):
    """Model for 4 bytes"""

    __tablename__ = "4bytes"

    bytes4_signature = Column(LargeBinary(4), primary_key=True)
    hex_signature = Column(String(length=8))
    function_signature: List[FunctionSignature] = relationship(
        "FunctionSignature",
        backref="4bytes",
    )
