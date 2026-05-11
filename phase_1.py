# Author: MUNEEB IHSAN JANJUA

'Project Title: Weather Data Analysis by using sqlite3 and pythoN'
import sqlite3
import matplotlib.pyplot as plt
import os
# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

"Portable database path run ANYWHERE "
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "CIS4044-N-SDI-OPENMETEO-PARTIAL.db")



"Routines to query the weather database and print results to the console."

def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        print('--------------------------- Countries---------------------------')
        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)
def select_all_cities(connection):

    try:
        print('--------------------------- Cities---------------------------')
        query = 'SELECT * from [cities]'
        cursor = connection.cursor()
        result = cursor.execute(query)
        for row in result:
            print(
                f"City id: {row['id']} ---- City Name {row['name']} ---- "
                f"Country id {row['country_id']} --- latlong: {row['latlong']}"
            )
    except sqlite3.Error as ex:
        print(ex)

def average_annual_temperature(connection, city_id, year):
   
   try:
        cursor = connection.cursor()
        query = """
            SELECT ROUND(AVG(mean_temp), 2) AS avg_temp
            FROM [daily_weather_entries]
            WHERE city_id = ?
            AND strftime('%Y', date) = ?
        """

        result = cursor.execute(query, (city_id, str(year))).fetchone()

        if result and result["avg_temp"] is not None:
            print(f"Average annual temperature for city {city_id} in {year}: {result['avg_temp']}°C")
        else:
            print("No temperature data found.")

   except sqlite3.Error as ex:
       print(ex)

'---------First REQUIREMENT COMPLETED HERE for visualization ---------'
'---------------7 DAY PRECIPITATION FOR A SPECIFIC CITY------------------'

def seven_day_precip(connection, city_name, start_date):
    try: 
        cursor = connection.cursor()
        query = """
            SELECT c.name AS city_name, 
                     w.date AS date, 
                     w.precipitation AS precipitation
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            WHERE c.name = ? AND w.date >= ? AND w.date < date(?, '+7 days')
            ORDER BY w.date;
        """
        rows = cursor.execute(query, (city_name, start_date, start_date)).fetchall()
        query1 = ''' SELECT * FROM cities WHERE name=?'''
        result2  = cursor.execute(query1,(city_name,)).fetchone()

        dates = [row["date"] for row in rows]
        precips = [row["precipitation"] for row in rows]
        city_name = result2["name"] if result2 else f"City ID {city_name}"
        return rows , city_name
    except sqlite3.Error as ex:
        print(ex)
def average_seven_day_precipitation(connection, city_id, start_date):

    try:
        cursor = connection.cursor()

        query = """
            SELECT ROUND(AVG(precipitation), 2) AS avg_precip
            FROM (
                SELECT precipitation
                FROM daily_weather_entries
                WHERE city_id = ?
                AND date >= ?
                AND date < date(?, '+7 days')
            )
        """
       

        result = cursor.execute(query, (city_id, start_date, start_date)).fetchone()

        if result and result["avg_precip"] is not None:
            print(f"Average 7-day precipitation from {start_date}: {result['avg_precip']} mm")
            return result
        else:
            print("No precipitation data found.")
            return None

    except sqlite3.Error as ex:
        print(ex)

'---------Second REQUIREMENT COMPLETED HERE FOR VISUALIZATION ---------'
'-------------SPECIFIC DATE RANGE FOR SET OF CITIES--------------'
def average_mean_temp_by_country(connection, country_name, date_from, date_to):
    try:
        cursor = connection.cursor()

        query = """
            SELECT c.name AS city_name,
                   ROUND(AVG(w.mean_temp), 2) AS avg_temp
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            JOIN countries co ON c.country_id = co.id
            WHERE co.name = ?
              AND w.date >= ?
              AND w.date <= ?
            GROUP BY c.id
            ORDER BY c.name;
        """

        rows = cursor.execute(query, (country_name, date_from, date_to)).fetchall()

        if rows:
            return rows
        else:
            return None

    except sqlite3.Error as ex:
        return None


