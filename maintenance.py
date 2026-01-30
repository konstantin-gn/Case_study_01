from datetime import date
from typing import Self

from serializable import Serializable
from database import DatabaseConnector


class Maintenance(Serializable):
    """Represents a maintenance window for a device."""

    db_connector = DatabaseConnector().get_table("maintenances")

    def __init__(
        self,
        id: str,
        device_id: str,
        description: str,
        start_date: date,
        end_date: date,
        creation_date=None,
        last_update=None,
    ):
        super().__init__(id, creation_date, last_update)
        self.device_id = device_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(
            data["id"],
            data["device_id"],
            data.get("description", ""),
            data["start_date"],
            data["end_date"],
            data.get("creation_date"),
            data.get("last_update"),
        )

    def __str__(self):
        return f"Maintenance {self.id}: {self.device_id} ({self.start_date} - {self.end_date})"
