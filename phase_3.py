# AUTHOR : MUNEEB IHSAN JANJUA


import requests, os, json, sqlite3

"Portable database path run ANYWHERE "
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "CIS4044-N-SDI-OPENMETEO-PARTIAL.db")

# -------------------------------
" CACHED REQUEST"
# -------------------------------
def make_cached_request(cache_file, url, params=None):
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    if os.path.exists(cache_file):
        with open(cache_file, "r") as raw_data:
            return json.load(raw_data)
    else:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            with open(cache_file, "w", encoding=response.encoding) as file:
                file.write(response.text)
            return response.json()
        else:
            return None

# -------------------------------
" DATEBSE SETUP "
# -------------------------------
def init_db(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_weather_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_id INTEGER,
                date TEXT,
                min_temp REAL,
                max_temp REAL,
                mean_temp REAL,
                precipitation REAL,
                FOREIGN KEY(city_id) REFERENCES cities(id),
                UNIQUE(city_id, date)
            )
        """)
        conn.commit()

def get_or_create_city_id(city_name, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city_name,))
        conn.commit()
        cursor.execute("SELECT id FROM cities WHERE name=?", (city_name,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"City '{city_name}' not found in cities table after insert.")
        return row[0]



def ensure_city(city_name, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city_name,))
        conn.commit()

# -------------------------------
'Weather Update Function'
# -------------------------------
def update_weather(city_name, url, params, db_path=DB_PATH):
    # Ensure DB exists
    init_db(db_path)

    # Fetch data (cached)
    cache_file = f"cache/{city_name}_2025.json"
    data = make_cached_request(cache_file, url, params)
    if not data:
        return

    # Extract daily values
    daily = data["daily"]
    dates = daily["time"]
    mean_temps = daily["temperature_2m_mean"]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    precip = daily["precipitation_sum"]

    # Ensure city exists and get its ID
    city_id = get_or_create_city_id(city_name, db_path)

    # Prepare values with city_id directly
    values = []
    for i in range(len(dates)):
        values.append((
            city_id,
            dates[i],
            min_temps[i],
            max_temps[i],
            mean_temps[i],
            precip[i]
        ))

    # Insert into DB
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR REPLACE INTO daily_weather_entries
            (city_id, date, min_temp, max_temp, mean_temp, precipitation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, values)
        conn.commit()


# -------------------------------
# Example Run
# -------------------------------
cities = {
    # UK
    "Middlesbrough": {"lat": 54.5762, "lon": -1.2348, "tz": "Europe/London"},
    "London": {"lat": 51.5072, "lon": -0.1276, "tz": "Europe/London"},
    "Manchester": {"lat": 53.4808, "lon": -2.2426, "tz": "Europe/London"},
    "Birmingham": {"lat": 52.4862, "lon": -1.8904, "tz": "Europe/London"},
    "Liverpool": {"lat": 53.4084, "lon": -2.9916, "tz": "Europe/London"},

    # France
    "Paris": {"lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris"},
    "Toulouse": {"lat": 43.6047, "lon": 1.4442, "tz": "Europe/Paris"},
    "Marseille": {"lat": 43.2965, "lon": 5.3698, "tz": "Europe/Paris"},
    "Lyon": {"lat": 45.7640, "lon": 4.8357, "tz": "Europe/Paris"},
    "Nice": {"lat": 43.7102, "lon": 7.2620, "tz": "Europe/Paris"},
    # Pakistan
    "Islamabad": {"lat": 33.6844, "lon": 73.0479, "tz": "Asia/Karachi"},
    "Karachi": {"lat": 24.8607, "lon": 67.0011, "tz": "Asia/Karachi"},
    "Lahore": {"lat": 31.5497, "lon": 74.3436, "tz": "Asia/Karachi"}

}


url = "https://archive-api.open-meteo.com/v1/archive"

if __name__ == "__main__":
    for city, coords in cities.items():
        ensure_city(city)
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "start_date": "2020-01-01",
            "end_date": "2025-12-15",
            "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": coords["tz"],
        }
        update_weather(city, url, params)
        # Example run only (kept quiet for easier reuse).



def show_counts(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.name, COUNT(*) 
            FROM daily_weather_entries d
            JOIN cities c ON d.city_id = c.id
            GROUP BY c.name
        """)
        rows = cursor.fetchall()
        return [{"city": name, "row_count": count} for name, count in rows]

