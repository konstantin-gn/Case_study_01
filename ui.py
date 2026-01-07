import streamlit as st
from users import User


st.title("Nutzerverwaltung")

# Nutzer laden
users = User.find_all()

st.subheader("Vorhandene Nutzer")
#Nutzer in Tabelle anzeigen
if users:
    st.table(
        {
            "E-Mail (ID)": [u.id for u in users],
            "Name": [u.name for u in users],
        }
    )
else:
    st.info("Noch keine Nutzer in der Datenbank.")


# Nutzer anlegen
st.subheader("Neuen Nutzer anlegen")

with st.form("create_user_form"):
    user_id = st.text_input("E-Mail-Adresse (ID)")
    user_name = st.text_input("Name")

    submitted = st.form_submit_button("Nutzer speichern")

    if submitted:
        if not user_id or not user_name:
            st.error("Bitte alle Felder ausfüllen.")
        else:
            existing_user = User.find_by_attribute("ID", user_id)
            if existing_user:
                st.error("Dieser Nutzer existiert bereits.")
            else:
                new_user = User(user_id, user_name)
                new_user.store_data()
                st.success("Nutzer erfolgreich angelegt.")
                st.rerun()


# Nutzer löschen
st.subheader("Nutzer löschen")

if users:
    user_to_delete = st.selectbox(
        "Nutzer auswählen",
        options=[u.id for u in users]
    )

    if st.button("Nutzer löschen"):
        user_obj = User.find_by_attribute("ID", user_to_delete)
        if user_obj:
            user_obj.delete()
            st.success("Nutzer gelöscht.")
            st.rerun()
else:
    st.info("Keine Nutzer zum Löschen vorhanden.")