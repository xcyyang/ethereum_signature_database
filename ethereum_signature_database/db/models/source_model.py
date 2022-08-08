import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ethereum_signature_database.db.base import Base


class Source(Base):
    """Model for source"""

    __tablename__ = "source"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String())
    network = Column(String(), nullable=True)
    address = Column(String(), nullable=True)
    url = Column(String(), nullable=True)
    original_function: UUID = Column(
        UUID,
        ForeignKey("function.id"),
        nullable=True,
    )
