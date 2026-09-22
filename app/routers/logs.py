from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_database
from app.models.log import Log
from app.repositories import log_repository
from app.schemas.log import LogCreate, LogLevel, LogResponse
from app.services import log_service


router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


@router.post(
    "",
    response_model=LogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_log(
    log_data: LogCreate,
    database: Session = Depends(get_database)
):
    return log_service.create_log(database, log_data)


@router.get(
    "/{log_id}",
    response_model=LogResponse
)
def get_log(
    log_id: str,
    database: Session = Depends(get_database)
) -> Log:
    existing_log = log_repository.get_log_by_id(
        database,
        log_id
    )

    if existing_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log '{log_id}' was not found"
        )

    return existing_log



@router.get(
    "",
    response_model=List[LogResponse],
    status_code=status.HTTP_200_OK
)
def get_logs(
    service_name: Optional[str] = None,
    level: Optional[LogLevel] = None,
    database: Session = Depends(get_database)
):
    return log_service.get_logs(
        database=database,
        service_name=service_name,
        level=level.value if level is not None else None
    )
