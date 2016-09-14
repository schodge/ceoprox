#!/usr/bin/python3
"""
data_collect.py
Copyright Shayne Hodge and SnapLogic Inc, 2016
All parts of the code not under another license are licensed under
a standard 3-clause BSD license.

Library for data collection/formatting from the PostgreSQL DB, using
SnapLogic as an intermediary. Generally useful if you'll be retrieving
data from a db via HTTP using some web server mechanism. Also
shows some use of GeoJSON and pandas. Usable as either a library or as a
script to dump data into files.
"""
from __future__ import division, print_function
import json
import requests
from datetime import datetime
import pandas as pd

GEO_OUT = './gj_new.json'
# It would be good to bring in argparse to pass these command line
WRITE_JSON = False


def get_creds(c_file='./template_creds.json'):
    """Make sure to fill in template_creds.json if you will need it."""
    with open(c_file) as f:
        creds = json.load(f)
    url = creds['url']
    token = creds['token']
    return (url, token)


def get_data_SL(route='B', tbeg='0', tend='0', url='', token='', hours_back=4800):
    """Generic function to create a request to SnapLogic to get data
    back from PostgreSQL. Typical of creating a JSON request to any
    REST-ish (very roughly speaking) API. Note that all args are turned
    into strings. The requests lib is then used to actually post the
    JSON. Wrapper functions are created for more specific requests."""
    # The decision was made to decision this function to return useful
    # data with few arguments, so some fill-in is needed
    tendi = tend if (tend != '0') else datetime.timestamp(datetime.utcnow()) * 1000
    tbeg = tbeg if (tbeg != '0') else str(tendi - (hours_back * 3600 * 1000))
    tend = str(tendi)
    # we keep the creds and url in a separate file for security, best to
    # keep this out of the git repo or at least make sure the file is
    # listed in .gitignore
    if ((url == '') or (token == '')):
        (url_new, token_new) = get_creds()
        url = url if (url != '') else url_new
        token = token if (token != '') else token_new
    data = {"route": route, "tbeg": tbeg, "tend": tend}
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(url, json=data, headers=headers)
    return r.json()


def df_to_geojson(df_g):
    """Pulls lat/lon/time out of a dataframe, and converts into a
    GeoJSON Feature collection. Note the each row becomes part of the
    list in gpart, and then the last step wraps some extra structure
    around that."""
    data = df_g[['lat', 'lon', 'time']].values
    data_list = [[d[0], d[1], d[2]] for d in data]
    gpart = [{"type": "Feature",
              "properties": {"ts": d[2]},
              "geometry": {"type": "Point", "coordinates": [d[0], d[1]]}}
             for d in data_list]
    geojson = {"type": "FeatureCollection", "features": gpart}
    return geojson


def get_batt_data(tbeg='0', tend='0', url='', token=''):
    """Wrapper function for getting battery data. Probably could also
    be done as a partial function application, but done this way in case
    additional processing steps are done, as in the next function."""
    return get_data_SL(tbeg=tbeg, tend=tend, url=url, token=token)


def get_geo_data(tbeg='0', tend='0', url='', token=''):
    data_g = get_data_SL(route='G', token=token, url=url, tend=tend,
                         tbeg=tbeg)
    # Conversion to dataframe for historical reasons and not really
    # necessary, except the downstream functions expect it
    df_g = pd.DataFrame(data_g)
    geojson = df_to_geojson(df_g)
    return geojson


def main():
    # Not all of these vars get used; in practice, main was often
    # commented out and the commands below unindented, and run in an
    # IPython shell.
    (url, token) = get_creds()
    data_b = get_batt_data()
    data_g = get_geo_data()
    df_b = pd.DataFrame(data_b)
    df_g = pd.DataFrame(data_g)
    if WRITE_JSON:
        with open(GEO_OUT, 'w') as f:
            json.dump(data_g, f)


if __name__ == '__main__':
    main()
