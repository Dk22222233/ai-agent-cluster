# app/agent/core/context.py

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import Session


@dataclass(frozen=True)
class ExecutionContext:
    user_id: UUID
    db: Session