'----------- THIRD REQUIREMENT COMPLETED HERE FOR VISUALIZATION ---------'
'-----------AVERAGE ANNUAL PRECIPITATION BY COUNTRY------------------'
def average_annual_precipitation_by_country(connection , year):
    try:
        

        query = """
            SELECT co.name AS country_name,
                   ROUND(AVG(w.precipitation), 2) AS avg_precip
            FROM daily_weather_entries w
            JOIN cities ci ON w.city_id = ci.id
            JOIN countries co ON ci.country_id = co.id
            WHERE strftime('%Y', w.date) = ?
            GROUP BY co.id
            ORDER BY co.name;
        """
        cursor = connection.cursor()
        rows = cursor.execute(query, (str(year),)).fetchall()

        if rows:
            return rows
        else:
            return None

    except sqlite3.Error as ex:
        return None


'---------------------FOURTH REQUIREMENT COMPLETED HERE FOR VISUALIZATION ---------------------------------------'
'-----------------MIN/MAX/MEAN TEMPERATURE AND PRECEIPITON FOR COUNTRIES AND CITIES-------------------------'

def max_min_mean_temperature_by_city_in_country(connection, country_name, year):
    try:
        cursor = connection.cursor()

        query = """
            SELECT 
                c.name AS city_name,
                MAX(w.mean_temp) AS max_temp,
                MIN(w.mean_temp) AS min_temp,
                ROUND(AVG(w.mean_temp), 2) AS mean_temp
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            JOIN countries co ON c.country_id = co.id
            WHERE co.name = ?
              AND strftime('%Y', w.date) = ?
            GROUP BY c.id
            ORDER BY c.name;
        """

        rows = cursor.execute(query, (country_name, str(year))).fetchall()

        if not rows:
            return None

        return rows

    except sqlite3.Error as ex:
        return None
def max_min_mean_precipitation_by_city_in_country(connection, country_name, year):
    try:
        cursor = connection.cursor()

        query = """
            SELECT 
                c.name AS city_name,
                MAX(w.precipitation) AS max_precip,
                MIN(w.precipitation) AS min_precip,
                ROUND(AVG(w.precipitation), 2) AS mean_precip
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            JOIN countries co ON c.country_id = co.id
            WHERE co.name = ?
              AND strftime('%Y', w.date) = ?
            GROUP BY c.id
            ORDER BY c.name;
        """

        rows = cursor.execute(query, (country_name, str(year))).fetchall()

        if not rows:
            return None

        return rows

    except sqlite3.Error as ex:
        return None
'---------------------FOURTH REQUIREMENT COMPLETED FOR VISUALIZATION ---------------------------------------'

