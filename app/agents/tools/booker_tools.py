# app/agents/tools/booking_tools.py
from typing import Optional

import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.config import settings


class FlightBookingInput(BaseModel):
    """Input schema for flight booking requests."""

    flight_id: str = Field(..., description="The flight ID to book")
    passenger_name: str = Field(..., description="Passenger name")
    passenger_email: str = Field(..., description="Passenger email address")


class HotelSearchInput(BaseModel):
    """Input schema for hotel search requests."""

    city: str = Field(..., description="City name to search hotels in")
    check_in: Optional[str] = Field(
        None, description="Check-in date in YYYY-MM-DD format (optional)"
    )
    check_out: Optional[str] = Field(
        None, description="Check-out date in YYYY-MM-DD format (optional)"
    )


class HotelBookingInput(BaseModel):
    """Input schema for hotel booking requests."""

    hotel_id: str = Field(..., description="The hotel ID to book")
    guest_name: str = Field(..., description="Guest name")
    guest_email: str = Field(..., description="Guest email address")
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    room_type: str = Field(..., description="Room type (e.g., Standard, Deluxe, Suite)")


@tool("search_hotels", args_schema=HotelSearchInput)
def search_hotels(
    city: str, check_in: Optional[str] = None, check_out: Optional[str] = None
) -> dict:
    """
    Searches for hotels in a city with optional check-in and check-out dates.
    Returns a list of available hotels with their details.
    """
    print(f"--- TOOL CALLED: Searching hotels in {city} ---")
    if check_in:
        print(f"  Check-in: {check_in}")
    if check_out:
        print(f"  Check-out: {check_out}")

    api_url = f"{settings.CONVEX_BASE_URL}/hotels/search"
    params = {"city": city}
    if check_in:
        params["checkIn"] = check_in
    if check_out:
        params["checkOut"] = check_out

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()

        hotels = response.json().get("hotels", [])

        if not hotels:
            return {"available": False, "hotels": []}

        return {"available": True, "hotels": hotels}

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return {"available": False, "hotels": [], "error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {
            "available": False,
            "hotels": [],
            "error": "An internal error occurred.",
        }


@tool("book_flight", args_schema=FlightBookingInput)
def book_flight(flight_id: str, passenger_name: str, passenger_email: str) -> dict:
    """
    Books a flight reservation using the confirmed flight ID.
    Returns booking confirmation with booking ID, reference, seat number, and status.
    """
    print(
        f"--- TOOL CALLED: Booking flight {flight_id} for {passenger_name} ({passenger_email}) ---"
    )

    api_url = f"{settings.CONVEX_BASE_URL}/flights/book"
    payload = {
        "flightId": flight_id,
        "passengerName": passenger_name,
        "passengerEmail": passenger_email,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if result.get("success"):
            booking = result.get("booking", {})
            return {
                "success": True,
                "booking_id": booking.get("bookingId"),
                "booking_reference": booking.get("bookingReference"),
                "seat_number": booking.get("seatNumber"),
                "status": booking.get("status"),
            }

        return {"success": False, "error": "Booking failed"}

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"success": False, "error": "An internal error occurred."}


@tool("book_hotel", args_schema=HotelBookingInput)
def book_hotel(
    hotel_id: str,
    guest_name: str,
    guest_email: str,
    check_in_date: str,
    check_out_date: str,
    room_type: str,
) -> dict:
    """
    Books a hotel reservation using the hotel ID, dates, and room type.
    Returns booking confirmation with booking ID, reference, number of nights, total price, and status.
    """
    print(
        f"--- TOOL CALLED: Booking hotel {hotel_id} for {guest_name} ({guest_email}) ---"
    )
    print(
        f"  Check-in: {check_in_date}, Check-out: {check_out_date}, Room: {room_type}"
    )

    api_url = f"{settings.CONVEX_BASE_URL}/hotels/book"
    payload = {
        "hotelId": hotel_id,
        "guestName": guest_name,
        "guestEmail": guest_email,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "roomType": room_type,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()

        if result.get("success"):
            booking = result.get("booking", {})
            return {
                "success": True,
                "booking_id": booking.get("bookingId"),
                "booking_reference": booking.get("bookingReference"),
                "number_of_nights": booking.get("numberOfNights"),
                "total_price": booking.get("totalPrice"),
                "status": booking.get("status"),
            }

        return {"success": False, "error": "Booking failed"}

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"success": False, "error": "An internal error occurred."}
