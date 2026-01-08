import streamlit as st
import database as db

# --------------------------------------------------
# Mockup UI for Case Study I
# UI-Only Mockup (no real business logic)
# --------------------------------------------------

st.set_page_config(page_title="Geräteverwaltung – Mockup", layout="wide")

# -------- Session State Placeholder --------
if "current_device" not in st.session_state:
    st.session_state.current_device = "CLETSCHI"

if "show_user_form" not in st.session_state:
    st.session_state.show_user_form = False

if "device_mode" not in st.session_state:
    st.session_state.device_mode = None  # None | "add" | "edit"

# -------- Sidebar Navigation --------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Bereich auswählen",
    [
        "Dashboard",
        "Geräteverwaltung",
        "Nutzerverwaltung",
        "Reservierungen (Mockup)",
        "Wartung (Mockup)",
    ],
)

# -------- Pages --------
if page == "Dashboard":
    st.title("Dashboard")
    st.info("Dies ist ein reines UI-Mockup ohne Funktionalität.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Anzahl Geräte", "12")
    col2.metric("Anzahl Nutzer", "5")
    col3.metric("Aktive Reservierungen", "3")

elif page == "Geräteverwaltung":
    st.title("Geräteverwaltung")

    # ---------------- Geräteliste ----------------
    results = db.read_table("device")

    st.subheader("Geräteliste (Platzhalter)")
    if results:
        st.table(
            {
                "Name": [d["name"] for d in results],
                "Status": [d["status"] for d in results],
                "Beschreibung": [d["description"] for d in results],
            }
        )
    else:
        st.info("Noch keine Geräte vorhanden.")

    # ---------------- Buttons (nebeneinander) ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Gerät anlegen"):
            st.session_state.device_mode = "add"
            st.rerun()

    with col2:
        if st.button("Gerät ändern"):
            st.session_state.device_mode = "edit"
            st.rerun()

    with col3:
        if st.button("Gerät löschen"):
            st.session_state.device_mode = "delete"
            st.rerun()

    st.divider()

    # ================= GERÄT ANLEGEN =================
    if st.session_state.device_mode == "add":
        st.subheader("Neues Gerät anlegen")

        name = st.text_input("Gerätename", key="add_name")
        status = st.selectbox(
            "Status",
            ["verfügbar", "reserviert", "in Wartung"],
            key="add_status",
        )
        description = st.text_area("Beschreibung", key="add_desc")

        if st.button("Gerät speichern"):
            if name.strip():
                db.safe_device(name.strip(), status, description.strip())
                st.success("Gerät wurde angelegt.")
                st.session_state.device_mode = None
                st.rerun()
            else:
                st.error("Bitte einen Gerätenamen eingeben.")

    # ================= GERÄT ÄNDERN =================
    elif st.session_state.device_mode == "edit":
        st.subheader("Gerät auswählen")

        if not results:
            st.warning("Keine Geräte vorhanden.")
            st.stop()

        selected_device = st.selectbox(
            "Vorhandene Geräte",
            options=results,
            format_func=lambda d: d.get("name", "Unbenannt"),
        )

        st.subheader("Gerätedetails bearbeiten")

        edit_name = st.text_input(
            "Gerätename",
            value=selected_device.get("name", ""),
            key="edit_name",
        )

        statuses = ["verfügbar", "reserviert", "in Wartung"]
        edit_status = st.selectbox(
            "Status",
            statuses,
            index=statuses.index(
                selected_device.get("status", "verfügbar")
            ),
            key="edit_status",
        )

        edit_description = st.text_area(
            "Beschreibung",
            value=selected_device.get("description", ""),
            key="edit_description",
        )

        if st.button("Änderungen speichern"):
            if edit_name.strip():
                db.update_device_by_doc_id(
                    selected_device.doc_id,
                    edit_name.strip(),
                    edit_status,
                    edit_description.strip(),
                )
                st.success("Änderungen wurden gespeichert.")
                st.session_state.device_mode = None
                st.rerun()
            else:
                st.error("Der Gerätename darf nicht leer sein.")

    # ================= GERÄT LÖSCHEN =================
    elif st.session_state.device_mode == "delete":
        st.subheader("Gerät löschen")

        if not results:
            st.warning("Keine Geräte zum Löschen vorhanden.")
            st.stop()

        selected_device = st.selectbox(
            "Zu löschendes Gerät auswählen",
            options=results,
            format_func=lambda d: d.get("name", "Unbenannt"),
        )

        st.warning(
            f"⚠️ Das Gerät **{selected_device.get('name')}** wird unwiderruflich gelöscht."
        )

        confirm = st.checkbox(
            "Ich bestätige, dass ich dieses Gerät löschen möchte."
        )

        if st.button("Gerät endgültig löschen"):
            if confirm:
                db.delete_device_by_doc_id(selected_device.doc_id)
                st.success("Gerät wurde gelöscht.")
                st.session_state.device_mode = None
                st.rerun()
            else:
                st.error("Bitte bestätige das Löschen mit der Checkbox.")

