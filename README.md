# HISTORICAL WEATHER REPORT 2020-2025

**Author:** Muneeb Ihsan Janjua  


---

## 1. Project Overview

This project is a **complete end-to-end weather data analysis system** developed using **Python, SQLite, Matplotlib, and the Open-Meteo API**. The system supports:

- Historical weather data collection (2020–2025)
- Relational database storage using SQLite
- Statistical analysis of temperature and precipitation
- Interactive data visualisation
- A menu-driven command-line interface for usability

The project is structured into **three analytical phases** plus a **menu-driven controller**, following good software engineering and data analytics practices.

---

## 2. Project Structure

```
project_root/
│
├── phase_1.py      # Database queries and analytical functions
├── phase_2.py      # Data visualisation (Matplotlib)
├── phase_3.py      # API integration, caching, database updates
├── menu.py         # User menu & program entry point
├── db/
│   └── CIS4044-N-SDI-OPENMETEO-PARTIAL.db
├── cache/          # Cached API responses (JSON)
└── Graphs          # chart made for visualizatin    
└── README.md       # Project documentation
```

---

## 3. Technologies Used

- **Python 3.9+**
- **SQLite3** (relational database)
- **Matplotlib** (visualisation)
- **Requests** (API calls)
- **Open-Meteo Archive API** (weather data)

---

## 4. Phase Breakdown

### Phase 1 – Database Queries & Analysis

Phase 1 focuses on querying the SQLite database and performing analytical computations:

Key features:
- List all countries and cities
- Average annual temperature per city
- 7-day precipitation analysis
- Average temperature by country and date range
- Annual precipitation by country
- Min / Max / Mean temperature and precipitation statistics

All SQL queries use **parameterised statements** to ensure security and correctness.

---

### Phase 2 – Data Visualisation

Phase 2 converts analytical results into **clear and meaningful visualisations** using Matplotlib:

Visualisations implemented:
- Bar chart: 7-day precipitation for a specific city
- Bar chart: average temperature by city within a country
- Bar chart: annual precipitation by country
- Grouped bar charts: min / max / mean temperature by city
- Grouped bar charts: min / max / mean precipitation by city
- Line chart: daily min / max / mean temperature for a city/month
- Scatter plot: average temperature vs average precipitation (city or country level)

All charts include:
- Proper titles and axis labels
- Gridlines for readability
- Dynamic scaling

---

### Phase 3 – API Integration & Data Updates

Phase 3 integrates **real-world weather data** using the Open-Meteo Archive API.

Key features:
- API request caching to avoid repeated downloads
- Automatic database initialisation
- Incremental updates using `INSERT OR REPLACE`
- Support for multiple cities across UK, France, and Pakistan

Supported cities:
- **UK:** Middlesbrough, London, Manchester, Birmingham, Liverpool
- **France:** Paris, Toulouse, Marseille, Lyon, Nice
- **Pakistan:** Islamabad, Karachi, Lahore

---

## 5. Menu System (menu.py)

The project is controlled through a **user-friendly command-line menu**.

### Main Menu
- Data Visualisation Menu
- Data Update Menu
- Exit Program

### Visualisation Menu Options
1. 7-Day Precipitation (City-based)
2. Average Temperature by Country (Date Range)
3. Annual Precipitation by Country
4. Min/Max/Mean Temperature by City
5. Min/Max/Mean Precipitation by City
6. Scatter Plot (Temperature vs Precipitation)

### Data Update Menu Options
1. Initialise Database
2. Insert Cities
3. Update Weather for All Cities
4. Update Weather for a Single City
5. Show Row Counts per City

Input validation is implemented for:
- Date formats
- Year ranges
- Valid city and country names

---

## 6. How to Run the Project

### Step 1: Install Dependencies

```bash
pip install matplotlib requests
```

### Step 2: Run the Menu

```bash
python menu.py
```

### Step 3: Use the Menu

Follow on-screen instructions to:
- Update weather data
- Generate visualisations
- Explore historical weather trends

---

## 7. Data Source

Weather data is sourced from:

**Open-Meteo Archive API**  
https://archive-api.open-meteo.com

Data includes:
- Daily mean temperature
- Daily max/min temperature
- Daily precipitation sum

---

## 8. Key Design Decisions

- SQLite chosen for portability and ease of assessment
- API caching implemented to improve performance
- Separation of concerns across phases
- Parameterised SQL for security
- Menu-driven interface for usability

---

## 9. Limitations & Future Improvements

Current limitations:
- Static country list
- Command-line interface only
- No interactive dashboards

Potential enhancements:
- Power BI or Tableau integration
- Web-based dashboard (Flask / Streamlit)
- Automated scheduling of data updates
- Advanced statistical forecasting

---

## 10. Academic Declaration

This project is my own work and was developed for academic purposes as part of the MSc Applied Data Science programme at Teesside University.

---

**End of README**

