# Things to do 

A list of things to do for this project

## Crew recording

To factilitate the tracking of crew and guests on board during the cuise

1. Implement a grammar to capture ``Person`` details including a shortname identifier for each person (and full name,
address contact, passport, etc).
1. Update the Cdl cruise description to allow implement ``Crew XYZ join`` or ``Crew XYX depart`` statements

## Cabin allocations
1. Facilitate cabin allocation (Ontology may need updating)
1. Vessel description needs to define available cabins
1. Assignement to cabin as part of ``Crew xxx join`` statement
1. Need to work out a way to do cabin change

## Crew role
1. Facilitate allocation of role(s) to crew members
1. Ontology will need updating
1. Vessel description needs to define required and optional roles
1. Need to work out a way to do role changes

## Descriptions
Things need general descriptions to help flesh out the cruise plan. Descriptions and notes should be applied to

* Locations
* Visitations
* Legs and hops
* Persons
* Vessels

Descriptions should be displayed as popups when clicked or hovered in a Google Earth display. Descriptions should allow
for the inclusion of URL links and other markup. Perhaps we should adopt markdown as a standard for Description text.
Descriptive text for things like Locations could be included in a separate file so that it can be updated independently 
and allowed to evolve over time.


# Cruise timing

A big and important topic. The system should be able to calculate and display/print a timetable for the cruise given:

* a proposed departure date/time
* average cruising speed (define as a property of the Vessel)
* stopover duration for each location (visitation) along the way
* some assumptions about time of depature from each stopover location

Cruise timing is driven to a large extent by the need to be in a certain place at a certain time to have crew/guests 
join or depart. These ``crew change timepoints`` are usually fixed well in advanced of the cruise to allow people to
book flights and make other travel arrangements. As such, they are firm commitments given by the skipper to be in 
a certain place at a certain time. Failure to meet these commitments, without good reason, may cause inconvenience 
to the crew.

So key requirements are:

1. The system should be able to specify crew change commitments  (at a specific times and locations)
1. hightlight crew change commitments in all output
1. warn where the calculated timetable for a cruise does not permit a commitment to be met


