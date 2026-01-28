from datetime import date
from typing import Self
from serializable import Serializable
from database import DatabaseConnector

class Reservation(Serializable):

    db_connector = DatabaseConnector().get_table("reservations")

    def __init__(
        self,
        id: str,
        device_id: str,
        user_id: str,
        start_date: date,
        end_date: date,
        creation_date=None,
        last_update=None
    ):
        super().__init__(id, creation_date, last_update)
        self.device_id = device_id
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(
            data["id"],
            data["device_id"],
            data["user_id"],
            data["start_date"],
            data["end_date"],
            data["creation_date"],
            data["last_update"],
        )

    def __str__(self):
        return f"Reservation {self.id}: {self.device_id} by {self.user_id}"
