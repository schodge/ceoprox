#!/usr/bin/python3
"""
within_range.py
"""

LAT = 37.5612878
LON = -122.3252377


def within_radius(lat, lon, r=1):
    # http://www.csgnetwork.com/degreelenllavcalc.html
    one_deg_lat_miles = 68.96471148345343
    one_deg_lon_miles = 54.8999549622639
    # Can skip the sqrt, since x <= 1 --> sqrt(x) <= 1
    dist = (((lat - LAT) * one_deg_lat_miles)**2 +
            ((lon - LON) * one_deg_lon_miles)**2)
    print(dist)
    out = True if dist <= 1 else False
    return out
