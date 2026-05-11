# Author: MUNEEB IHSAN JANJUA

'Project Title: Weather Data Analysis by using sqlite3 and python'


import matplotlib.pyplot as plt
from phase_1 import (
    average_annual_precipitation_by_country,
    average_mean_temp_by_country,
    seven_day_precip,
    max_min_mean_temperature_by_city_in_country,
    max_min_mean_precipitation_by_city_in_country,
    min_max_mean_temperature_by_specific_city_month,
    avg_temp_vs_precip,
    select_all_countries,
    select_all_cities,
    average_annual_temperature,
    average_seven_day_precipitation,
    monthly_avg_temperature,
    maximum_temperature_by_city,

    create_connection
)



'--------------------------------------------- Visualization Section ---------------------------------------------------'

"---------------------------------First REQUIREMENT COMPLETED HERE for visualization----------------------------------- "
'------------------------------Bar chart: 7 - day precepitation for a sepcific city-----------------------------'

def plot_seven_day_precipitation(city_name, start_date):
    with create_connection() as connection:
        rows, city_name = seven_day_precip(
            connection, city_name=city_name, start_date=start_date
        )
        if not rows:
            return None
        dates = [row["date"] for row in rows]
        precips = [row["precipitation"] for row in rows]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(dates, precips, color="blue")
        ax.set_xlabel("Date")
        ax.set_ylabel("Precipitation (mm)")
        ax.set_title(f"7-Day Precipitation for City {city_name} starting {dates[0]}")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        return fig



 
"----------------------------------Second Requiremnet completed here for visualization----------------------------------"
"-----------------------Bar chart: for a specific date range for specified set of cities or countries-----------"


def plot_average_temperatures_by_country(country_name, date_from, date_to):
    with create_connection() as connection:
        city_temp = average_mean_temp_by_country(
            connection,
            country_name=country_name,
            date_from=date_from,
            date_to=date_to )
        if not city_temp:
            return None

        cities = [row["city_name"] for row in city_temp]
        avg_temps = [row["avg_temp"] for row in city_temp]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(cities, avg_temps)
        ax.set_xlabel("City")
        ax.set_ylabel("Average Mean Temperature (°C)")
        ax.set_title(
            f"Average Mean Temperature by Cities in {country_name} "
            f"from {date_from} to {date_to}"
        )
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        ax.set_ylim(0, max(avg_temps) + 5)
        return fig



'---------------------------------THIRD REQUIREMENT COMPLETED HERE FOR VISUALIZATION ---------------------------------------'
'---------------------------------------AVERAGE ANNUAL PRECIPITATION BY COUNTRY---------------------------------------'
def plot_average_annual_precipitation_by_country(year):
    with create_connection() as connection:
        country_annual_precipitation = average_annual_precipitation_by_country(
            connection,
            year=year
        )
        if not country_annual_precipitation:
            return None

        countries = [row["country_name"] for row in country_annual_precipitation]
        avg_precipitations = [row["avg_precip"] for row in country_annual_precipitation]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(countries, avg_precipitations, color="green")
        ax.set_xlabel("Country")
        ax.set_ylabel("Average Annual Precipitation (mm)")
        ax.set_title(f"Average Annual Precipitation by Countries  in {year}")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        ax.set_ylim(0, max(avg_precipitations) + 1)
        return fig



'-------------------------------------FOURTH REQUIREMENT COMPLETED HERE FOR VISUALIZATION ---------------------------------------'
'------------------------------Group chart @ for min/max/mean temperature and preceipiton for countries and cities @ ---------------------------------------'



