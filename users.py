import os
from tinydb import TinyDB, Query


class User:
    # Gemeinsame DB-Verbindung für alle User
    db_connector = TinyDB(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
    ).table('users')

    # Benutzerattribute
    def __init__(self, id: str, name: str) -> None:
        self.id = id # E-Mail
        self.name = name # Name 

    # Speichern des Benutzers in der DB
    def store_data(self) -> None:
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.id == self.id)

        # bestehenden Nutzer aktualisieren
        if result:
            self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
        
        # neuen Nutzer anlegen
        else:
            self.db_connector.insert(self.__dict__)


    # Nutzer löschen
    def delete(self) -> None:
        UserQuery = Query()
        self.db_connector.remove(UserQuery.id == self.id)

    # Darstellungsmethoden
    def __str__(self) -> str:
        return f"User {self.id} - {self.name}"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def find_all() -> list:
        
        # Alle Nutzer laden
        result = User.db_connector.all()
        return [User(x["id"], x["name"]) for x in result]

    @classmethod
    def find_by_attribute(cls, attribute: str, value: str) -> "User | None":
        # Nach Nutzer anhand eines Attributs suchen
        UserQuery = Query()
        result = cls.db_connector.search(
            getattr(UserQuery, attribute) == value
        )

        if result:
            data = result[0]
            return cls(data["id"], data["name"])
        return None