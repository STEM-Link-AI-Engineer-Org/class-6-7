# Convex API Endpoints

This section provides with all the convex API Endpoints to interact with the airline booking database

### General

1. Check All city and Country Mappings:

```bash
curl -X GET https://standing-fish-574.convex.site/admin/usage-stats
```

```bash
{
  "stats": {
    "availableCountries": [
      {
        "code": "JP",
        "name": "Japan"
      },
      ...
    ],
    "citiesByCountry": {
      "China": 3,
      "India": 2,
      ...
    },
    "hotelsByCountry": {
        "China": 25,
        "India": 14,
        ...
    },
    "totalCities": 20,
    "totalCountries": 10,
    "totalFlightBookings": 0,
    "totalFlights": 270,
    "totalHotelBookings": 0,
    "totalHotels": 155
  }
}
```

2. Get All Cities:

```bash
curl -X GET https://standing-fish-574.convex.site/reference/cities
```

```bash
{
  "cities": [
    {
      "_creationTime": 1758944679147.96,
      "_id": "jx78sn8mn52zghht6gajrmbwrn7rd74h",
      "airportCode": "NRT",
      "country": "Japan",
      "countryCode": "JP",
      "countryId": "k1742ss7s5p06whfhbdqdzn5v97rdez7",
      "isCapital": true,
      "name": "Tokyo"
    },
    ...
  ]
}
```

3. Get All Countries:

```bash
curl -X GET https://standing-fish-574.convex.site/reference/countries
```

```bash
{
  "countries": [
    {
      "_creationTime": 1758944679147.96,
      "_id": "k1742ss7s5p06whfhbdqdzn5v97rdez7",
      "code": "JP",
      "currency": "JPY",
      "name": "Japan",
      "region": "Asia",
      "timezone": "Asia/Tokyo"
    },
    ...
  ]
}
```

4. Get All Flight Routes country to country:

```bash
curl -X GET https://standing-fish-574.convex.site/reference/routes
```

```bash
{
  "routes": [
    {
      "destination": "ICN",
      "origin": "NRT"
    },
    ...
  ]
}
```

5. Get All Flight Bookings Made:

```bash
curl -X GET https://standing-fish-574.convex.site/bookings/flights
```

```bash
{
  "bookings": [
    {
      "_creationTime": 1758950089474.97,
      "_id": "k5790qjf1w8qywbc3rtwhrcp257rc615",
      "bookingDate": 1758950089475,
      "bookingReference": "FL50089475",
      "currency": "USD",
      "flight": {
        "_creationTime": 1758949497662.85,
        "_id": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
        "aircraft": "Airbus A350",
        "airline": "Cathay Pacific",
        "arrivalTime": "12:15",
        "availableSeats": 186,
        "currency": "USD",
        "departureTime": "06:45",
        "destination": "Seoul",
        "destinationCityId": "jx71bgsyd3yb1v3bnf6rga4ren7rcw2y",
        "duration": 419,
        "flightDate": "2025-11-15",
        "flightNumber": "CA2264",
        "origin": "Tokyo",
        "originCityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
        "price": 505
      },
      "flightId": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
      "passengerEmail": "john@example.com",
      "passengerName": "John Doe",
      "seatNumber": "22E",
      "status": "confirmed",
      "totalPrice": 505,
      "userId": "kn7d18wewdrz8e6xqsj067pf2s7rchp3"
    }
  ]
}
```

6. Get All Hotel Bookings Made:

```bash
curl -X GET https://standing-fish-574.convex.site/bookings/hotels
```

```bash
{
  "bookings": [
    {
      "_creationTime": 1758950660837.06,
      "_id": "kd71h5rq6p867jetph3b6948js7rcfjv",
      "bookingDate": 1758950660840,
      "bookingReference": "HT50660840",
      "checkInDate": "2026-02-15",
      "checkOutDate": "2026-02-18",
      "currency": "USD",
      "guestEmail": "john@example.com",
      "guestName": "John Doe",
      "hotel": {
        "_creationTime": 1758949497662.94,
        "_id": "kh7a1eeczs6yratwvyv05sj0997rda9k",
        "address": "30 Main Street, NRT",
        "amenities": [
          "WiFi",
          "Pool",
          "Gym",
          "Spa",
          "Restaurant",
          "Bar",
          "Room Service",
          "Concierge",
          "Business Center"
        ],
        "availableRooms": 16,
        "city": "Tokyo",
        "cityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
        "country": "Japan",
        "currency": "USD",
        "description": "Luxury 4-star hotel in the heart of the city with modern amenities and excellent service.",
        "name": "Hilton NRT 1",
        "pricePerNight": 360,
        "starRating": 4
      },
      "hotelId": "kh7a1eeczs6yratwvyv05sj0997rda9k",
      "numberOfNights": 3,
      "roomType": "Deluxe",
      "status": "confirmed",
      "totalPrice": 1080,
      "userId": "kn7d18wewdrz8e6xqsj067pf2s7rchp3"
    }
  ]
}
```

