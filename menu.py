from datetime import datetime
from phase_2 import ( 
    plot_seven_day_precipitation,
    plot_average_temperatures_by_country,
    plot_average_annual_precipitation_by_country,
    plot_min_max_mean_temperature_by_city_in_country,
    plot_min_max_mean_precipitation_by_city_in_country,
    plot_average_temperature_vs_precipitation,
) 
from phase_3 import init_db, ensure_city, update_weather, show_counts, cities, url

# -------------------------------
# Making  menu for user to select
#  from datetime import datetime


def main_menu():
    
    while True:
        print('Welcome to Histroical Weather Menu')
        print('Enter 1 for Data Visualization Menu')
        print('Enter 2 for Data Update Menu')
        print("Enter 3 for Exit ")
        choice = input("Enter your choice 1  2  3: ")
        if choice == "1":
            display_plot_menu()
        elif choice == "2":
            display_update_menu()
        elif choice == "3":
            print ("Exit Program ")
            break
        else: 
            print("Invalid choice, try again")






 

def display_plot_menu():
    while True:
        print("\nWeather Data Visualization Menu: ")
        print("1. Plot 7-Day Precipitation")
        print("2. Plot Average Temperatures by Country")
        print("3. Plot Average Annual Precipitation by Country")
        print("4. Plot Min/Max/Mean Temperature by City in Country")
        print("5. Plot Min/Max/Mean Precipitation by City in Country")
        print("6. Scatter Plot: Avg Temperature vs Avg Precipitation")
        print("7. Update Weather Data")
        
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")
        if choice == "1":
            print("Cities Available: \n Middlesbrough, London , Manchester, Liverpool, \n Paris, Toulouse, Marseille, Lyon , Nice, \nKarachi, Islamabad, Lahore")
            city_name = input("Enter City Name: ")
            if city_name not in ["Middlesbrough", "London", "Manchester", "Liverpool", "Paris", "Toulouse", "Marseille", "Lyon", "Nice", "Karachi", "Islamabad", "Lahore"]:
                print("City not found. Please try again.")
                continue    
            print("date format e.g.  2020-01-01")
            print("Available date range: 2020-01-01 to 2025-12-15")
            start_date = input("Enter Start Date (YYYY-MM-DD): ")

            try:
    
                datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            plot_seven_day_precipitation(city_name, start_date)
        elif choice == "2":
            country_name = input("Enter Country Name: ")
            if country_name not in ["UK", "France", "Pakistan"]:
                print("Country not found. Please try again.")
                continue 
            try:
                print("Range of dates available: 2020-01-01 to 2025-12-31")
                print("date format e.g.  2020-01-01")
                date_from = input("Enter Start Date (YYYY-MM-DD): ")
                date_to = input("Enter End Date (YYYY-MM-DD): ")
                datetime.strptime(date_from, "%Y-%m-%d")
                datetime.strptime(date_to, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            plot_average_temperatures_by_country(country_name, date_from, date_to)
        elif choice == "3":
            print("Available years: 2020 to 2025")
            year = int(input("Enter Year (e.g., 2025): "))
            if year < 2020 or year > 2025:
                print("Year out of range. Please enter a year between 2020 and 2025.")
                continue    
            plot_average_annual_precipitation_by_country(year)
        elif choice == "4":
            print("Countries Available: UK, France, Pakistan")
            country_name = input("Enter Country Name: ")
            if country_name not in ["UK", "France", "Pakistan"]:
                print("Country not found. Please try again.")
                continue
            print("Available years: 2020 to 2025")
            year = int(input("Enter Year (e.g., 2025): "))
            if year < 2020 or year > 2025:
                print("Year out of range. Please enter a year between 2020 and 2025.")
                continue
            plot_min_max_mean_temperature_by_city_in_country(country_name, year)
        elif choice == "5":
            print("Countries Available: UK, France, Pakistan")
            country_name = input("Enter Country Name: ")
            if country_name not in ["UK", "France", "Pakistan"]:
                print("Country not found. Please try again.")
                continue
            print("Available years: 2020 to 2025")
            year = int(input("Enter Year (e.g., 2025): "))
            if year < 2020 or year > 2025:
                print("Year out of range. Please enter a year between 2020 and 2025.")
                continue
            plot_min_max_mean_precipitation_by_city_in_country(country_name, year)
        elif choice == "6":
            print("\nScatter Plot Options:")
            print("1. Group by City")
            print("2. Group by Country")
            group_choice = input("Choose grouping (1 or 2): ")

            if group_choice == "1":
                plot_average_temperature_vs_precipitation("city")
            elif group_choice == "2":
                plot_average_temperature_vs_precipitation("country")
            else:
                print("Invalid choice. Please select 1 or 2.")
                continue
        elif choice == "7":
            print("Updating weather data...")
            
            print("Weather data updated successfully.")
        elif choice == "8":
            print("Exiting the menu. Goodbye!")
            break
        else: 
                ('Invalid choice, try again')
                break
        
def display_update_menu():
    while True:
        print("\n=== Weather Data Menu ===")
        print("1. Initialize database")
        print("2. Insert all cities")
        print("3. Update weather data for all cities")
        print("4. Update weather data for a single city")
        print("5. Show row counts per city")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            init_db()
            print("Database initialized.")

        elif choice == "2":
            for city in cities.keys():
                ensure_city(city)
            print("Cities inserted.")

        elif choice == "3":
            for city, coords in cities.items():
                params = {
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "start_date": "2020-01-01",
                    "end_date": "2025-12-15",
                    "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
                    "timezone": coords["tz"],
                }
                update_weather(city, url, params)
                print(f"Weather data for {city} updated successfully!")

        elif choice == "4":
            city_name = input("Enter city name: ")
            if city_name not in cities:
                print("City not found.")
                continue
            coords = cities[city_name]
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": "2020-01-01",
                "end_date": "2025-12-15",
                "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
                "timezone": coords["tz"],
            }
            update_weather(city_name, url, params)
            print(f"Weather data for {city_name} updated successfully!")

        elif choice == "5":
            show_counts()

        elif choice == "6":
            print("Exiting program.")
            break

        else:
            print("Invalid choice, try again.")
        

if __name__ == "__main__":
    main_menu()