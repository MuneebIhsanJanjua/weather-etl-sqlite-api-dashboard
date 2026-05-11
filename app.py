from datetime import date

import streamlit as st

from phase_2 import (
    plot_average_temperature_vs_precipitation,
    plot_average_annual_precipitation_by_country,
    plot_average_temperatures_by_country,
    plot_min_max_mean_precipitation_by_city_in_country,
    plot_min_max_mean_temperature_by_city_in_country,
    plot_seven_day_precipitation,
)
from phase_3 import cities, ensure_city, init_db, show_counts, update_weather, url


COUNTRIES = ["UK", "France", "Pakistan"]
DAILY_FIELDS = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
]

DATE_MIN = date(2020, 1, 1)
DATE_MAX = date(2025, 12, 31)
DATE_START_DEFAULT = date(2020, 1, 1)
DATE_END_DEFAULT = date(2025, 12, 15)


def _date_to_iso(d: date) -> str:
    return d.isoformat()


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

.stApp {
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<style>

/* ── Page background ── */
.stApp {
    background-color: #F8F9FB;
}

/* ── Main page title (st.title) ── */
h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2rem !important;
    font-weight: 400 !important;
    letter-spacing: -0.02em !important;
    color: #1A1A2E !important;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 1.5rem !important;
}

/* ── Section headings (st.header / st.subheader) ── */
h2 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #1A1A2E !important;
    margin-top: 0 !important;
}

h3 {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: #4A5568 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    padding-top: 1rem;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #718096 !important;
    margin-bottom: 4px !important;
}

/* ── Sidebar radio buttons → styled as nav pills ── */
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    padding: 7px 12px !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
    color: #4A5568 !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    margin-bottom: 2px !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #F1F5F9 !important;
    color: #1A1A2E !important;
}

[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div label,
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: #E6F1FB !important;
    color: #185FA5 !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] .stRadio input[type="radio"] {
    accent-color: #185FA5 !important;
}

/* ── Sidebar selectbox ── */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #F8F9FB !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    color: #1A1A2E !important;
}

/* ── Form field labels ── */
.stSelectbox label,
.stTextInput label,
.stDateInput label,
.stSlider label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #718096 !important;
    margin-bottom: 4px !important;
}

/* ── Selectbox (main content) ── */
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    padding: 2px 4px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #378ADD !important;
    box-shadow: 0 0 0 3px rgba(55, 138, 221, 0.15) !important;
}

/* ── Text / Date Input ── */
.stTextInput > div > div > input,
.stDateInput > div > div > input {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E0 !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 9px 14px !important;
    color: #1A1A2E !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}

.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: #378ADD !important;
    box-shadow: 0 0 0 3px rgba(55, 138, 221, 0.15) !important;
}

/* ── Primary button ("Generate chart") ── */
.stButton > button {
    background-color: #185FA5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 9px 22px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
}

.stButton > button:hover {
    background-color: #0C447C !important;
    border: none !important;
}

.stButton > button:active {
    transform: scale(0.98) !important;
}

/* ── Sliders ── */
.stSlider [role="slider"] {
    background-color: #185FA5 !important;
    border-color: #185FA5 !important;
}

/* ── Card-style container (st.form only; avoids wrapping whole page blocks) ── */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
}

/* ── Charts: Plotly / Vega / Pydeck / Matplotlib (st.pyplot) ── */
[data-testid="stPlotlyChart"],
[data-testid="stArrowVegaLiteChart"],
[data-testid="stPydeckChart"],
[data-testid="stImage"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin-top: 1rem !important;
}

/* ── Info / success / warning banners ── */
.stAlert {
    border-radius: 8px !important;
    font-size: 13.5px !important;
}