def plot_min_max_mean_temperature_by_city_in_country(country_name, year):
    with create_connection() as connection:
        city_temps = max_min_mean_temperature_by_city_in_country(
            connection,
            country_name=country_name,
            year=year,
        )
        if not city_temps:
            return None

        cities = [row["city_name"] for row in city_temps]
        max_temps = [row["max_temp"] for row in city_temps]
        min_temps = [row["min_temp"] for row in city_temps]
        mean_temps = [row["mean_temp"] for row in city_temps]

        x = range(len(cities))
        width = 0.25

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar([p - width for p in x], max_temps, width=width, label="Max Temp", color="red")
        ax.bar(x, min_temps, width=width, label="Min Temp", color="blue")
        ax.bar([p + width for p in x], mean_temps, width=width, label="Mean Temp", color="green")

        ax.set_xlabel("City")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(
            f"Min, Max, and Mean Temperatures by City in {country_name} for {year}"
        )
        ax.set_xticks(list(x))
        ax.set_xticklabels(cities, rotation=45, ha="right")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        ax.set_ylim(0, max(max_temps) + 5)

        return fig
 

'--------------------------------Group chart for min/max/mean precipitation by city in country ---------------------------------------'

def plot_min_max_mean_precipitation_by_city_in_country(country_name, year):
    with create_connection() as connection:
        city_precips = max_min_mean_precipitation_by_city_in_country(
            connection,
            country_name=country_name,
            year=year
        )
        if not city_precips:
            return None
    
        cities = [row["city_name"] for row in city_precips]
        max_precips = [row["max_precip"] for row in city_precips]
        min_precips = [row["min_precip"] for row in city_precips]
        mean_precips = [row["mean_precip"] for row in city_precips]
    
        x = range(len(cities))
        width = 0.25
    
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar([p - width for p in x], max_precips, width=width, label="Max Precip", color="cyan")
        ax.bar(x, min_precips, width=width, label="Min Precip", color="orange")
        ax.bar([p + width for p in x], mean_precips, width=width, label="Mean Precip", color="purple")
    
        ax.set_xlabel("City")
        ax.set_ylabel("Precipitation (mm)")
        ax.set_title(f"Min, Max, and Mean Precipitation by City in {country_name} for {year}")
        ax.set_xticks(x)
        ax.set_xticklabels(cities, rotation=45, ha="right")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()
        ax.set_ylim(0, max(max_precips) + 1)
        return fig




'-------------------------------------FIFTH REQUIREMENT COMPLETED HERE FOR VISUALIZATION ---------------------------------------'
'------------------------------Line chart for min/max/mean precipitation for city specific month ---------------------------------------'

def plot_min_max_mean_temperature_for_city_month(connection, city_name,year ,month):
    rows = min_max_mean_temperature_by_specific_city_month(connection, city_name, year, month)
    if not rows:
        return None

    city_name = rows[0]["city_name"]
    min_temps = [row["min_temp"] for row in rows]
    max_temps = [row["max_temp"] for row in rows]
    mean_temps = [row["mean_temp"] for row in rows]
    dates = [f"{year}-{month:02d}-{day:02d}" for day in range(1, len(rows) + 1)]
    plt.figure(figsize=(12, 6))
    plt.plot(dates, min_temps, marker="o", label="Min Temp", color="blue")
    plt.plot(dates, max_temps, marker="o", label="Max Temp", color="red")
    plt.plot(dates, mean_temps, marker="o", label="Mean Temp", color="green")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Min, Max, and Mean Temperatures for {city_name} in {year}-{month:02d} month")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.ylim(min(min_temps) - 1, max(max_temps) + 1)
    plt.show()
    return dates, min_temps, max_temps, mean_temps




      
   

# Remaing task: scatter plot for average temperature agaist average rainfall for city or countries or all cities , howeever there is no rainfall data so todo it 
def plot_average_temperature_vs_rainfall():
    # TODO: Implement scatter plot for average temperature against average rainfall
    pass
def plot_average_temperature_vs_precipitation(group_by="city"):
    connection = create_connection()
    rows = avg_temp_vs_precip(connection, group_by=group_by)

    if not rows:
        return None

    labels = [row["label"] for row in rows]
    avg_temps = [row["avg_temp"] for row in rows]
    avg_precips = [row["avg_precip"] for row in rows]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(avg_temps, avg_precips, color="purple")

    for i, label in enumerate(labels):
        ax.text(avg_temps[i], avg_precips[i], label, fontsize=9)

    ax.set_xlabel("Average Temperature (°C)")
    ax.set_ylabel("Average Precipitation (mm)")
    ax.set_title(f"Average Temperature vs Precipitation ({group_by.title()})")
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()

    connection.close()
    return fig



