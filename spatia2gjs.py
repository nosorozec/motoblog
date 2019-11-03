#!/ust/bin/python3

# https://gis.stackexchange.com/questions/142970/dump-a-geojson-featurecollection-from-spatialite-query-with-python
#https://macwright.org/2015/03/23/geojson-second-bite.html#features

import os
import argparse
#import geojson
import sqlite3
import json

#{
#  "type": "Feature",
#  "properties": {
#    "length":600,
#    "name": "ludwik went mad",
#    "descr": "Bardzo fajna przejażdzka, etc, etc. Blery blery",
#    "countries":[['Poland',100], ['Germany',200], ['Czech',300]]
#  },
#  "geometry": {
#    "type":"LineString",
#    "coordinates":[//tablica punktów, punkty to po prostu tablica
#      [23.25111499987542,50.71879399940371],[21.07512499205768,52.16366697102785]
#    ]
#  },
#};


#parsing the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--db", required=True, help="spatialite database name")
args = parser.parse_args()

#creating the databse
conn = sqlite3.connect(os.path.realpath(args.db))
conn.enable_load_extension(True)
conn.execute('SELECT load_extension("mod_spatialite.so")')
c = conn.cursor()



#{
#  "type": "Feature",
#  "geometry": {
#    "type": "Point",
#    "coordinates": [0, 0]
#  },
#  "properties": {
#     "trip": "trip_name"
#    ,"memory": "trip_memory"
#    ,"bike": "trip_bike"
#    ,"countries": [["country1", km1], ["country2", km2]]
#   }
#  }
#}


#hashes = c.execute("select hash from tracks").fetchall()
hashes = c.execute("select hash from tracks where hash='ab76dabe1a71a30ae787148de7ba1e412fa3e886ed18f2bb2f9ea7df'").fetchall()

for hash in hashes:
    (trackStart, trackStop, trackName, trackNote, trackGeom) = c.execute("""
        select start, stop, name, notes, AsGeoJSON(geom) from tracks where hash=?
        """, hash).fetchone()
    #print("track name: {0} countries: ".format(trackBasicks[2]), end="")

    trackCountries = c.execute("""
        SELECT
        b.name AS COUNTRY,
        sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000)) AS ODO
        FROM tracks a, countries b
        WHERE ST_Intersects(a.geom, b.geometry) AND a.hash=?
        GROUP BY COUNTRY
        ORDER BY ODO DESC
    """, hash).fetchall()

    #rozpakowujemy pole notes
    try:
      trackNoteUnpacked=json.loads(trackNote)
    except Exception as e:
      trackNoteUnpacked['memory']=str_json
      trackNoteUnpacked['trip']='Small rides'
      trackNoteUnpacked['bike']='MotoMoto'

    trackNoteUnpacked['countries']=trackCountries

    trackGeojson = {}
    trackGeojson.update({"type":"Feature"})
    #trackGeojson.update({"geometry":json.loads(trackGeom)})
    trackGeojson['properties']=trackNoteUnpacked




    print(json.dumps(trackGeojson, indent=4))
