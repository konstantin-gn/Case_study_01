import streamlit as st
from users import User
from devices import Device
from reservation import Reservation
from maintenance import Maintenance



# --------------------------------------------------
# Mockup UI for Case Study I
# UI-Only Mockup (no real business logic)
# --------------------------------------------------

st.set_page_config(page_title="Geräteverwaltung – Mockup", layout="wide")

# -------- Session State Placeholder --------
if "user_mode" not in st.session_state:
    st.session_state.user_mode = None  # None | "add" | "delete"

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
        "Reservierungen",
        "Wartung",
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
    devices = Device.find_all()

    st.subheader("Geräteliste")

    if devices:
        st.table({
            "Geräte-ID": [d.id for d in devices],
            "Verwaltet von": [d.managed_by_user_id for d in devices],
            "Aktiv": [d.is_active for d in devices],
            "End of Life": [d.end_of_life for d in devices],
        })
    else:
        st.info("Noch keine Geräte vorhanden.")
    # ---------------- Buttons (nebeneinander) ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Gerät anlegen"):
            st.session_state.device_mode = "add"
            st.rerun()


    with col3:
        if st.button("Gerät löschen"):
            st.session_state.device_mode = "delete"
            st.rerun()

    st.divider()

    # ================= GERÄT ANLEGEN =================
    
    if st.session_state.get("device_mode") == "add":
        st.subheader("Neues Gerät anlegen")

        device_id = st.text_input("Geräte-ID")
        users = User.find_all()

        managed_by = st.selectbox(
            "Verantwortlicher Nutzer",
            options=users,
            format_func=lambda u: f"{u.name} ({u.id})"
        )

        if st.button("Gerät speichern"):
            if device_id.strip():
                device = Device(
                    id=device_id.strip(),
                    managed_by_user_id=managed_by.id
                )
                device.store_data()
                st.success("Gerät wurde angelegt.")
                st.rerun()
            else:
                st.error("Bitte eine Geräte-ID eingeben.")


    # ================= GERÄT LÖSCHEN =================
    elif st.session_state.get("device_mode") == "delete":
        st.subheader("Gerät löschen")

        devices = Device.find_all()

        selected_device = st.selectbox(
            "Gerät auswählen",
            options=devices,
            format_func=lambda d: d.id
        )

        st.warning(
            f" Das Gerät **{selected_device.id}** wird unwiderruflich gelöscht."
        )

        confirm = st.checkbox(
            "Ich bestätige, dass ich dieses Gerät löschen möchte."
        )

        if st.button("Gerät endgültig löschen"):
            if confirm:
                selected_device.delete()
                st.success("Gerät wurde gelöscht.")
                st.session_state.device_mode = None
                st.rerun()
            else:
                st.error("Bitte bestätige das Löschen mit der Checkbox.")



    # ---------------- Nutzerliste ----------------
