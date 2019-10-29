import hashlib
import xml.etree.ElementTree as ET
import argparse

# print("Name = {0}, descr={1}".format(trk.find('{http://www.topografix.com/GPX/1/1}name').text, trk.find('{http://www.topografix.com/GPX/1/1}desc').text))
#gpx -> trk ->

def gpx2sql(fname):
    gpx = ET.parse(fname).getroot()
    ns = {'gpx':'http://www.topografix.com/GPX/1/1'}
    #w pętli teorzone są dwa SQL insert - tracks oraz points
    for trk in gpx.findall('gpx:trk', ns):
        if trk.find('gpx:name',ns) is not None:
            trk_name=trk.find('gpx:name',ns).text
        else:
            trk_name = ''

        if trk.find('gpx:desc',ns) is not None:
            trk_desc=trk.find('gpx:desc',ns).text
        else:
            trk_desc=''

        trk_start = trk.find('gpx:trkseg/gpx:trkpt/gpx:time',ns).text #znajduję czas pierwszego punktu
        #trk_stop = trk.find('gpx:trkseg[last()]/gpx:trkpt[last()]/gpx:time', ns).text #znajduję czas ostatniego punktu SLOOW
        trk_hash = hashlib.sha224(ET.tostring(trk)).hexdigest()
        sql_track_pts = '' #konstruujemy listę punktów
        for trkseg in trk.findall('gpx:trkseg', ns):
            for trkpt in trkseg.findall('gpx:trkpt', ns):
                sql_track_pts += trkpt.get('lon') + " " + trkpt.get('lat')+","
        trk_stop = trkpt.find('gpx:time', ns).text #Ostatni punkt w tracku - pobieram jego czas (dużo szybciej)
        #mamy już wszystkie dane do utworzenia SQL INSERTa
        sql_track = "insert into tracks (track_uid, name, description, start, stop, hash, geom) values (NULL, '"
        sql_track += trk_name + "', '" + trk_desc + "', '" + trk_start + "', '" + trk_stop  + "', '" + trk_hash
        sql_track += "', GeomFromText('LINESTRING(" + sql_track_pts[:-1] + ")\', 4326));"
        return(sql_track)


parser = argparse.ArgumentParser()
parser.add_argument("gpxfiles", nargs="+", help="list of gpx files to parse")
args = parser.parse_args()
for gpxfile in args.gpxfiles:
    print(gpx2sql(gpxfile))
