import streamlit as st

# --------------------------------------------------
# Mockup UI for Case Study I
# UI-Only Mockup (no real business logic)
# --------------------------------------------------

st.set_page_config(page_title="Geräteverwaltung – Mockup", layout="wide")

# -------- Session State Placeholder --------
if "current_device" not in st.session_state:
    st.session_state.current_device = "Laptop"

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

    devices = ["Laptop", "Tablet", "Beamer"]

    st.subheader("Geräteliste (Platzhalter)")
    st.table(
        {
            "Geräte-ID": ["G-001", "G-002", "G-003"],
            "Name": devices,
            "Status": ["verfügbar", "reserviert", "in Wartung"],
        }
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Gerät anlegen"):
            st.session_state.device_mode = "add"

    with col2:
        if st.button("Gerät ändern"):
            st.session_state.device_mode = "edit"

    if st.session_state.device_mode == "add":
        st.subheader("Neues Gerät anlegen")
        st.text_input("Gerätename")
        st.selectbox("Status", ["verfügbar", "reserviert", "in Wartung"])
        st.text_area("Beschreibung")
        st.button("Gerät speichern (Mockup)")

    if st.session_state.device_mode == "edit":
        st.subheader("Gerät auswählen")
        selected_device = st.selectbox(
            "Vorhandene Geräte",
            devices,
            index=devices.index(st.session_state.current_device),
        )
        st.session_state.current_device = selected_device

        st.subheader("Gerätedetails bearbeiten")
        st.text_input("Gerätename", st.session_state.current_device)
        st.selectbox("Status", ["verfügbar", "reserviert", "in Wartung"])
        st.text_area("Beschreibung", "Platzhalter-Beschreibung")
        st.button("Änderungen speichern (Mockup)")

elif page == "Nutzerverwaltung":
    st.title("Nutzerverwaltung")

    st.subheader("Nutzerliste (Platzhalter)")
    st.table(
        {
            "Nutzer-ID": ["U-001", "U-002"],
            "Name": ["Max Mustermann", "Erika Musterfrau"],
            "Rolle": ["Admin", "User"],
        }
    )

    if st.button("Nutzer anlegen"):
        st.session_state.show_user_form = True

    if st.session_state.show_user_form:
        st.subheader("Neuen Nutzer anlegen")
        st.text_input("Name")
        st.selectbox("Rolle", ["Admin", "User"])
        st.button("Nutzer speichern (Mockup)")

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
