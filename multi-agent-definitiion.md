# 🧭 AI Travel Planner and Booker — Architecture Specification

## 1. Single Agent Specification (Requirements Agent)

### **Scope**
A **Requirements-Gathering Agent** implemented as a standalone LangGraph node/subgraph that can be reused independently or as part of a larger multi-agent system. It interviews the user to capture all inputs needed to plan a trip later. It does **not** create itineraries — it validates and verifies flight availability for provided dates.

---

### **Architecture Concept**

The Requirements Agent is implemented as:
- **Standalone Graph**: Can be used independently to gather requirements
- **Reusable Subgraph**: Can be embedded as a node in the larger travel system graph
- **Interrupt-Based Flow**: Uses LangGraph interrupts to pause execution and ask users for missing information

**Graph Flow**:
```
Start → RequirementsAgent Node → [Missing Info?] → Ask User (Interrupt) → RequirementsAgent Node → End
                                                      ↓ (Complete)
                                                     End
```

---

### **Functional Requirements**

1. **Collect & confirm**:
   - Traveler profile (adults, children)
   - Trip basics (origin/destination airports, trip type, dates)
   - Preferences (cabin class, non-stop preference, max layovers, date flexibility, interests)
   - Budget (total, flights, hotels, currency)
   - Hotel preferences (star range, area, room type)

2. **Validate**:
   - Dates (ISO `YYYY-MM-DD`)
   - Origin ≠ destination
   - Departure ≤ return (for round-trip)
   - At least one traveler

3. **Search flights**: Invoke `search_flight_availability` tool when origin/destination airports are known

4. **Confirm selections**: Present top flight option and get user confirmation

5. **Output**: Structured response model containing all requirements

---

### **System Prompt (Summarized)**

*Note: The actual prompt is more detailed with dynamic information gathering strategies. This is a conceptual summary.*

```
You are a Requirements-Gathering Agent for a travel assistant.
Your job is to intelligently gather all required information to complete a user's travel request.

Core Workflow:
1. Analyze initial query - identify what's provided, what's missing
2. Dynamically gather missing information with targeted questions
3. Search for flights when airports are known (using search_flight_availability tool)
4. Present flight options and get user confirmation
5. Handle missing information gracefully using interrupt mechanism

Key Fields to Collect:
- Traveler profile, trip basics, preferences, budget, interests, hotel preferences

Validation Rules:
- ISO date formats (YYYY-MM-DD)
- Departure ≤ return for round-trip
- Origin ≠ destination
- Traveler counts ≥ 1
```

---

### **Tools**

#### **search_flight_availability**

**Purpose**: Checks flight availability between two airports

**Arguments**:
- `origin` (str): IATA code for origin airport (e.g., "CMB")
- `destination` (str): IATA code for destination airport (e.g., "BKK")

**Tool Response**:
```json
{
  "available": true,
  "options": [
    {
      "id": "FL-CMB-BKK-1",
      "carrier": "DemoAir",
      "from": "CMB",
      "to": "BKK",
      "depart_iso": "2025-11-10T09:10:00+05:30",
      "arrive_iso": "2025-11-10T14:35:00+07:00",
      "price_usd": 245.00,
      "flight_number": "DA123"
    }
  ]
}
```

**When to Call**: After origin and destination airports are known from user input.

---

### **Agent Response Structure**

The Requirements Agent outputs a structured response model:

```json
{
  "requirements": {
    "traveler": {
      "adults": 1,
      "children": 0
    },
    "trip": {
      "type": "round_trip",
      "origin": {
        "city": "Colombo",
        "airport_iata": "CMB"
      },
      "destination": {
        "city": "Bangkok",
        "airport_iata": "BKK"
      },
      "depart_date": "2025-11-10",
      "return_date": "2025-11-15"
    },
    "preferences": {
      "cabin_class": "economy",
      "non_stop": false,
      "max_layovers": 1,
      "date_flex_days": 0,
      "interests": ["food", "culture"]
    },
    "budget": {
      "total_currency": "USD",
      "total_amount": 1200,
      "flights_amount": 700,
      "hotels_amount": 500
    },
    "hotel_prefs": {
      "stars": "3-4",
      "area": "central",
      "room_type": "double"
    },
    "flight_check": {
      "outbound_query": {
        "from_iata": "CMB",
        "to_iata": "BKK",
        "date": "2025-11-10",
        "passengers": 1,
        "cabin": "economy",
        "non_stop": false
      },
      "outbound_result": {
        "available": true,
        "top_option": {
          "carrier": "DemoAir",
          "flight_number": "DA123",
          "depart_iso": "2025-11-10T09:10:00+05:30",
          "arrive_iso": "2025-11-10T14:35:00+07:00",
          "price_usd": 245.0
        }
      },
      "return_query": {
        "from_iata": "BKK",
        "to_iata": "CMB",
        "date": "2025-11-15",
        "passengers": 1,
        "cabin": "economy",
        "non_stop": false
      },
      "return_result": {
        "available": true,
        "top_option": {
          "carrier": "DemoAir",
          "flight_number": "DA456",
          "depart_iso": "2025-11-15T10:00:00+07:00",
          "arrive_iso": "2025-11-15T14:30:00+05:30",
          "price_usd": 245.0
        }
      }
    },
    "user_confirmations": {
      "accept_outbound_top_option": true,
      "accept_return_top_option": true,
      "notes": "Okay with 1 layover if cheaper"
    },
    "missing_info": {
      "missing_info": [],
      "question": ""
    }
  }
}
```