7. Get All Flight and Hotel Bookings done under a particular user

```bash
curl -X GET https://standing-fish-574.convex.site/bookings/user?email=john@example.com
```

```bash
{
  "flightBookings": [
    {
      "_creationTime": 1758950089474.97,
      "_id": "k5790qjf1w8qywbc3rtwhrcp257rc615",
      "bookingDate": 1758950089475,
      "bookingReference": "FL50089475",
      "currency": "USD",
      "flight": {
        "_creationTime": 1758949497662.85,
        "_id": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
        "aircraft": "Airbus A350",
        "airline": "Cathay Pacific",
        "arrivalTime": "12:15",
        "availableSeats": 186,
        "currency": "USD",
        "departureTime": "06:45",
        "destination": "Seoul",
        "destinationCityId": "jx71bgsyd3yb1v3bnf6rga4ren7rcw2y",
        "duration": 419,
        "flightDate": "2025-11-15",
        "flightNumber": "CA2264",
        "origin": "Tokyo",
        "originCityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
        "price": 505
      },
      "flightId": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
      "passengerEmail": "john@example.com",
      "passengerName": "John Doe",
      "seatNumber": "22E",
      "status": "confirmed",
      "totalPrice": 505,
      "userId": "kn7d18wewdrz8e6xqsj067pf2s7rchp3"
    }
  ],
  "hotelBookings": [
    {
      "_creationTime": 1758950660837.06,
      "_id": "kd71h5rq6p867jetph3b6948js7rcfjv",
      "bookingDate": 1758950660840,
      "bookingReference": "HT50660840",
      "checkInDate": "2026-02-15",
      "checkOutDate": "2026-02-18",
      "currency": "USD",
      "guestEmail": "john@example.com",
      "guestName": "John Doe",
      "hotel": {
        "_creationTime": 1758949497662.94,
        "_id": "kh7a1eeczs6yratwvyv05sj0997rda9k",
        "address": "30 Main Street, NRT",
        "amenities": [
          "WiFi",
          "Pool",
          "Gym",
          "Spa",
          "Restaurant",
          "Bar",
          "Room Service",
          "Concierge",
          "Business Center"
        ],
        "availableRooms": 16,
        "city": "Tokyo",
        "cityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
        "country": "Japan",
        "currency": "USD",
        "description": "Luxury 4-star hotel in the heart of the city with modern amenities and excellent service.",
        "name": "Hilton NRT 1",
        "pricePerNight": 360,
        "starRating": 4
      },
      "hotelId": "kh7a1eeczs6yratwvyv05sj0997rda9k",
      "numberOfNights": 3,
      "roomType": "Deluxe",
      "status": "confirmed",
      "totalPrice": 1080,
      "userId": "kn7d18wewdrz8e6xqsj067pf2s7rchp3"
    }
  ],
  "user": {
    "_id": "kn7d18wewdrz8e6xqsj067pf2s7rchp3",
    "email": "john@example.com",
    "name": "John Doe"
  }
}
```

### Flights

1. Get All Flights:

```bash
curl -X GET https://standing-fish-574.convex.site/flights
```

```bash
{
  "flights": [
    {
      "_creationTime": 1758949497662.85,
      "_id": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
      "aircraft": "Airbus A350",
      "airline": "Cathay Pacific",
      "arrivalTime": "12:15",
      "availableSeats": 187,
      "currency": "USD",
      "departureTime": "06:45",
      "destination": {
        "airport": "ICN",
        "city": "Seoul",
        "country": "South Korea"
      },
      "destinationCityId": "jx71bgsyd3yb1v3bnf6rga4ren7rcw2y",
      "duration": 419,
      "flightDate": "2025-11-15",
      "flightNumber": "CA2264",
      "origin": {
        "airport": "NRT",
        "city": "Tokyo",
        "country": "Japan"
      },
      "originCityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
      "price": 505
    },
    ...
  ]
}
```

2. Search a particular Flight:

