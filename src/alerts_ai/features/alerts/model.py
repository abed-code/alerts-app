
from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from alerts_ai.core.database import AppModel


class AlertStatus(StrEnum):
    PENDING = "pending"
    INVESTIGATING = "investigating"
    DONE = "done"


class AlertVerdict(StrEnum):
    TRUE_POSITIVE = "True Positive"
    FALSE_POSITIVE = "False Positive"
    NEED_INVESTIGATION = "Need Investigation"


def _values(enum_cls):
    # store the enum values ("True Positive"), not the member names (TRUE_POSITIVE)
    return [member.value for member in enum_cls]


class Alert(AppModel):
    __tablename__ = "alerts"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    verdict: Mapped[AlertVerdict] = mapped_column(
        Enum(AlertVerdict, name="alert_verdict", values_callable=_values),
        nullable=False,
    )
    severity: Mapped[int] = mapped_column(
        nullable=False,
    )
    # shortcut: free-text value, switch to Enum once the allowed values are fixed
    attack_outcome: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, name="alert_status", values_callable=_values),
        nullable=False,
    )
