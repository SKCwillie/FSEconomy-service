# FSEconomy-service
```url
http://api.fseconomy-service.com/
```
This API functions by trying to maximize that amount of data I am able to retrieve via the FSEconomy datafeeds and still stay with the limits of the API keys.
I have essentially tried to optimize my 40 request per 6 hours to build a database of assignment data and a limited number of aircraft.
The aircraft that are supported are available via an endpoint. This allows users of the API to not have to worry about aliases, ids, or spelling.
The ICAOs that are currently supported are large airport in the United States and Canada.
I have requested an API key for developers via the website but have not heard back, hopefully more support will eventually be added.
## Status
Confirm the service is up and running
#### URI
```url
/status
```
#### Method
```method
GET
```
#### Response

```json
{"message": "up"}
```
## Available Aircraft
This will return a list of aircraft that are currently supported by this service. Due to the nature of data retrieval, this is currently limited to 10 aircraft. If you want different aircraft, I suggest pulling the source code and entering the aircraft you like and running the service locally.
#### URI
```url
/aircrafts/jobs/available
```
```method
GET
```
#### Example Response
```json
[
    {
        "id": 55,
        "makeModel": "Beechcraft 18"
    },
    {
        "id": 33,
        "makeModel": "Beechcraft King Air 350"
    },
    {
        "id": 372,
        "makeModel": "Cessna Citation CJ4 (MSFS)"
    },
    {
        "id": 22,
        "makeModel": "Cessna 208 Caravan"
    },
    {
        "id": 214,
        "makeModel": "Cessna 414A Chancellor"
    },
    {
        "id": 45,
        "makeModel": "DeHavilland DHC-6 Twin Otter"
    },
    {
        "id": 345,
        "makeModel": "Douglas DC-6B (PMDG)"
    },
    {
        "id": 363,
        "makeModel": "Socata TBM 930 (MSFS)"
    }
]
```

## Jobs
Jobs are the heart of this API. The Jobs endpoint can be hit by using a supported ICAO or a supported aircraft. Assignments in FSEconomy tend to be unidirectional. My flow for finding assignments involved logging in, searching for an assignment with an aircraft I liked to fly and try to fill it with passengers. I would then have to click another link and determine if the amount of return passengers made the job worthwhile. This endpoint, at it's core, just finds the return passengers without having to manually go to a website and provides the information in a RESTful way.
### Searching by ICAO
#### URI
```url
/jobs/{ICAO}
```
I find this endpoint espeically helpful when using an aircraft I currently own. This allows for quick searching to find assignments that will fill my current aircraft.
#### Method
```method
GET
```
#### Example Response
```json
{
  "KARR": [
    {
      "ToIcao": "KMWC",
      "Distance": 83,
      "Pay": 8595,
      "Amount": 17,
      "UnitType": "passengers",
      "Type": "Trip-Only",
      "ReturnPax": 9
    },
    {
      "ToIcao": "KYIP",
      "Distance": 223,
      "Pay": 1507,
      "Amount": 2,
      "UnitType": "passengers",
      "Type": "Trip-Only",
      "ReturnPax": 9
    }
  ],
  "Rentals": [
    {
      "MakeModel": "Beechcraft 18",
      "SerialNumber": 23605,
      "Equipment": "IFR/AP/GPS",
      "Home": "55J",
      "NeedsRepair": 0,
      "PctFuel": 0.82,
      "Cost": {
        "RentalDry": 438,
        "RentalWet": 643,
        "Bonus": 106
      },
      "EngineTime": "267:24",
      "TimeLast100h": "75:28"
    }
  ]
```
### Searching by Aircraft
#### URI
```url
/jobs/{makeModel}
```

