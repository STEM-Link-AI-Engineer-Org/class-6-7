from pydantic import BaseModel, Field
from typing import Optional


class FlightBookingResult(BaseModel):
    """Flight booking confirmation result."""

    booking_id: str = Field(..., description="Booking ID from the booking system")
    status: str = Field(..., description="Booking status (e.g., confirmed)")
    ticket_ref: str = Field(..., description="Ticket reference number")
    flight_id: str = Field(..., description="Flight ID that was booked")


class HotelBookingResult(BaseModel):
    """Hotel booking confirmation result."""

    booking_id: str = Field(..., description="Booking ID from the booking system")
    status: str = Field(..., description="Booking status (e.g., confirmed)")
    reservation_ref: str = Field(..., description="Reservation reference number")
    hotel_id: str = Field(..., description="Hotel ID that was booked")
    total_price: float = Field(..., description="Total price for the hotel stay")


class Bookings(BaseModel):
    """Container for all booking confirmations."""

    flights: Optional[FlightBookingResult] = Field(
        None, description="Flight booking confirmation if flight was booked"
    )
    hotels: Optional[HotelBookingResult] = Field(
        None, description="Hotel booking confirmation if hotel was booked"
    )


class BookerAgentResponseModel(BaseModel):
    """Response model for the booker agent."""

    bookings: Bookings = Field(..., description="All booking confirmations")