- Requires providing the `origin` and `destination` search parameters
- Optionally a `date` parameters can be used in the request url as `date=2024-02-15`

```bash
https://standing-fish-574.convex.site/flights/search?origin=NRT&destination=ICN
```

```bash
{
  "flights": [
    {
      "_creationTime": 1758949497662.85,
      "_id": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
      "aircraft": "Airbus A350",
      "airline": "Cathay Pacific",
      "arrivalTime": "12:15",
      "availableSeats": 187,
      "currency": "USD",
      "departureTime": "06:45",
      "destination": {
        "airport": "ICN",
        "city": "Seoul",
        "country": "South Korea"
      },
      "destinationCityId": "jx71bgsyd3yb1v3bnf6rga4ren7rcw2y",
      "duration": 419,
      "flightDate": "2025-11-15",
      "flightNumber": "CA2264",
      "origin": {
        "airport": "NRT",
        "city": "Tokyo",
        "country": "Japan"
      },
      "originCityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
      "price": 505
    },
    ...
  ]
}
```

3. Book a Flight:

```bash
curl -X POST "https://standing-fish-574.convex.site/flights/book" \
  -H "Content-Type: application/json" \
  -d '{
    "flightId": "k973gxt3x05h5f42zh4vp6gva17rcxv4",
    "passengerName": "John Doe",
    "passengerEmail": "john@example.com"
  }'
```

```bash
{
  "success":true,
  "booking":{
    "bookingId":"k5790qjf1w8qywbc3rtwhrcp257rc615",
    "bookingReference":"FL50089475",
    "seatNumber":"22E",
    "status":"confirmed"
  }
}
```

### Hotels

1. Get All Hotels:

```bash
curl -X GET https://standing-fish-574.convex.site/hotels
```

```bash
{
  "hotels": [
    {
      "_creationTime": 1758949497662.92,
      "_id": "kh7fwtt847vjz257rmgf2ehy057rcdcz",
      "address": "792 Main Street, BKK",
      "airportCode": "BKK",
      "amenities": [
        "WiFi",
        "Pool",
        "Gym",
        "Spa",
        "Restaurant",
        "Bar",
        "Room Service"
      ],
      "availableRooms": 52,
      "city": "Bangkok",
      "cityId": "jx791kh0mhbr7km68ae37tjc1x7rcr02",
      "country": "Thailand",
      "currency": "USD",
      "description": "Luxury 4-star hotel in the heart of the city with modern amenities and excellent service.",
      "name": "Shangri-La BKK 1",
      "pricePerNight": 180,
      "starRating": 4
    },
    ...
  ]
}
```

2. Search a particular Hotel:

- Requires providing the `city` search parameter
- Optionally `checkIn` and `checkOut` parameters can be used in the request url as `checkIn=2024-02-15&checkOut=2024-02-18`

```bash
curl -X GET https://standing-fish-574.convex.site/hotels/search?city=Tokyo
```

```bash
{
  "hotels": [
    {
      "_creationTime": 1758949497662.94,
      "_id": "kh7a1eeczs6yratwvyv05sj0997rda9k",
      "address": "30 Main Street, NRT",
      "airportCode": "NRT",
      "amenities": [
        "WiFi",
        "Pool",
        "Gym",
        "Spa",
        "Restaurant",
        "Bar",
        "Room Service",
        "Concierge",
        "Business Center"
      ],
      "availableRooms": 17,
      "city": "Tokyo",
      "cityId": "jx7cpghz14tqdcwzbdj0vayeth7rc9bn",
      "country": "Japan",
      "currency": "USD",
      "description": "Luxury 4-star hotel in the heart of the city with modern amenities and excellent service.",
      "name": "Hilton NRT 1",
      "pricePerNight": 360,
      "starRating": 4
    },
    ...
  ]
}
```

3. Book a Hotel:

```bash
curl -X POST "https://standing-fish-574.convex.site/hotels/book" \
  -H "Content-Type: application/json" \
  -d '{
    "hotelId": "kh7a1eeczs6yratwvyv05sj0997rda9k",
    "guestName": "John Doe",
    "guestEmail": "john@example.com",
    "checkInDate": "2026-02-15",
    "checkOutDate": "2026-02-18",
    "roomType": "Deluxe"
  }'
```

```bash
{
  "success":true,
  "booking":{
    "bookingId":"kd71h5rq6p867jetph3b6948js7rcfjv",
    "bookingReference":"HT50660840",
    "numberOfNights":3,
    "status":"confirmed",
    "totalPrice":1080
  }
}
```
