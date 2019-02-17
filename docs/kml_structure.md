# KML structure

This document describes the mapping between model objects and KML features

## File becomes a KML document

The ``CDL`` file being processed results in the production of a single KML file. The to level ``Document`` contains
all features generated from the ``CDL`` file.

## Locations to Placemarks

Each ``Location`` defined in the input ``CDL file`` result in the generation of a ``Placemark`` within a ``Location Folder``
at the top level of the ``Document``. Three subfolders are created

* ``Stopovers`` containing placemarks that are mentioned as stopovers in one or more cruise definitions
* ``Waypoints`` containing placemarks which are visited as part of a cruise but are not stopovers
* ``Interests`` containing locations that are not mentioned in a cruise definition but may be of interest (nearby locations
that could be accessed by land)

The ``Stopover`` folder is marked as visible by default. The remaining folders have visibility turned off.

## Season becomes a folder

The ``Season`` definition results in a ``Folder`` of the same name. This folder contains all the cruises

## Cruise to Folder

Each ``Cruise`` becomes a ``Folder`` in the ``Season Folder``.  The folder description will contain a summary of the 
Cruise including

* Start and end dates
* Time duration
* Distance covered in NM
* Names of crew involved


