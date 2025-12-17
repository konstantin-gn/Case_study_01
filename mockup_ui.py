import streamlit as st

# --------------------------------------------------
# Mockup UI for Case Study I
# UI-Only Mockup (no real business logic)
# --------------------------------------------------

st.set_page_config(page_title="Geräteverwaltung – Mockup", layout="wide")

# -------- Session State Placeholder --------
if "current_device" not in st.session_state:
    st.session_state.current_device = "Laptop"

if "device_mode" not in st.session_state:
    st.session_state.device_mode = None  # None | "add" | "edit"

# -------- Sidebar Navigation --------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Bereich auswählen",
    [
        "Geräteverwaltung",
        "Reservierungen (Mockup)",
    ],
)

# -------- Geräteverwaltung --------
if page == "Geräteverwaltung":
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

# -------- Reservierungen --------
elif page == "Reservierungen (Mockup)":
    st.title("Reservierungen")
    st.warning("Reservierungslogik wird in Case Study II umgesetzt.")

    st.selectbox("Gerät auswählen", ["Laptop", "Tablet", "Beamer"])
    st.selectbox("Nutzer auswählen", ["Max Mustermann", "Erika Musterfrau"])
    st.date_input("Startdatum")
    st.date_input("Enddatum")
    st.button("Reservierung anlegen (Mockup)")