if __name__ == "__main__":
    plot_average_annual_precipitation_by_country(year=2025)
    plot_min_max_mean_temperature_by_city_in_country(country_name="Lyon", year=2025)
    plot_average_temperatures_by_country(country_name="Pakistan", date_from="2020-01-01", date_to="2025-12-31")
    plot_min_max_mean_precipitation_by_city_in_country(country_name="France", year=2025)
    plot_min_max_mean_temperature_for_city_month(create_connection(), city_name="Nice", year=2025, month=2)
    








""""def plot_min_max_mean_temperature_and_precipitation(city_id, year):
 with create_connection() as connection:
        # Max Temperature
        max_temp_data, city_name= max_min_mean_temperature_by_city(
            connection,
            city_id=city_id,
            year=year,
            temp_type="max"
        )
        months = [row["month"] for row in max_temp_data]
        max_temps = [row["temp"] for row in max_temp_data]  
        # Min Temperature
        min_temp_data, _ = max_min_mean_temperature_by_city(
            connection,
            city_id=city_id,
            year=year,
            temp_type="min"
        )
        min_temps = [row["temp"] for row in min_temp_data]
        # Mean Temperature
        mean_temp_data, _ = max_min_mean_temperature_by_city(
            connection,
            city_id=city_id,
            year=year,
            temp_type="mean"
        )
        mean_temps = [row["temp"] for row in mean_temp_data]
        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(months, max_temps, marker="o", label="Max Temp", color="red")
        plt.plot(months, min_temps, marker="o", label="Min Temp", color="blue")
        plt.plot(months, mean_temps, marker="o", label="Mean Temp", color="green")
        plt.xlabel("Month")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Monthly Max, Min, and Mean Temperatures for City {city_name} in {year}")
        plt.xticks(months)
        plt.legend()
        plt.grid(linestyle="--", alpha=0.4)
        plt.tight_layout()
        plt.show()
        connection.close()
        return months, max_temps, min_temps, mean_temps
plot_min_max_mean_temperature_and_precipitation(city_id=1, year=2022)"""








"""
city_temp = average_mean_temp_by_city(connection, date_from='2022-01-01', date_to='2022-12-31') 
cities = [row["city_name"] for row in city_temp]
avg_temps = [row["avg_temp"] for row in city_temp]


plt.figure(figsize=(12,6))
plt.bar(cities, avg_temps, color="skyblue")
plt.xlabel("City")
plt.ylabel("Average Mean Temperature (°C)")
plt.title(f"Average Mean Temperature by City from 2022-01-01 to 2022-12-31")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

country_annual_precipitation = average_annual_precipitation_by_country(connection, year=2022)
countries = [row["country_name"] for row in country_annual_precipitation]
avg_precipitations = [row["avg_precip"] for row in country_annual_precipitation]
plt.figure(figsize=(12,6))
plt.bar(countries, avg_precipitations, color="lightgreen")
plt.xlabel("Country")
plt.ylabel("Average Annual Precipitation (mm)")
plt.title(f"Average Annual Precipitation by Country in 2022")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

annual_temp = average_annual_temperature(connection, city_id=1, year=2022)
years = annual_temp['years']
temps = annual_temp['avg_temps']
plt.figure(figsize=(6,6))
plt.plot(years, temps, color="salmon", marker="o", linestyle="-")
plt.xlabel("Year")
plt.ylabel("Average Annual Temperature (°C)")
plt.title("Average Annual Temperature for City ID 1")
plt.show()
monthly_temp = monthly_avg_temperature(connection, city_id=1, year=2022)

# Extract values from each row in the list
months = [row["month"] for row in monthly_temp]
avg_temps = [row["avg_temp"] for row in monthly_temp]


plt.figure(figsize=(10,6))
plt.plot(months, avg_temps, marker="o", linestyle="-", color="salmon")
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")
plt.title("Monthly Average Temperature for City ID 1 in 2022")
plt.tight_layout()
plt.show()

"""