/* ── Streamlit default top padding reduction ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 860px !important;
}

/* ── Hide Streamlit branding (optional; do not hide header — breaks layout) ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

</style>
""",
    unsafe_allow_html=True,
)

st.title("Weather Data Analysis")

nav = st.sidebar.radio(
    "Navigation",
    ["Data Visualization", "Database Management"],
    index=0,
)

if nav == "Data Visualization":
    st.markdown(
        """
    <span style="font-size:28px; font-weight:bold;">
        🌤️ Data Visualization
    </span>
    """,
        unsafe_allow_html=True,
    )

    visualization_choice = st.sidebar.selectbox(
        "Visualization",
        [
            "Plot 7-Day Precipitation",
            "Plot Average Temperatures by Country",
            "Plot Average Annual Precipitation by Country",
            "Plot Min/Max/Mean Temperature by City in Country",
            "Plot Min/Max/Mean Precipitation by City in Country",
            "Scatter Plot: Avg Temperature vs Avg Precipitation",
        ],
    )

    city_options = sorted(list(cities.keys()))

    if visualization_choice == "Plot 7-Day Precipitation":
        st.subheader("7-Day Precipitation for a Specific City")
        city_name = st.selectbox("City", city_options, index=0)
        start_date = st.date_input(
            "Start Date",
            value=DATE_START_DEFAULT,
            min_value=DATE_MIN,
            max_value=DATE_MAX,
        )

        if st.button("Generate chart"):
            fig = plot_seven_day_precipitation(city_name=city_name, start_date=_date_to_iso(start_date))
            if fig is None:
                st.info("No precipitation data found for the selected city and start date.")
            else:
                st.pyplot(fig)

    elif visualization_choice == "Plot Average Temperatures by Country":
        st.subheader("Average Mean Temperatures by Country")
        country_name = st.selectbox("Country", COUNTRIES, index=0)
        date_from = st.date_input(
            "Date From",
            value=DATE_START_DEFAULT,
            min_value=DATE_MIN,
            max_value=DATE_MAX,
        )
        date_to = st.date_input(
            "Date To",
            value=DATE_END_DEFAULT,
            min_value=DATE_MIN,
            max_value=DATE_MAX,
        )

        if st.button("Generate chart"):
            if date_from > date_to:
                st.error("`Date From` must be earlier than or equal to `Date To`.")
            else:
                fig = plot_average_temperatures_by_country(
                    country_name=country_name,
                    date_from=_date_to_iso(date_from),
                    date_to=_date_to_iso(date_to),
                )
                if fig is None:
                    st.info("No data found for the selected country and date range.")
                else:
                    st.pyplot(fig)

    elif visualization_choice == "Plot Average Annual Precipitation by Country":
        st.subheader("Average Annual Precipitation by Country")
        year = st.slider("Year", min_value=2020, max_value=2025, value=2025, step=1)

        if st.button("Generate chart"):
            fig = plot_average_annual_precipitation_by_country(year=year)
            if fig is None:
                st.info("No precipitation data found for the selected year.")
            else:
                st.pyplot(fig)

    elif visualization_choice == "Plot Min/Max/Mean Temperature by City in Country":
        st.subheader("Min/Max/Mean Temperature by City in Country")
        country_name = st.selectbox("Country", COUNTRIES, index=0)
        year = st.slider("Year", min_value=2020, max_value=2025, value=2025, step=1)

        if st.button("Generate chart"):
            fig = plot_min_max_mean_temperature_by_city_in_country(country_name=country_name, year=year)
            if fig is None:
                st.info("No temperature data found for the selected inputs.")
            else:
                st.pyplot(fig)

    elif visualization_choice == "Plot Min/Max/Mean Precipitation by City in Country":
        st.subheader("Min/Max/Mean Precipitation by City in Country")
        country_name = st.selectbox("Country", COUNTRIES, index=0)
        year = st.slider("Year", min_value=2020, max_value=2025, value=2025, step=1)

        if st.button("Generate chart"):
            fig = plot_min_max_mean_precipitation_by_city_in_country(country_name=country_name, year=year)
            if fig is None:
                st.info("No precipitation data found for the selected inputs.")
            else:
                st.pyplot(fig)

    elif visualization_choice == "Scatter Plot: Avg Temperature vs Avg Precipitation":
        st.subheader("Scatter Plot: Avg Temperature vs Avg Precipitation")
        group_choice = st.radio("Group by", ["city", "country"], index=0, horizontal=True)

        if st.button("Generate chart"):
            fig = plot_average_temperature_vs_precipitation(group_by=group_choice)
            if fig is None:
                st.info("No data available for the scatter plot.")
            else:
                st.pyplot(fig)

else:
    st.markdown(
        """
    <span style="font-size:30px; font-weight:bold;">
        🌤️ Database Management
    </span>
    """,
        unsafe_allow_html=True,
    )
    city_options = sorted(list(cities.keys()))

    init_clicked = st.button("Initialize database")
    insert_clicked = st.button("Insert all cities")
    update_all_clicked = st.button("Update weather data (all cities)")

    if init_clicked:
        init_db()
        st.success("Database initialized.")

    if insert_clicked:
        with st.spinner("Inserting cities..."):
            for city_name in cities.keys():
                ensure_city(city_name)
        st.success("Cities inserted (idempotent).")

    if update_all_clicked:
        st.info("Updating weather data for all cities. This can take a while...")
        with st.spinner("Fetching + updating from Open-Meteo (cached)..."):
            for city_name, coords in cities.items():
                params = {
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "start_date": "2020-01-01",
                    "end_date": "2025-12-15",
                    "daily": DAILY_FIELDS,
                    "timezone": coords["tz"],
                }
                update_weather(city_name, url, params)
        st.success("Weather data updated for all cities.")

    st.divider()

    update_one_city = st.selectbox("Select city to update", city_options, index=0)
    update_single_clicked = st.button("Update selected city")
    if update_single_clicked:
        coords = cities[update_one_city]
        st.info(f"Updating weather data for `{update_one_city}`...")
        with st.spinner("Fetching + updating (cached)..."):
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": "2020-01-01",
                "end_date": "2025-12-15",
                "daily": DAILY_FIELDS,
                "timezone": coords["tz"],
            }
            update_weather(update_one_city, url, params)
        st.success(f"Weather data updated for `{update_one_city}`.")

    st.divider()

    show_counts_clicked = st.button("Show row counts")
    if show_counts_clicked:
        rows = show_counts()
        if not rows:
            st.info("No rows found yet. Initialize/update the database first.")
        else:
            st.table(rows)