elif page == "Nutzerverwaltung":
    st.title("Nutzerverwaltung")
    users = User.find_all()

    st.subheader("Nutzerliste")
    if users:
        st.table(
            {
                "Name": [u.name for u in users],
                "E-mail": [u.id for u in users],
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

        name = st.text_input("Name")
        email = st.text_input("E-Mail")

        if st.button("Nutzer speichern"):
            if name.strip() and email.strip():
                user = User(
                    id=email.strip().lower(),
                    name=name.strip()
                )
                user.store_data()

                st.success("Nutzer wurde angelegt.")
                st.session_state.user_mode = None
                st.rerun()
            else:
                st.error("Name und E-Mail müssen ausgefüllt sein.")

    # ================= NUTZER LÖSCHEN =================
    elif st.session_state.get("user_mode") == "delete":
        st.subheader("Nutzer löschen")

        if not users:
            st.warning("Keine Nutzer zum Löschen vorhanden.")
            st.stop()

        selected_user = st.selectbox(
            "Zu löschenden Nutzer auswählen",
            options=users,
            format_func=lambda u: f"{u.name} ({u.id})",
        )

        st.warning(
            f" Der Nutzer **{selected_user.name}** wird unwiderruflich gelöscht."
        )

        confirm = st.checkbox(
            "Ich bestätige, dass ich diesen Nutzer löschen möchte."
        )

        if st.button("Nutzer endgültig löschen"):
            if confirm:
                selected_user.delete()
                st.success("Nutzer wurde gelöscht.")
                st.session_state.user_mode = None
                st.rerun()
            else:
                st.error("Bitte bestätige das Löschen mit der Checkbox.")


# ================= RESERVIERUNGEN =================
if "reservation_mode" not in st.session_state:
    st.session_state.reservation_mode = None  # None | "add" | "delete"
if "maintenance_mode" not in st.session_state:
    st.session_state.maintenance_mode = None  # None | "add" | "delete"

elif page == "Reservierungen":
    st.title("Reservierungen")
    
    reservations = Reservation.find_all()
    devices = Device.find_all()
    users = User.find_all()

    st.subheader("Aktive Reservierungen")

    if reservations:
        st.table({
            "Nutzer": [r.user_id for r in reservations],
            "Gerät": [r.device_id for r in reservations],
            "Startdatum": [r.start_date for r in reservations],
            "Enddatum": [r.end_date for r in reservations],
        })
    else:
        st.info("Noch keine Reservierungen vorhanden.")

    # ---------------- Buttons (nebeneinander) ----------------    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reservierung anlegen"):
            st.session_state.reservation_mode = "add"
            st.rerun()

    with col2:
        if st.button("Reservierung löschen"):
            st.session_state.reservation_mode = "delete"
            st.rerun()

    st.divider()

    # ================= RESERVIERUNG ANLEGEN =================

    if st.session_state.reservation_mode == "add":
        st.subheader("Neue Reservierung anlegen")

        selected_device = st.selectbox(
            "Gerät auswählen",
            options=devices,
            format_func=lambda d: d.id
        )

        selected_user = st.selectbox(
            "Nutzer auswählen",
            options=users,
            format_func=lambda u: f"{u.name} ({u.id})"
        )

        start_date = st.date_input("Startdatum")
        end_date = st.date_input("Enddatum")

        if st.button("Reservierung speichern"):
            if start_date > end_date:
                st.error("Enddatum muss nach dem Startdatum liegen.")
            else:
                reservation = Reservation(
                    id=f"{selected_device.id}-{start_date}",
                    device_id=selected_device.id,
                    user_id=selected_user.id,
                    start_date=start_date,
                    end_date=end_date,
                )
                reservation.store_data()

                st.success("Reservierung wurde angelegt.")
                st.session_state.reservation_mode = None
                st.rerun()

    # ================= RESERVIERUNG LÖSCHEN =================

    elif st.session_state.reservation_mode == "delete":
        st.subheader("Reservierung löschen")

    selected_reservation = st.selectbox(
        "Reservierung auswählen",
        options=reservations,
        format_func=lambda r: f"{r.device_id} | {r.start_date} – {r.end_date}"
    )

    confirm = st.checkbox("Ich bestätige das Löschen")

    if st.button("Reservierung entgültig löschen"):
        if confirm:
            selected_reservation.delete()
            st.success("Reservierung gelöscht.")
            st.session_state.reservation_mode = None
            st.rerun()
        else:
            st.error("Bitte bestätige das Löschen.")



# ================= WARTUNG =================
if page == "Wartung":
    st.title("Wartung")

    maintenances = Maintenance.find_all()
    devices = Device.find_all()

    st.subheader("Eingetragene Wartungen")

    if maintenances:
        st.table({
            "Gerät": [m.device_id for m in maintenances],
            "Beschreibung": [m.description for m in maintenances],
            "Startdatum": [m.start_date for m in maintenances],
            "Enddatum": [m.end_date for m in maintenances],
        })
    else:
        st.info("Noch keine Wartungen vorhanden.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Wartung anlegen"):
            st.session_state.maintenance_mode = "add"
            st.rerun()

    with col2:
        if st.button("Wartung löschen"):
            st.session_state.maintenance_mode = "delete"
            st.rerun()

    st.divider()

    # ================= WARTUNG ANLEGEN =================
    if st.session_state.maintenance_mode == "add":
        st.subheader("Neue Wartung anlegen")

        selected_device = st.selectbox(
            "Gerät auswählen",
            options=devices,
            format_func=lambda d: d.id
        )

        description = st.text_area("Wartungsbeschreibung")
        start_date = st.date_input("Startdatum")
        end_date = st.date_input("Enddatum")

        if st.button("Wartung speichern"):
            if start_date > end_date:
                st.error("Enddatum muss nach dem Startdatum liegen.")
            elif not description.strip():
                st.error("Bitte eine Wartungsbeschreibung eingeben.")
            else:
                maintenance = Maintenance(
                    id=f"{selected_device.id}-{start_date}",
                    device_id=selected_device.id,
                    description=description.strip(),
                    start_date=start_date,
                    end_date=end_date,
                )
                maintenance.store_data()

                st.success("Wartung wurde angelegt.")
                st.session_state.maintenance_mode = None
                st.rerun()

    # ================= WARTUNG LÖSCHEN =================
    elif st.session_state.maintenance_mode == "delete":
        st.subheader("Wartung löschen")

        selected_maintenance = st.selectbox(
            "Wartung auswählen",
            options=maintenances,
            format_func=lambda m: f"{m.device_id} | {m.start_date} – {m.end_date}"
        )

        confirm = st.checkbox("Ich bestätige das Löschen")

        if st.button("Wartung endgültig löschen"):
            if confirm:
                selected_maintenance.delete()
                st.success("Wartung gelöscht.")
                st.session_state.maintenance_mode = None
                st.rerun()
            else:
                st.error("Bitte bestätige das Löschen.")
