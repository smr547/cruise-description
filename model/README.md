# CDL data model

The cruise description language (CDL) allows the master of a vessel to describe a planned cruise of a vessel during a
cruising season. This file defines an ontology for cruise  descriptions. 

## Vessel
The vessel to be cruised. Has properties:

* Name
* Country of registration
* Registration number
* LOA
* Displacement
* Draft
* Beam
* Engine details
* Type
* Description

## Season
A period in which one or more cruises will be conducted in earnesti, possibly involving multiple vesses. Has properties:

* Title
* duration (a time interval)

A season includes the cruising of one or more vessels. A single vessel may be cruised for one or more seasons. 

## VesselSeason

Reresents the cruising activities of a single vessel in a single season. 

* identifier (combination of the vessel identifier and season title
* commencement location
* commencement date

## Cruise
A trip from one major destination to another, involving stopovers along the way for sightseeing and other activities. A
Cruise will typically involve no changes in crew or passengers.

A cruise starts in one Locations, has a series of stopovers, and ends at a final destination (typically a major port or 
marina). It can be viewed as a sequence of legs.

A cruise has attributes:

* Title
* Duration
* Persons on board (collection of Persons)
* Sequence of legs

## Leg
A part of a cruise involving the vessel moving from one stopover location to another (possibly with some intevening 
waypoints). Has properties

* depature location
* sequence of visitations (locations) along the way, the last being the destination for the leg
* period (from departure date/time to destination arrival date/time)
* duration (derived from period)

## Visitation 
A planned arrival at a location as part of a Leg of a cruise. Properties are

* Location
* Planned arrival date/time
* Stopover duration (zero for waypoints on the leg)
* description including comments, planned activities and points of interest


## Location
A named place or point of interest. Has properties

* id (an arbitrary key uniquely identifying the location)
* shortname (some unique abbreviation of the location name)
* name (fully qualified name of the location)
* position (longitude and latitude)
* description

A Location may be a destination, a place for a planned stopover or simply a point of navigational interst (a waypoint)

# Crewing

Our system should be able to track the persons on board each vessel at any point in time. Some additional concepts are
therefore required.

## Person
A natural person travelling on board the vessel in the role of  crew member, passenger or guest. Has attributes:

* Name (first, middle, surname)
* Shortname (initials)
* Gender
* Address
* Telephone
* email
* Passport details
** Number
** DOB
** Nationality (country of issue)
** Issue date
** Expiry date

## PersonRole
The concept of a person occupying a role on a vessel for a period of time. Roles may be Passenger, Guest or a Crew Role
(skipper, mate, navigator)

## Compliment
The collections of people on board at any point in time. Each person on board can be identified in a specific Role 
Crew roles include skipper, mate, navigator etc. A person on board may also be a Guest or a Passenger (the latter pay to 
to be transported on board the vessel).

# Other terms that may be of interest

## Route
A sequence of locations representing the planned track of the vessel. If a route is given a name then it could be
considered a "standard route" that could be utilised to describe a Leg simply by adding the time period over which the 
Route is to be traversed.

## Track
The actual path of the vessel across the ground. The track consists of 

* a sequence of Timepoints

Where a Timepoint has properties:

* Date/time 
* Position (long, lat, [alititude])

## Voyage
Synonym for Cruise perhaps

## Passage
May be useful to describe a Leg with duration greater than 12 hours and/or involving nightime sailing.


