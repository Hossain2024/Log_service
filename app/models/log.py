from sqlalchemy import Column, DateTime, String

from app.database import Base


class Log(Base):
    __tablename__ = "logs"

    log_id = Column(
        String(100),
        primary_key=True,
        index=True
    )

    service_name = Column(
        String(100),
        nullable=False,
        index=True
    )

    level = Column(
        String(20),
        nullable=False,
        index=True
    )

    message = Column(
        String(1000),
        nullable=False
    )

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )