# FSEconomyV2
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
## Jobs
Jobs are the heart of this API. The Jobs endpoint can be hit by using a supported ICAO or a supported aircraft. Assignments in FSEconomy tend to be unidirectional. My flow for finding assignments involved logging in, searching for an assignment with an aircraft I liked to fly and try to fill it with passengers. I would then have to click another link and determine if the amount of return passengers made the job worthwhile. This endpoint, at it's core, just finds the return passengers without having to manually go to a website and provides the information in a RESTful way.
### Searching by ICAO
#### URI
```url
/jobs/{ICAO}
```
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
}
```
