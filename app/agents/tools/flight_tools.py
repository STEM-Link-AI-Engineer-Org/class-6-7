# app/tools/flight_tools.py
import requests

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.config import settings


class FlightSearchInput(BaseModel):
    """Input schema for flight search requests."""

    origin: str = Field(
        ..., description="The IATA code for the origin airport (e.g., 'CMB')."
    )
    destination: str = Field(
        ..., description="The IATA code for the destination airport (e.g., 'BKK')."
    )


@tool("search_flight_availability", args_schema=FlightSearchInput)
def search_flight_availability(origin: str, destination: str) -> dict:
    """
    Checks if flights are available on a given date between two airports.
    Returns a small list of candidate options sorted by price.
    Only call this after you have the origin, destination, and date.
    """
    print(f"--- TOOL CALLED: Searching flights from {origin} to {destination} ---")

    api_url = f"{settings.CONVEX_BASE_URL}/flights/search"
    params = {"origin": origin, "destination": destination}

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors

        flights = response.json().get("flights", [])

        if not flights:
            return {"available": False, "options": []}

        return {"available": True, "options": flights}

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return {"available": False, "options": [], "error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {
            "available": False,
            "options": [],
            "error": "An internal error occurred.",
        }
