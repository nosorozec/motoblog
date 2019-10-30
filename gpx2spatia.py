import xml.etree.ElementTree as ET
import argparse
import sqlite3
import os


#print("Name = {0}, descr={1}".format(trk.find('{http://www.topografix.com/GPX/1/1}name').text, trk.find('{http://www.topografix.com/GPX/1/1}desc').text))
#gpx -> trk ->

#export PYTHONIOENCODING=utf8
#rm /ludwik_spatia.db &&  time python3 gpx2spatia.py gpx/*gpx

# echo "select name, hash, round(st_length(geom,1)/1000,2) from tracks; select round(sum(st_length(geom,1))/1000,2) from tracks;" | spatialite -silent ludwik.db
#
#132984.06

spatia_schema = """
    CREATE TABLE tracks (
    track_uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    start TEXT NOT NULL,
    stop TEXT NOT NULL,
    name TEXT,
    description TEXT,
    hash INTEGER
    );
    SELECT AddGeometryColumn('tracks', 'geom', 4326, 'LINESTRING', 'XY', 1);
    SELECT CreateSpatialIndex('tracks', 'geom');
"""

def db_inserter(conn, c, sql):
    try:
        c.execute(sql)
    except Exception as e:
        print("Exception in SQL query: %s" % e)
    finally:
        conn.commit()


def gpx2sql(conn, c, fname):
    gpx = ET.parse(fname).getroot()
    ns = {'gpx':'http://www.topografix.com/GPX/1/1'}
    #w pętli teorzone są dwa SQL insert - tracks oraz points
    for trk in gpx.findall('gpx:trk', ns):
        if trk.find('gpx:name',ns) is not None:
            trk_name=trk.find('gpx:name',ns).text
        else:
            trk_name = ''
        print("  track {0}".format(trk_name))

        if trk.find('gpx:desc',ns) is not None:
            trk_desc=trk.find('gpx:desc',ns).text
        else:
            trk_desc=''

        trk_start = trk.find('gpx:trkseg/gpx:trkpt/gpx:time',ns).text #znajduję czas pierwszego punktu
        #trk_stop = trk.find('gpx:trkseg[last()]/gpx:trkpt[last()]/gpx:time', ns).text #znajduję czas ostatniego punktu SLOOW
        #trk_hash = hashlib.sha224(ET.tostring(trk)).hexdigest()
        trk_hash = abs(hash(ET.tostring(trk)))
        sql_track_pts = '' #konstruujemy listę punktów
        for trkseg in trk.findall('gpx:trkseg', ns):
            for trkpt in trkseg.findall('gpx:trkpt', ns):
                sql_track_pts += trkpt.get('lon') + " " + trkpt.get('lat')+","
        trk_stop = trkpt.find('gpx:time', ns).text #Ostatni punkt w tracku - pobieram jego czas (dużo szybciej)
        #mamy już wszystkie dane do utworzenia SQL INSERTa
        sql_track = "insert into tracks (track_uid, name, description, start, stop, hash, geom) values (NULL, '"
        sql_track += trk_name + "', '" + trk_desc + "', '" + trk_start + "', '" + trk_stop  + "', '" + str(trk_hash)
        sql_track += "', GeomFromText('LINESTRING(" + sql_track_pts[:-1] + ")\', 4326));"
        db_inserter(conn, c, sql_track)

#parsing the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("gpxfiles", nargs="+", help="list of gpx files to parse")
parser.add_argument("-d", "--db", required=True, help="spatialite database name")
args = parser.parse_args()

#If exist - delete it
if os.path.exists(os.path.realpath(args.db)) is True:
    print("deleting existing database...")
    os.remove(os.path.realpath(args.db))

#connecting fo database and insert schema
conn = sqlite3.connect(os.path.realpath(args.db))
conn.enable_load_extension(True)
conn.execute('SELECT load_extension("mod_spatialite.so")')
conn.execute('SELECT InitSpatialMetaData(1);')
c = conn.cursor()
c.executescript(spatia_schema)

#main loop for porcessing gpx files
for gpxfile in args.gpxfiles:
    print("procesing file {0}".format(gpxfile))
    gpx2sql(conn, c, gpxfile)