**State Key**: `requirements` (dict containing the complete requirements structure)

---

## 2. Multi-Agent Architecture

### **Overview**

LangGraph orchestration of three agents in a sequential pipeline:

| Agent | Function | Key Output | State Key |
|-------|----------|------------|-----------|
| RequirementsAgent | Collects structured requirements (reusable subgraph) | Complete requirements dict | `state["requirements"]` |
| PlannerAgent | Generates day-by-day itinerary via web search | Itinerary with activities | `state["itinerary"]` |
| BookerAgent | Confirms flight and hotel bookings | Booking confirmations | `state["bookings"]` |

---

### **1️⃣ RequirementsAgent (Reusable Subgraph)**

> **Purpose**: Collect structured requirements and verify flight availability  
> **Implementation**: Implemented as a standalone LangGraph that can be invoked as a subgraph node  
> **Produces**: `state["requirements"]` dict following the complete requirements schema

**System Prompt**: See Single Agent Specification above (summarized version)

**Tools**:
- `search_flight_availability` (origin, destination)

**Output**: Complete requirements dict as shown in Single Agent Specification

**Reusability Concept**: The requirements gathering graph is implemented separately and can be:
- Used standalone for requirements collection
- Embedded as a subgraph node in the main travel system graph
- Handles its own interrupt loop internally before returning complete requirements

---

### **2️⃣ PlannerAgent**

> **Purpose**: Generate a day-by-day itinerary based on user requirements  
> **Does NOT**: Book flights or hotels

#### **System Prompt (Summarized)**

*Note: The actual prompt includes detailed workflow for analyzing requirements, web searching, and creating balanced itineraries.*

```
You are a Planner Agent for a travel assistant.
Your job is to take user requirements (destination, dates, interests, budget) and produce a lightweight day-by-day itinerary.

Core Workflow:
1. Analyze requirements - identify destination, dates, interests
2. Use web search tool to find 2-3 points of interest per day matching user interests
3. Create day-by-day itinerary with date, city, and activities
4. Each activity should have name and type (culture, scenic, shopping, food, nature, etc.)

Key Principles:
- Use web search to find real, relevant activities
- Match activities to user interests
- Keep activities realistic and doable within a day
- Do not book anything - only plan
```

#### **Tools**

##### **web_search**

**Purpose**: Search the web for travel information, attractions, POIs, and activities

**Arguments**:
- `query` (str): Search query string (e.g., "Bangkok cultural attractions", "Seoul food tours")

**Tool Response**: 
- Returns search results as text from DuckDuckGo search
- Agent parses results to extract relevant POIs and activities

**When to Call**: For each day, search for activities matching user interests and destination city.

---

#### **Agent Response Structure**

```json
{
  "itinerary": {
    "days": [
      {
        "date": "2025-11-10",
        "city": "Bangkok",
        "activities": [
          {
            "name": "Grand Palace",
            "type": "culture"
          },
          {
            "name": "Chao Phraya river cruise",
            "type": "scenic"
          },
          {
            "name": "Street food tour",
            "type": "food"
          }
        ]
      },
      {
        "date": "2025-11-11",
        "city": "Bangkok",
        "activities": [
          {
            "name": "Chatuchak Market",
            "type": "shopping"
          },
          {
            "name": "Wat Pho Temple",
            "type": "culture"
          }
        ]
      }
    ]
  }
}
```

**State Key**: `itinerary` (dict containing the itinerary structure)

---

### **3️⃣ BookerAgent**

> **Purpose**: Confirm travel reservations (flights and hotels) based on requirements and itinerary  
> **Does NOT**: Create itineraries or search for activities

#### **System Prompt (Summarized)**

*Note: The actual prompt includes detailed workflow for extracting booking information and calling booking tools.*

```
You are a Booker Agent for a travel assistant.
Your job is to confirm travel reservations based on the itinerary and requirements provided.

Core Workflow:
1. Analyze requirements and itinerary to extract booking information
2. Book flight using confirmed flight ID from requirements
3. Search for hotels if needed, then book hotel using hotel ID
4. Return booking confirmations for both flight and hotel

Key Principles:
- Use confirmed flight ID from requirements for flight booking
- Extract passenger/guest info from requirements
- Extract dates from itinerary or requirements
- Only use booking tools - do not search manually
- Return booking confirmations only
```

#### **Tools**

##### **book_flight**

**Purpose**: Books a flight reservation using the confirmed flight ID

**Arguments**:
- `flight_id` (str): The flight ID to book (from requirements)
- `passenger_name` (str): Passenger name
- `passenger_email` (str): Passenger email address

