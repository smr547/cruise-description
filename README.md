# Cruise description language
A set of tools for captains planning yacht cruises.

## Example

A text-based lauguage to describe a cruise

```

location "Sant Carles de la Rapita, Spain" is abbreviated to SCARLES
location "Tarragona" is abbreviated to TARR
location "Barcelona, Spain" is abbreviated to BARCEL

cruise "2019 Season - Part 1"
    SCARLES
    TARR for 2 nights
    BARCEL
```

## Tools

Tools based on Cruise Definition Language (CDL)

1. CDL -> KML to visualise cruise on Google Earth
1. CDL -> cruise plan (departure/arrival schedule)
1. CDL -> weather outlook
