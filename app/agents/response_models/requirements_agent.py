from pydantic import BaseModel, Field
from typing import List, Optional



class TravelerProfile(BaseModel):
    """Traveler profile information."""

    adults: int = Field(..., description="Number of adult travelers")
    children: int = Field(..., description="Number of child travelers")

class AirportInfo(BaseModel):
    """Airport information with city and IATA code."""

    city: str = Field(..., description="City name")
    airport_iata: str = Field(..., description="IATA airport code")

class TripDetails(BaseModel):
    """Trip basic information."""

    type: str = Field(..., description="Trip type: one_way or round_trip")
    origin: AirportInfo = Field(..., description="Origin airport information")
    destination: AirportInfo = Field(..., description="Destination airport information")
    depart_date: str = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: Optional[str] = Field(
        None, description="Return date in YYYY-MM-DD format (for round trips)"
    )

class Preferences(BaseModel):
    """User travel preferences."""

    cabin_class: str = Field(..., description="Cabin class: economy, premium, business")
    non_stop: bool = Field(..., description="Preference for non-stop flights")
    max_layovers: int = Field(..., description="Maximum number of layovers allowed")
    date_flex_days: int = Field(..., description="Date flexibility in days")
    interests: List[str] = Field(..., description="List of travel interests")

class Budget(BaseModel):
    """Budget information."""

    total_currency: str = Field(..., description="Currency code (e.g., USD)")
    total_amount: float = Field(..., description="Total budget amount")
    flights_amount: float = Field(..., description="Budget allocated for flights")
    hotels_amount: float = Field(..., description="Budget allocated for hotels")

class HotelPreferences(BaseModel):
    """Hotel preferences."""

    stars: str = Field(..., description="Star rating range (e.g., 3-4)")
    area: str = Field(..., description="Area preference (e.g., central, quiet)")
    room_type: str = Field(..., description="Room type preference")

class FlightQuery(BaseModel):
    """Flight search query parameters."""

    from_iata: str = Field(..., description="Origin airport IATA code")
    to_iata: str = Field(..., description="Destination airport IATA code")
    date: str = Field(..., description="Flight date in YYYY-MM-DD format")
    passengers: int = Field(..., description="Number of passengers")
    cabin: str = Field(..., description="Cabin class")
    non_stop: bool = Field(..., description="Non-stop preference")

class FlightOption(BaseModel):
    """Individual flight option details."""

    carrier: str = Field(..., description="Airline carrier")
    flight_number: str = Field(..., description="Flight number")
    depart_iso: str = Field(..., description="Departure time in ISO format")
    arrive_iso: str = Field(..., description="Arrival time in ISO format")
    price_usd: float = Field(..., description="Price in USD")

class FlightResult(BaseModel):
    """Flight search result."""

    available: bool = Field(..., description="Whether flights are available")
    top_option: Optional[FlightOption] = Field(
        None, description="Best flight option if available"
    )

class FlightCheck(BaseModel):
    """Flight availability check results."""

    outbound_query: FlightQuery = Field(..., description="Outbound flight search query")
    outbound_result: FlightResult = Field(
        ..., description="Outbound flight search result"
    )
    return_query: Optional[FlightQuery] = Field(
        None, description="Return flight search query (for round trips)"
    )
    return_result: Optional[FlightResult] = Field(
        None, description="Return flight search result (for round trips)"
    )

class UserConfirmations(BaseModel):
    """User confirmation status."""

    accept_outbound_top_option: bool = Field(
        ..., description="Whether user accepts the top outbound option"
    )
    notes: Optional[str] = Field(None, description="Additional user notes")


class MissingInfo(BaseModel):
    """Missing information."""

    missing_info: List[str] = Field(
        ..., description="List of missing or ambiguous fields"
    )
    question: str = Field(
        ..., description="Question to ask the user to provide the missing information"
    )

class CompleteRequirements(BaseModel):
    """
    The final output from the requirements agent when it has gathered all the information from the user and necessary tools calls.
    """

    traveler: TravelerProfile = Field(..., description="Traveler profile information")
    trip: TripDetails = Field(..., description="Trip basic information")
    preferences: Preferences = Field(..., description="User travel preferences")
    budget: Budget = Field(..., description="Budget information")
    hotel_prefs: HotelPreferences = Field(..., description="Hotel preferences")
    flight_check: FlightCheck = Field(
        ..., description="Flight availability check results"
    )
    user_confirmations: UserConfirmations = Field(
        ..., description="User confirmation status"
    )
    missing_info: MissingInfo = Field(..., description="Missing information")


class RequirementsAgentResponseModel(BaseModel):
    requirements: CompleteRequirements = Field(..., description="Complete requirements")