#!/usr/bin/env python3

import unittest
from grammar_model import Vessel, Season, VesselSeason, Location, Hop, Cruise, Leg, Visitation, StaySpec, remove_repeats

class TestLocation(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_location_create(self):
        wlg = Location('wlg', 'Wollongong, NSW', [150.905285, -34.420143])
        print(wlg, wlg.as_geometry())

    def test_hop_create(self):
        wlg = Location('wlg', 'Wollongong, NSW', [150.905285, -34.420143])
        pt_hacking = Location('pthack', 'Port Hacking, NSW', [151.187489, -34.066777])
        hop = Hop(wlg, pt_hacking)
        print(hop, hop.as_geometry())
        print(hop.as_geometry().length)
        print(hop.as_geometry().bounds)

    def test_vessel(self):
        vessel = Vessel('Trilogy', 'SV Trilogy', 'Australia', '807189', 6.5)
        print(vessel)

    def test_season(self):
        season = Season("2020")
        print(season)

    def test_VesselSeason(self):
        
        vessel = Vessel('Trilogy', 'SV Trilogy', 'Australia', '807189', 6.5)
        season = Season("2020")
        vs = VesselSeason(vessel, season)
        print(vs)

    def test_visitation(self):
        ph = Location('pthack', 'Port Hacking, NSW', [151.187489, -34.066777])
        visit = Visitation(ph, None)
        self.assertEqual(visit.location.identifier, "pthack")

    def test_leg_create(self):
        wlg = Location('wlg', 'Wollongong, NSW', [150.905285, -34.420143])
        pt_hacking = Location('pthack', 'Port Hacking, NSW', [151.187489, -34.066777])
        broughton = Location('broughton', 'Broughton Island, NSW', [152.326456, -32.62500])

        cruise = None
        leg = Leg(cruise)
        no_stay = None
        leg.add_visitation(Visitation(wlg, no_stay))
        leg.add_visitation(Visitation(pt_hacking, no_stay))
        leg.add_visitation(Visitation(broughton, StaySpec('days', 3)))
        self.assertEqual(len(leg.visitations), 3)
        self.assertEqual(leg.origin().identifier, 'wlg')
        self.assertEqual(leg.destination().identifier, 'broughton')

        print(leg.as_geometry())


    def test_cruise(self):
        vessel = Vessel('Trilogy', 'SV Trilogy', 'Australia', '807189', 6.5)
        season = Season("2020")
        vs = VesselSeason(vessel, season)

        
        wlg = Location('wlg', 'Wollongong, NSW', [150.905285, -34.420143])
        pt_hacking = Location('pthack', 'Port Hacking, NSW', [151.187489, -34.066777])
        broughton = Location('broughton', 'Broughton Island, NSW', [152.326456, -32.62500])
        cruise = Cruise(vs, name="Cruise to Broghton Island and return", departure_port=wlg)

        no_stay = None
        cruise.add_event(Visitation(wlg, None))
        cruise.add_event(Visitation(pt_hacking, None))
        cruise.add_event(Visitation(broughton, None, stay_spec=StaySpec(3, 'days')))
        self.assertEqual(len(cruise.get_legs()), 1)
        
        print(cruise, cruise.as_geometry())

        vs.add_cruise(cruise)

        print(vs, vs.as_geometry())
        

    def test_remove_repeats(self):
        a = [1, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
        b = remove_repeats(a)
        self.assertEqual(b, [1,2,3,4,5,6,7,8])

    def test_remove_repeats_empty_list(self):
        a = []
        b = remove_repeats(a)
        self.assertEqual(b, a)



if __name__ == '__main__':
    unittest.main()
