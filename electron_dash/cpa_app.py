"""
Copyright Shayne Hodge and SnapLogic Inc, 2016
All parts of the code not under another license are licensed under
a standard 3-clause BSD license.

cpa_app.py

This flask app is setup to retrieve data from a PSQL db
behind a firewall exposed via a SnapLogic pipeline providing a
REST-ish interface, using the functions from data_collect.py. However,
as noted in that file, those functions are easily adaptable to any DB
accessed via HTTP.

The functions are in place to use sqlite3 locally to
store location information to show how this could be implemented.
"""

from flask import Flask, request, jsonify, g
from data_collect import get_batt_data, get_geo_data
import sqlite3


app = Flask(__name__)
# Turn this off in production!!
app.debug = True
DATABASE = './db/cellular.db'
SCHEMA_FILE = './cpa_schema.sql'

# See http://flask.pocoo.org/docs/0.11/patterns/sqlite3/
# On first run, create the schema as follows from a python shell
# >>> from cpa_app import init_db
# >>> init_db()


def dict_factory(cursor, row):
    """Taken straight from the Python docs to make each row a dict:
    https://docs.python.org/3.5/library/sqlite3.html """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA_FILE, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def db_insert(query, args=()):
    get_db().execute(query, args)
    g._database.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/batt', methods=['GET'])
def battery():
    return get_batt_data()


@app.route('/loc', methods=['GET'])
def loc():
    return get_geo_data()


@app.route('/store_batt_sqlite', methods=['POST'])
def sqlite_batt_store():
    content = request.json
    device = content['coreid']
    ts = content['published_at']
    cap = content['data'][2:]
    with app.app_context():
        db_insert("INSERT INTO battery (device, ts, capacity) VALUES "
                  "(?, ?, ?)", (device, ts, cap))
    return "battery data inserted"


@app.route('/store_loc_sqlite', methods=['POST'])
def sqlite_loc_store():
    """ This function is unfinished, and needs the variables properly
    mapped. """
    content = request.json
    device = content['coreid']
    ts = content['published_at']
    """
    lat = content['']
    lon = content['']
    """
    with app.app_context():
        db_insert("INSERT INTO position (device, ts, lat, lon) VALUES "
                  "(?, ?, ?, ?)", (device, ts, lat, lon))
    return "location data inserted"


@app.route('/read_batt_sqlite', methods=['GET'])
def sqlite_batt_read():
    with app.app_context():
        batt = query_db('SELECT * FROM battery')
    return jsonify(batt)


@app.route('/read_geo_sqlite', methods=['GET'])
def sqlite_loc_read():
    with app.app_context():
        loc = query_db('SELECT * FROM position')
    return jsonify(loc)


if __name__ == '__main__':
    app.run(debug=True)