elif page == "Nutzerverwaltung":
    st.title("Nutzerverwaltung")

    # ---------------- Nutzerliste ----------------
    users = db.read_users()

    st.subheader("Nutzerliste")
    if users:
        st.table(
            {
                "Name": [u["name"] for u in users],
                "Rolle": [u["role"] for u in users],
            }
        )
    else:
        st.info("Noch keine Nutzer vorhanden.")

    # ---------------- Buttons ----------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Nutzer anlegen"):
            st.session_state.user_mode = "add"
            st.rerun()

    with col2:
        if st.button("Nutzer löschen"):
            st.session_state.user_mode = "delete"
            st.rerun()

    st.divider()

    # ================= NUTZER ANLEGEN =================
    if st.session_state.get("user_mode") == "add":
        st.subheader("Neuen Nutzer anlegen")

        name = st.text_input("Name", key="user_add_name")
        role = st.selectbox("Rolle", ["Admin", "User"], key="user_add_role")

        if st.button("Nutzer speichern"):
            if name.strip():
                db.save_user(name.strip(), role)
                st.success("Nutzer wurde angelegt.")
                st.session_state.user_mode = None
                st.rerun()
            else:
                st.error("Bitte einen Namen eingeben.")

    # ================= NUTZER LÖSCHEN =================
    elif st.session_state.get("user_mode") == "delete":
        st.subheader("Nutzer löschen")

        if not users:
            st.warning("Keine Nutzer zum Löschen vorhanden.")
            st.stop()

        selected_user = st.selectbox(
            "Zu löschenden Nutzer auswählen",
            options=users,
            format_func=lambda u: u.get("name", "Unbenannt"),
        )

        st.warning(
            f"⚠️ Der Nutzer **{selected_user.get('name')}** wird unwiderruflich gelöscht."
        )

        confirm = st.checkbox(
            "Ich bestätige, dass ich diesen Nutzer löschen möchte."
        )

        if st.button("Nutzer endgültig löschen"):
            if confirm:
                db.delete_user_by_doc_id(selected_user.doc_id)
                st.success("Nutzer wurde gelöscht.")
                st.session_state.user_mode = None
                st.rerun()
            else:
                st.error("Bitte bestätige das Löschen mit der Checkbox.")

elif page == "Reservierungen (Mockup)":
    st.title("Reservierungen")
    st.warning("Reservierungslogik wird in Case Study II umgesetzt.")

    st.selectbox("Gerät auswählen", ["Laptop", "Tablet", "Beamer"])
    st.selectbox("Nutzer auswählen", ["Max Mustermann", "Erika Musterfrau"])
    st.date_input("Startdatum")
    st.date_input("Enddatum")
    st.button("Reservierung anlegen (Mockup)")

elif page == "Wartung (Mockup)":
    st.title("Wartung")
    st.warning("Wartungsverwaltung ist noch nicht implementiert.")

    st.selectbox("Gerät auswählen", ["Laptop", "Tablet", "Beamer"])
    st.text_area("Wartungsbeschreibung")
    st.button("Wartung eintragen (Mockup)")
