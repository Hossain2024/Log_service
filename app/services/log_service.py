from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import log_repository
from app.schemas.log import LogCreate
from app.models.log import Log


def create_log(
    database: Session,
    log_data: LogCreate
) -> Log:
    existing_log = log_repository.get_log_by_id(
        database,
        log_data.log_id
    )

    if existing_log is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Log '{log_data.log_id}' already exists"
        )

    try:
        return log_repository.create_log(database, log_data)

    except IntegrityError:
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Log '{log_data.log_id}' already exists"
        )
    