This endpoint should take any of the aliases FSEconomy accepts or the make model. White spaces will need to be sripped from the string before using in the URL. See GET Jobs Aircraft endpoint to see list of currently supported aircraft.
This endpoint returns a Financial object. This takes the cruise speed and fuel of the aircraft according to FSEconomy and calculates a rough estimate for how long the flight will take given the information from the Rental object. This allows the user to quickly find the best assignments for a given aircraft.
#### Method
```method
GET
```
#### Example Response
```json
{
    "DeHavilland DHC-6 Twin Otter": [
        {
            "Job": {
                "FromIcao": "KGAD",
                "ToIcao": "KMAI",
                "Amount": 19,
                "Distance": 193,
                "UnitType": "passengers",
                "ReturnPax": 29,
                "Pay": 11817
            },
            "Rental": {
                "Registration": "N-672LW",
                "Equipment": "IFR/AP/GPS",
                "RentalDry": 723,
                "RentalWet": 1224,
                "Bonus": 235,
                "NeedsRepair": false
            },
            "Financial": {
                "NetPay": 23634.1,
                "PaxTo": 19,
                "PaxFrom": 19,
                "BestRental": "dry",
                "RentalCost": 2109.73,
                "BookingFeeTo": 4490.48,
                "BookingFeeFrom": 4490.48,
                "Earnings": 10180.0,
                "EarningsPerHr": 4039
            }
        },
        {
            "Job": {
                "FromIcao": "PAAQ",
                "ToIcao": "PADQ",
                "Amount": 32,
                "Distance": 253,
                "UnitType": "passengers",
                "ReturnPax": 21,
                "Pay": 9638
            },
            "Rental": {
                "Registration": "N-564PJ",
                "Equipment": "IFR/AP/GPS",
                "RentalDry": 616,
                "RentalWet": 0,
                "Bonus": 0,
                "NeedsRepair": true
            },
            "Financial": {
                "NetPay": 11445.22,
                "PaxTo": 19,
                "PaxFrom": 19,
                "BestRental": "dry",
                "RentalCost": 2355.32,
                "BookingFeeTo": 2174.59,
                "BookingFeeFrom": 2174.59,
                "Earnings": 3596.19,
                "EarningsPerHr": 1115
            }
        },
        {
            "Job": {
                "FromIcao": "PADQ",
                "ToIcao": "PAAQ",
                "Amount": 21,
                "Distance": 253,
                "UnitType": "passengers",
                "ReturnPax": 32,
                "Pay": 6881
            },
            "Rental": {
                "Registration": "N-363XC",
                "Equipment": "IFR/AP/GPS",
                "RentalDry": 700,
                "RentalWet": 1201,
                "Bonus": 235,
                "NeedsRepair": false
            },
            "Financial": {
                "NetPay": 12451.46,
                "PaxTo": 19,
                "PaxFrom": 19,
                "BestRental": "dry",
                "RentalCost": 2626.35,
                "BookingFeeTo": 2365.78,
                "BookingFeeFrom": 2365.78,
                "Earnings": 3848.41,
                "EarningsPerHr": 1193
            }
        },
        {
            "Job": {
                "FromIcao": "PADQ",
                "ToIcao": "PAEN",
                "Amount": 16,
                "Distance": 174,
                "UnitType": "passengers",
                "ReturnPax": 37,
                "Pay": 6263
            },
            "Rental": {
                "Registration": "N-363XC",
                "Equipment": "IFR/AP/GPS",
                "RentalDry": 700,
                "RentalWet": 1201,
                "Bonus": 235,
                "NeedsRepair": false
            },
            "Financial": {
                "NetPay": 13700.4,
                "PaxTo": 16,
                "PaxFrom": 19,
                "BestRental": "dry",
                "RentalCost": 1869.81,
                "BookingFeeTo": 2192.06,
                "BookingFeeFrom": 2603.08,
                "Earnings": 5665.41,
                "EarningsPerHr": 2466
            }
        }
    ]
}
```
## Assignments
Currently a single endpoint that allows for retrieving assignment information from an airport. This requires passing a userKey as a header and will return assignments grouped by ToIcao. Due to the nature of  Jobs only being able to support Large airports, this should help alleviate some issues that occur from not supporting small airports. Your user key will be subject to the normal datafeed limits imposed by FSEconomy.
#### URI
```url
/assignments/(icao)
```
```method
GET
```
#### Example Response
```json
[
    {
        "FromIcao": "3GV",
        "ToIcao": "2MO",
        "Amount": 2,
        "UnitType": "kg",
        "Type": "Trip-Only",
        "Pay": 419.0,
        "Distance": 118.0
    },
    {
        "FromIcao": "3GV",
        "ToIcao": "KAIZ",
        "Amount": 2,
        "UnitType": "passengers",
        "Type": "VIP",
        "Pay": 1805.0,
        "Distance": 96.0
    },
    {
        "FromIcao": "3GV",
        "ToIcao": "KBAD",
        "Amount": 1,
        "UnitType": "passengers",
        "Type": "Trip-Only",
        "Pay": 960.0,
        "Distance": 391.0
    },
    {
        "FromIcao": "3GV",
        "ToIcao": "KDSM",
        "Amount": 5,
        "UnitType": "passengers",
        "Type": "Trip-Only",
        "Pay": 4485.0,
        "Distance": 153.0
    }
]
```




## Other endpoints
This is a collection of URLs that will return data from the FSEconomy Datafeeds. These are provided as a convenience as JSON responses are not available from the datafeeds.

#### All airports
```url
/airports
```

#### Single airport information
```url
/airport/{icao}
```


#### All aircraft
```url
/aircrafts
```

#### All airports
 Will accept integer ID or make model with spaces removed
```url
/airport/{aircraftId}
```
or
```url
/airport/{makeModel}
```



