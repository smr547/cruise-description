

The production of a cruise schedule or timetable is an important capability of this system.


## Sailing time

The time spent with the vessel on the move.

A Hop represents the planned movement of the vessel from one point to the next without major deviation in course
and certainly without any intervening stopovers.  The sailing time for a Hop (measured in HOURS) can be calculated 
as simply the distance between the end points (in NM) divided by the speed of the vessel (in KTS).

A Leg is simply a series of hops and therefore the sailing time for a leg is the sum of the sailing times of the 
constituent hops.

The aggregate sailing time for a Cruise is the sum of the sailing time of the constituent legs.

If the average speed of the vessel is well known then the computed sailing times should have an uncertainty measured in 
a few hours (for the longest legs) and less for shorter legs.

## Elapsed time

The total time taken to complete a cruise

A cruise is spent either moving along a leg on the planned route or while stationary at a stopover (enjoying the 
local delights). In CDL we try to estimate the time spent at a stopover either in hours (for a brief stopover) 
or one or more nights for a more extended stopover.  The CDL itself allows the cruise planner to enter the 
stopover duration.


## Estimating stopover duration

In order to maintain a precision of a few hours over the extent of a cruise, some logic needs to be applied to compute
the likely duration of each stopover. Given a firm cruise departure date/time, the system will 

* calculate the computed_arrival_time at the destination of the first leg (based on sailing time)
* compute the scheduled_departure_time for the next leg (see logic below)

The process is repeated until the computed_arrival_time at the destination is found. 

## Estimating the scheduled departure date/time for a stopover

The computed arrival time has been calculated and the stopover duration has been specified by the cruise planner, 
our task is to compute the scheduled departure time.

Noting that, in CDL, a stopover duration may be specified in NIGHT(S) or HOURS. If it is not specified a stopover 
of one night is assumed.

The arrival date is the date of the computed arrival time. Add the stopover days to this to get the scheduled departure
date. Apply the scedulted departure time to this date (defaults to 1000 if not specified)

All calculation are done in the local timezone.  Note if the vessel arrives after local midnight, the remaining nightime
hours are NOT regarded as a night.

A stopover duration measured in hours will always be honoured by the system so long as no departure time is specified.
A departure time (whether explicitly specified or computed) after sunset will generate a navigation warning

If no departure time is specified then a departure time of 1000 local is assumed
If no departure time is specified and if the sailing time of the  current leg is estimated to be less than 12 hours 
but greater than 8 hours then an earlier departure time will be computed (this strategy is suggested by the fact
that an arrival before sunset is desired)



## Cruise schedule

The schedule is simply a listing of the arrival and departure events for a Cruise. Based on the CDL description of a
cruise, the system should be able to produce a complete cruise schedule consisting of 

1. Depart Date, time and location
2. Arrival date/time at each stopover 
3. Departure date/time at each stopover
4. Anticipated arrival date/time at the destination

The system should report the total elapsed time for the cruise, the time actually spent sailing/motoring and the
total distance covered.


