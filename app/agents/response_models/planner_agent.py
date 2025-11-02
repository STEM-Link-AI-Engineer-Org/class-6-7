from typing import List

from pydantic import BaseModel, Field


class Activity(BaseModel):
    """Individual activity in an itinerary day."""

    name: str = Field(..., description="Name of the activity or attraction")
    type: str = Field(
        ...,
        description="Type of activity: culture, scenic, shopping, food, nature, beaches, adventure, etc.",
    )


class DayItinerary(BaseModel):
    """Itinerary for a single day."""

    date: str = Field(..., description="Date in YYYY-MM-DD format")
    city: str = Field(..., description="City name for this day")
    activities: List[Activity] = Field(
        ..., description="List of 2-3 activities/attractions for this day"
    )


class Itinerary(BaseModel):
    """Complete travel itinerary with day-by-day plan."""

    days: List[DayItinerary] = Field(
        ..., description="List of day itineraries for the trip"
    )


class PlannerAgentResponseModel(BaseModel):
    """Response model for the planner agent."""

    itinerary: Itinerary = Field(..., description="Complete travel itinerary")