'-------------------------------- Fifth REQUIREMENT COMPLETED HERE FOR VISUALIZATION --------------------------- '
'--------------------------------MIN/MAX/MEAN TEMPERATURE FOR A SPECIFIC CITY AND MONTH-------------------------'
def min_max_mean_temperature_by_specific_city_month(connection, city_name, year, month):
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                c.name AS city_name,
                strftime('%Y', w.date) AS year,
                strftime('%m', w.date) AS month,
                w.date AS day,
                MIN(w.min_temp) AS min_temp,
                MAX(w.max_temp) AS max_temp,
                ROUND(AVG(w.mean_temp), 2) AS mean_temp
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            WHERE c.name = ?
              AND strftime('%Y', w.date) = ?
              AND strftime('%m', w.date) = ?
            GROUP BY w.date
            ORDER BY w.date
        """
        rows = cursor.execute(query, (city_name, str(year), f"{month:02}")).fetchall()

        for row in rows:
            print(
                f"{row['city_name']} ({row['year']}-{row['month']}-{row['day']}) → "
                f"Max: {row['max_temp']}°C, "
                f"Min: {row['min_temp']}°C, "
                f"Mean: {row['mean_temp']}°C"
            )
        return rows

    except sqlite3.Error as ex:
        print(ex)
        return None


'---------------------Sixth REQUIREMENT COMPLETED FOR VISUALIZATION ---------------------------------------'

def average_temperature_vs_rainfall():
#TODO: Implement scatter plot for average temperature against average precipitation
    pass


def maximum_temperature_by_city(connection, city_id, date_from, date_to):
    try:
        cursor = connection.cursor()

        query = """
            SELECT MAX(mean_temp) AS max_temp
            FROM daily_weather_entries
            WHERE city_id = ?
              AND date >= ?
              AND date <= ?
        """

        result = cursor.execute(query, (city_id, date_from, date_to)).fetchone()
        if result and result["max_temp"] is not None:
            print(f"Maximum temperature for city {city_id} from {date_from} to {date_to}: {result['max_temp']}°C")
            return

        else:
            print("No temperature data found.")
    except sqlite3.Error as ex:
        print(ex)
def minimum_temperature_by_city(connection, city_id, date_from, date_to):
    try:
        cursor = connection.cursor()

        query = """
            SELECT MIN(mean_temp) AS min_temp
            FROM daily_weather_entries
            WHERE city_id = ?
              AND date >= ?
              AND date <= ?
        """

        result = cursor.execute(query, (city_id, date_from, date_to)).fetchone()
        if result and result["min_temp"] is not None:
            print(f"Minimum temperature for city {city_id} from {date_from} to {date_to}: {result['min_temp']}°C")  
        else:
            print("No temperature data found.")
    except sqlite3.Error as ex:
        print(ex)
def monthly_avg_temperature(connection, city_id, year):
    query = """
        SELECT strftime('%m', date) AS month,
               ROUND(AVG(mean_temp), 2) AS avg_temp
        FROM daily_weather_entries
        WHERE city_id = ?
          AND strftime('%Y', date) = ?
        GROUP BY month
        ORDER BY month;
    """
    cursor = connection.cursor()
    return cursor.execute(query, (city_id, str(year))).fetchall()
def create_connection(db_path = DB_PATH):
        """Create a database connection and return it."""
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect(db_path)
        
            # You can optionally set row_factory to sqlite3.Row to access columns by name
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            return None
def avg_temp_vs_precip(connection, group_by="city"):
    cursor = connection.cursor()

    if group_by == "city":
        query = """
            SELECT c.name AS label,
                   ROUND(AVG(w.mean_temp), 2) AS avg_temp,
                   ROUND(AVG(w.precipitation), 2) AS avg_precip
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            GROUP BY c.id
            ORDER BY c.name;
        """

    elif group_by == "country":
        query = """
            SELECT co.name AS label,
                   ROUND(AVG(w.mean_temp), 2) AS avg_temp,
                   ROUND(AVG(w.precipitation), 2) AS avg_precip
            FROM daily_weather_entries w
            JOIN cities c ON w.city_id = c.id
            JOIN countries co ON c.country_id = co.id
            GROUP BY co.id
            ORDER BY co.name;
        """

    else:
        return None

    return cursor.execute(query).fetchall()




if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.

    connection = create_connection(DB_PATH)
    print("DB : ", DB_PATH)
    #min_max_mean_temperature_by_specific_city_month(connection,"Middlesbrough",2020,1)
    #max_min_mean_temperature_by_city_in_country(connection, country_name="France", year=2020)
  # Replace with the actual path to your SQLite database
    #select_all_countries(connection)
    #select_all_cities(connection)
    #average_annual_temperature(connection=connection, city_id=1 , year=2020)
    #city_weekly_percipitation = average_seven_day_precipitation(connection, city_id=1, start_date='2022-06-01')
    #average_mean_temp_by_city(connection=connection, date_from='2020-01-01', date_to='2020-12-31')
    #verage_annual_precipitation_by_country(connection=connection, year=2020)"""