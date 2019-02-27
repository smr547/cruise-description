
from model import VesselSeason, Cruise


def schedule_season(vessel_season : VesselSeason):
    '''
    schedule all cruises in the specified vessel's season
    '''
    print("Scheduling vessel/season %s" % (vessel_season.identifier(),))
    print(type(vessel_season.cruises))
    last_cruise = None
    for ci in range(0, len(vessel_season.cruises)):
        c = vessel_season.cruises[ci]
        if ci < len(vessel_season.cruises)-1: 
            next_cruise = vessel_season.cruises[ci+1]
        else:
            next_cruise = None
        schedule_cruise(c, last_cruise, next_cruise)
        last_cruise = c


def schedule_cruise(this_cruise, last_cruise=None, next_cruise=None):
    '''
    schedule the visitations and legs in the specified cruise
    '''
    
    print("    Scheduling cruise %s" % (this_cruise.name,))

    # prior to departure, the vessel is deemed to be at it's "first visitation"
    # the first visitation must correspond to the cruise departure point

    c = this_cruise
    visits = c.get_visitations()
    if c.departure_port is not visits[0].location :
        raise ValueError("Cruise %s must have departure port %s as first visitation" %
            (c.name, c.departure_port.identifier, visits[0].location.identifier))
   
    # the departure datetime is specified in CDL so it take precedence
    # Note that the departure time for the cruise is the departure time for the first visitation
    # therefore we set an arbitrary duration for the first visitation

     