**Tool Response**:
```json
{
  "success": true,
  "booking_id": "BK-FLT-123",
  "booking_reference": "TKT-778899",
  "seat_number": "12A",
  "status": "CONFIRMED"
}
```

**When to Call**: After requirements are complete and flight ID is confirmed.

---

##### **search_hotels**

**Purpose**: Searches for hotels in a city with optional check-in and check-out dates

**Arguments**:
- `city` (str): City name to search hotels in
- `check_in` (str, optional): Check-in date in YYYY-MM-DD format
- `check_out` (str, optional): Check-out date in YYYY-MM-DD format

**Tool Response**:
```json
{
  "available": true,
  "hotels": [
    {
      "id": "HT-BKK-1",
      "name": "Royal Orchid Demo",
      "stars": 4,
      "price_usd_per_night": 58,
      "address": "123 Sukhumvit Rd, Bangkok"
    }
  ]
}
```

**When to Call**: Before booking hotel if hotel ID is not already in requirements.

---

##### **book_hotel**

**Purpose**: Books a hotel reservation using hotel ID, dates, and guest information

**Arguments**:
- `hotel_id` (str): The hotel ID to book
- `guest_name` (str): Guest name
- `guest_email` (str): Guest email address
- `check_in_date` (str): Check-in date in YYYY-MM-DD format
- `check_out_date` (str): Check-out date in YYYY-MM-DD format
- `room_type` (str): Room type (e.g., "Standard", "Deluxe", "Suite")

**Tool Response**:
```json
{
  "success": true,
  "booking_id": "BK-HTL-456",
  "booking_reference": "RES-2025-001",
  "number_of_nights": 5,
  "total_price": 290.00,
  "status": "CONFIRMED"
}
```

**When to Call**: After hotel search or when hotel ID is available from requirements.

---

#### **Agent Response Structure**

```json
{
  "bookings": {
    "flights": {
      "booking_id": "BK-FLT-123",
      "status": "CONFIRMED",
      "ticket_ref": "TKT-778899",
      "flight_id": "FL-CMB-BKK-1"
    },
    "hotels": {
      "booking_id": "BK-HTL-456",
      "status": "CONFIRMED",
      "reservation_ref": "RES-2025-001",
      "hotel_id": "HT-BKK-1",
      "total_price": 290.00
    }
  }
}
```

**State Key**: `bookings` (dict containing flight and hotel booking confirmations)

---

### **LangGraph Orchestration**

**Graph Structure**:
```
Start 
  → requirements_subgraph (Requirements Agent as subgraph)
  → planner (Planner Agent)
  → booker (Booker Agent)
  → End
```

**Shared State**:
```python
{
  "messages": [...],           # Conversation messages
  "requirements": {...},        # Complete requirements dict
  "itinerary": {...},           # Day-by-day itinerary dict
  "bookings": {...}             # Flight and hotel booking confirmations
}
```

**Node Responsibilities**:
- `requirements_subgraph`: Invokes standalone requirements graph, handles interrupt loop internally, returns complete requirements
- `planner`: Receives requirements, generates itinerary using web search
- `booker`: Receives requirements and itinerary, books flights and hotels

---

### **API Endpoints (Mock Services)**

The tools call REST API endpoints to access flight and hotel data:

#### **Flight API**

**GET /flights/search**
- Query params: `origin` (IATA), `destination` (IATA)
- Response: List of available flights with ID, carrier, times, price

**POST /flights/book**
- Body: `flightId`, `passengerName`, `passengerEmail`
- Response: Booking confirmation with booking ID, reference, status

#### **Hotel API**

**GET /hotels/search**
- Query params: `city`, `checkIn` (optional), `checkOut` (optional)
- Response: List of available hotels with ID, name, stars, price

**POST /hotels/book**
- Body: `hotelId`, `guestName`, `guestEmail`, `checkInDate`, `checkOutDate`, `roomType`
- Response: Booking confirmation with booking ID, reference, total price, status

---

### **MVP Implementation Concepts**

1. **Modular Agent Design**: Each agent is implemented as a separate LangChain agent with its own tools and response model

2. **Reusable Subgraph Pattern**: Requirements gathering is a standalone graph that can be:
   - Used independently
   - Embedded as a subgraph node in the main travel system

3. **Structured Outputs**: Each agent uses Pydantic response models to ensure consistent, validated outputs

4. **Tool-Based Architecture**: Agents interact with external services (flight/hotel APIs, web search) through tools, not direct API calls

5. **State Management**: LangGraph manages state flow between agents, with each agent reading from and writing to shared state

6. **Interrupt Handling**: Requirements subgraph uses LangGraph interrupts to pause and collect user input when information is missing

---

### **Summary of Response Structures**

| Agent | State Key | Structure | Purpose |
|-------|-----------|-----------|---------|
| RequirementsAgent | `requirements` | CompleteRequirements dict | Stores all user requirements, flight search results, confirmations |
| PlannerAgent | `itinerary` | Itinerary with days and activities | Day-by-day plan with POIs matching user interests |
| BookerAgent | `bookings` | Bookings with flight and hotel confirmations | Booking IDs, references, and status for both reservations |
