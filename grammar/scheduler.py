
from grammar_model import VesselSeason, Cruise, Hop, Warning, CrewEvent, Visitation
from datetime import datetime, timedelta, time


def schedule_season(vessel_season : VesselSeason):
    '''
    schedule all cruises in the specified vessel's season
    '''
    all_events = [] 
    last_cruise = None
    for ci in range(0, len(vessel_season.cruises)):
        c = vessel_season.cruises[ci]
        if ci < len(vessel_season.cruises)-1: 
            next_cruise = vessel_season.cruises[ci+1]
        else:
            next_cruise = None
        schedule_cruise(c, last_cruise, next_cruise)
        last_cruise = c
        all_events.extend(c.events)

    # allocate CrewEvents to cabins and check crew movement date

    cabins = vessel_season.vessel.cabins
    current_visitation = None
    for ei in range(0, len(all_events)):
        event = all_events[ei]
        if isinstance(event, Visitation):
            current_visitation = event

        if isinstance(event, CrewEvent):
            # print("processing ", event)
            person = event.person
            cabin = event.cabin

            # find the last cabin event for this person

            if cabin is None:
                # print("Bactracking to find cabin for  ", event)
                for i in range(ei-1, -1, -1):
                    this_event = all_events[i]

                    # print("Examining ", this_event)
                    if isinstance(this_event, CrewEvent) and this_event.join_not_leave and this_event.person == person:
                        cabin = this_event.cabin
                        break

                if cabin is None:
                    raise Exception("Unknown cabin allocation for %s" % 
                        (person.identifier))
                event.cabin = cabin

            cabin.crew_events.append(event)

            # check the date is reasonable with the current visitation

            if not current_visitation.includes_date(event.scheduled().date()):
                current_visitation.add_warning(Warning("Crew movement for %s schedule for %s is not in %s visitation period (%s)" %
                    (event.person.identifier, event.scheduled().strftime("%d/%m/%y"), current_visitation.location.identifier, current_visitation.period_str())))
            


def schedule_cruise(this_cruise, last_cruise=None, next_cruise=None):
    '''
    schedule the visitations and legs in the specified cruise
    '''
    # prior to departure, the vessel is deemed to be at it's "first visitation"
    # the first visitation must correspond to the cruise departure point

    c = this_cruise
    visits = c.get_visitations()
    if c.departure_port is not visits[0].location :
        raise ValueError("Cruise %s must have departure port %s as first visitation (not %s)" %
            (c.name, c.departure_port.identifier, visits[0].location.identifier))
   
    # the departure datetime is specified in CDL so it take precedence
    # Note that the departure time for the cruise is the departure time for the first visitation
    # therefore we set an arbitrary duration for the first visitation

    dv = visits[0]  # departure visitation
    dv.set_arrival_dt(c.get_departure_dt())
    dv.set_computed_duration(timedelta(0))

    # consider each subsequent visitation in turn
    default_departure_time = time(hour=10)
    speed_KTS = c.vesselSeason.vessel.speed_kts
    current_vi = 1
    while current_vi < len(visits) :
        last_v = visits[current_vi-1]
        v = visits[current_vi] 
        h = Hop(last_v.location, v.location)
        duration = timedelta(hours=h.distance_NM()/speed_KTS)

        arrival = last_v.get_departure_dt() + duration
        arrival = arrival.astimezone(v.location.get_timezone())
        v.set_arrival_dt(arrival)

        # if this visitation is a waypoint there is no stay duration

        if v.is_stopover():
            this_planned_stopover_duration = v.get_planned_duration_td()
            next_departure = arrival + this_planned_stopover_duration
            next_departure = datetime.combine(next_departure.date(), default_departure_time)
            next_departure = v.location.get_timezone().localize(next_departure)
            duration = next_departure - arrival
        else:
            duration = timedelta(0)
        
        v.set_computed_duration(duration)
        current_vi += 1

    # clear all warnings
    for v in visits:
        v.clear_warnings()

    # consider each leg
    for leg in c.legs:

        # nightime departure

        v = leg.visitations[0]
        departure_dt = v.get_departure_dt()
        if departure_dt is not None:
            departure_time = departure_dt.time()
            if departure_time < time(hour=6) or departure_time > time(hour=18):
                leg.add_warning(Warning("Nightime departure"))

        
        v = leg.visitations[-1]
        arrival_dt = v.get_arrival_dt()

        # check for overnight passage

        if arrival_dt.date() != departure_dt.date():
            leg.add_warning(Warning("Overnight passage"))

        # nightime arrival?
        arrival_time = arrival_dt.time()
        if arrival_time < time(hour=6) or arrival_time > time(hour=18):
            leg.add_warning(Warning("Nightime arrival"))

    # consider the final arrival_dt in relation to the scheduled departure of the next cruise
    # WARNING if arrival at destination is AFTER scheduled departure

    if next_cruise is not None:
        if arrival_dt > next_cruise.get_departure_dt():
            leg.add_warning(Warning("Arrival in %s is AFTER schedule departure for %s" % (
                v.location.identifier, 
                next_cruise.get_destination_port().identifier)))
        else:

            # WARNING if arrival date/time does not allow specified stopover period
            td = next_cruise.get_departure_dt().date() - arrival_dt.date()
            days_at_destination = round(td.total_seconds()/86400.0)
            planned_stay_days = v.duration_days
            if days_at_destination < planned_stay_days:
                leg.add_warning(Warning("Late arrival in %s allows only %d days stay (not %d as planned)" % (
                    v.location.identifier, 
                    days_at_destination,
                    planned_stay_days)))

            elif days_at_destination > planned_stay_days:
                leg.add_warning(Warning("Early arrival in %s means a %d days stay (not %d as planned)" % (
                    v.location.identifier,
                    days_at_destination,
                    planned_stay_days)))
