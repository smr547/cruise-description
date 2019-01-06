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
A period in which one or more cruises will be conducted in earnest. Has properties:

* Title
* duration (a time interval)

## Cruise
A trip from one major destination to another, involving stopovers along the way for sightseeing and other activities. A
Cruise will typically involve no changes in crew or passengers.

A cruise starts in one Locations, has a series of stopovers, and ends at a final destination (typically a major port or 
marina. It can be viewed as a sequence of legs.

A cruise has attributes:

* Title
* Duration
* Persons on board (collection of Persons)
* Sequence of legs

## Leg
A part of a cruise involving the vessel moving from one stopover location to another (possibly with some intevening 
waypoints). Has properties

* sequence of locations


## Location
A named place or point of interest. Has properties

* id (an arbitrary key uniquely identifying the location)
* shortname (some unique abbreviation of the location name)
* name (fully qualified name of the location)
* position (longitude and latitude)

A Location may be a destination, a place for a planned stopover or simply a point of navigational interst (a waypoint)


## Person
A natural person travelling on board the vessel in the role of  crew member, passenger or guest. Has attributes:

* Name (first, middle, surname)
* Shortname (initials)
* Role
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
