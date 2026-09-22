from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.log import Log
from app.schemas.log import LogCreate


def get_log_by_id(
    database: Session,
    log_id: str
) -> Optional[Log]:
    return (
        database.query(Log)
        .filter(Log.log_id == log_id)
        .first()
    )
def get_logs(
    database: Session,
    service_name: Optional[str] = None,
    level: Optional[str] = None
) -> List[Log]:
    query = database.query(Log)

    if service_name is not None:
        query = query.filter(
            Log.service_name == service_name
        )

    if level is not None:
        query = query.filter(
            Log.level == level
        )

    return (
        query
        .order_by(Log.timestamp.desc())
        .all()
    )

def create_log(
    database: Session,
    log_data: LogCreate
) -> Log:
    new_log = Log(
        log_id=log_data.log_id,
        service_name=log_data.service_name,
        level=log_data.level.value,
        message=log_data.message,
        timestamp=log_data.timestamp
    )

    database.add(new_log)
    database.commit()
    database.refresh(new_log)

    return new_log