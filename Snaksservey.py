import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Forgokul Snaks – Outlet Survey",
    page_icon="🍟",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Header banner */
.banner {
    background: linear-gradient(135deg, #ff6b00 0%, #ff9f00 100%);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 24px rgba(255,107,0,0.30);
}
.banner h1 { font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.banner p  { font-size: 1rem; margin: 6px 0 0; opacity: 0.92; }

/* Section card */
.card {
    background: #fff7f0;
    border-left: 5px solid #ff6b00;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 18px;
}
.card-title {
    font-weight: 600;
    color: #c94e00;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

/* Submit button override */
div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #ff6b00, #ff9f00) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 12px 36px !important;
    font-size: 1rem !important;
}

/* Download button */
.stDownloadButton > button {
    background: #222 !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 10px 28px !important;
}
.stDownloadButton > button:hover {
    background: #ff6b00 !important;
}

/* Table header */
thead tr th {
    background-color: #ff6b00 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── Banner ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner">
  <h1>🍟 Forgokul Snaks</h1>
  <p>Outlet Survey — Field Data Collection Form</p>
</div>
""", unsafe_allow_html=True)

# ── Session state: data store ─────────────────────────────────────────────────
if "survey_data" not in st.session_state:
    st.session_state.survey_data = []

# ── Helper: auto Sr No ───────────────────────────────────────────────────────
def next_sr():
    return len(st.session_state.survey_data) + 1

# ── Form ──────────────────────────────────────────────────────────────────────
st.markdown("### 📋 Add Outlet Entry")

with st.form("survey_form", clear_on_submit=True):

    st.markdown('<div class="card"><div class="card-title">Outlet Information</div>', unsafe_allow_html=True)
    col0, col0b = st.columns(2)
    with col0:
        survey_date = st.date_input("Date *", value=datetime.date.today())
    col1, col2 = st.columns(2)
    with col1:
        outlet_name = st.text_input("Outlet Name *", placeholder="e.g. Sharma General Store")
    with col2:
        outlet_mobile = st.text_input("Outlet Mobile No *", placeholder="e.g. 9876543210", max_chars=15)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Outlet Classification</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        outlet_type = st.selectbox(
            "Outlet Type *",
            ["-- Select --", "Kirana / General Store", "Supermarket", "Convenience Store",
             "Hotel / Restaurant", "Dhaba", "Canteen", "Medical Store", "Petrol Pump Outlet",
             "Pan / Cigarette Shop", "Other"],
        )
    with col4:
        outlet_class = st.selectbox(
            "Outlet Class *",
            ["-- Select --", "A", "B", "C", "D"],
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Location Details</div>', unsafe_allow_html=True)
    location = st.text_input("Location *", placeholder="e.g. Main Market, Gandhi Chowk")
    col5, col6 = st.columns(2)
    with col5:
        sub_city = st.text_input("Sub-City", placeholder="e.g. Andheri East")
    with col6:
        sub_village = st.text_input("Sub-Village", placeholder="e.g. Ghatkopar Village")
    outlet_address = st.text_area(
        "Outlet Address *", placeholder="Full address including landmark…", height=90
    )
    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("➕  Add Entry", use_container_width=True)

# ── Validate & save ───────────────────────────────────────────────────────────
if submitted:
    errors = []
    if not outlet_name.strip():         errors.append("Outlet Name is required.")
    if not outlet_mobile.strip():       errors.append("Outlet Mobile No is required.")
    if outlet_type == "-- Select --":   errors.append("Please select Outlet Type.")
    if outlet_class == "-- Select --":  errors.append("Please select Outlet Class.")
    if not location.strip():            errors.append("Location is required.")
    if not outlet_address.strip():      errors.append("Outlet Address is required.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.session_state.survey_data.append({
            "Sr No":            next_sr(),
            "Date":             survey_date.strftime("%d-%m-%Y"),
            "Outlet Name":      outlet_name.strip(),
            "Outlet Mobile No": outlet_mobile.strip(),
            "Outlet Type":      outlet_type,
            "Outlet Class":     outlet_class,
            "Location":         location.strip(),
            "Sub-City":         sub_city.strip(),
            "Sub-Village":      sub_village.strip(),
            "Outlet Address":   outlet_address.strip(),
        })
        st.success(f"✅ Entry #{next_sr() - 1} saved successfully!")

# ── Data table & download ─────────────────────────────────────────────────────
st.markdown("---")

if st.session_state.survey_data:
    df = pd.DataFrame(st.session_state.survey_data)

    st.markdown(f"### 📊 Collected Data &nbsp; `{len(df)} entries`")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Excel export ──────────────────────────────────────────────────────────
    def to_excel(dataframe: pd.DataFrame) -> bytes:
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Survey Data")
            # Auto-fit columns
            ws = writer.sheets["Survey Data"]
            for col_cells in ws.columns:
                max_len = max(
                    len(str(cell.value)) if cell.value else 0
                    for cell in col_cells
                )
                ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 4, 50)
        return buf.getvalue()

    col_dl, col_clr = st.columns([3, 1])
    with col_dl:
        st.download_button(
            label="⬇️  Download Excel",
            data=to_excel(df),
            file_name="Forgokul_Snaks_Survey.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with col_clr:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.survey_data = []
            st.rerun()

else:
    st.info("No entries yet. Fill the form above to start collecting data.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<br>
<div style="text-align:center; color:#aaa; font-size:0.78rem;">
    Forgokul Snaks &nbsp;|&nbsp; Outlet Survey System &nbsp;|&nbsp; Powered by Streamlit
</div>
""", unsafe_allow_html=True)
