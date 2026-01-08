from tinydb import TinyDB, Query

db = TinyDB('db.json')

# Geräteverwaltung
def safe_device(name, status, description):
    db.insert({'table': "device", 'name': name, 'status': status, 'description': description})

def read_table(table):
    Data = Query()
    return db.search(Data.table == table)

def get_device_by_doc_id(doc_id: int):
    return db.get(doc_id=doc_id)

def update_device_by_doc_id(doc_id: int, name: str, status: str, description: str):
    db.update(
        {'name': name, 'status': status, 'description': description},
        doc_ids=[doc_id]
    )

def delete_device_by_doc_id(doc_id: int):
    db.remove(doc_ids=[doc_id])

# Nutzerverwaltung
def save_user(name: str, role: str):
    db.insert({"table": "user", "name": name, "role": role})

def read_users():
    Data = Query()
    return db.search(Data.table == "user")

def delete_user_by_doc_id(doc_id: int):
    db.remove(doc_ids=[doc_id])

