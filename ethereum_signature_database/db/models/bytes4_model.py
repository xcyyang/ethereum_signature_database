import uuid
from typing import List

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import LargeBinary

from ethereum_signature_database.db.base import Base


class FunctionSignature(Base):
    """Model for function"""

    __tablename__ = "function"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    function_name = Column(String())
    return_type = Column(String())
    hex_signature = Column(String(length=8))
    bytes4_signature = Column(LargeBinary(4), ForeignKey("4bytes.bytes4_signature"))


class Bytes4Signature(Base):
    """Model for 4 bytes"""

    __tablename__ = "4bytes"

    bytes4_signature = Column(LargeBinary(4), primary_key=True)
    hex_signature = Column(String(length=8))
    function_signature: List[FunctionSignature] = relationship(
        "FunctionSignature",
        backref="4bytes",
    )
