import json
import time


def search_flights():
    time.sleep(0.2)
    return {"status": "success", "result": "Flight options found"}


def search_hotels():
    time.sleep(0.2)
    return {"status": "success", "result": "Hotel options found"}


def check_weather():
    time.sleep(0.2)
    return {"status": "success", "result": "Weather information retrieved"}


def generate_itinerary():
    time.sleep(0.2)
    return {"status": "success", "result": "3-day travel itinerary generated"}


def main():
    print("Starting AI Travel Planner workflow...")

    results = {
        "request": "Plan a 3-day trip to Goa",
        "steps": [
            {"name": "flight_search", "result": search_flights()},
            {"name": "hotel_search", "result": search_hotels()},
            {"name": "weather_check", "result": check_weather()},
            {"name": "itinerary_generation", "result": generate_itinerary()},
        ],
    }

    print(json.dumps(results, indent=2))
    print("Travel Planner workflow completed successfully.")


if __name__ == "__main__":
    main()
