
# Moto blog

1. prepare raw gpx files
1. import do spatialite
1. query the data with Spatial SQL (SQL with spatial extension)
 * https://en.wikipedia.org/wiki/SQL_syntax
 * https://en.wikipedia.org/wiki/Spatial_database
 * https://en.wikipedia.org/wiki/Spatial_query
 * https://www.slideshare.net/shawty_ds/what-is-spatial-sql
1. main queries
 * Intersects(geometry, geometry) : boolean
 * Length(geometry) : number
 * Distance(geometry, geometry) : number
 * Equals(geometry, geometry) : boolean
 * Disjoint(geometry, geometry) : boolean
 * Touches(geometry, geometry) : boolean
 * Crosses(geometry, geometry) : boolean
 * Overlaps(geometry, geometry) : boolean
 * Contains(geometry, geometry) : boolean
 * Area(geometry) : number
 * Centroid(geometry) : geometry
1. create docker image
```
 docker build -t ludw/spatialite:devel .
```

https://www.marksmath.org/classes/Spring2016NumericalAnalysis/demos/ImportGPX.html
https://docs.python.org/3/library/xml.etree.elementtree.html


gpx - root node
  trk - child node
    name - child node


gpx = ET.parse('sample.gpx').getroot()
for trk in gpx.findall('trk'):
  print("Name = {0}, descr={1}".format(trk.find('name').text, trk.find('desc').text))
  for trkseg in trk.findall('trkseg'):
    for trkpt in trkseg.findall('trkpt'):
      print(trkpt.get('lat'))


import xml.etree.ElementTree as ET
gpx = ET.parse('gpx/20191026-Zamosc.gpx').getroot()
for trk in gpx.findall('{http://www.topografix.com/GPX/1/1}trk'):
  print("Name = {0}, descr={1}".format(trk.find('{http://www.topografix.com/GPX/1/1}name').text, trk.find('{http://www.topografix.com/GPX/1/1}desc').text))
  for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
    sql="LINESTRING("
    for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
      sql += trkpt.get('lat') + " " + trkpt.get('lon')+","
    sql = sql[:-1]+")"

lxml -> create SQL from GPX. Można by użyć do tego gpxpy ale my nie idziemy na łatwiznę. Sami przeorami te XMLe :)


https://gis.stackexchange.com/questions/228966/how-to-properly-get-coordinates-from-gpx-file-in-python
from lxml import etree
NSMAP = {"gpx": "http://www.topografix.com/GPX/1/1"}
tree = etree.parse("St_Louis_Zoo_sample.gpx")
for elem in tree.findall("gpx:wpt", namespaces=NSMAP):
     print elem.attrib['lon'], elem.attrib['lat']

from lxml import etree
NSMAP = {"gpx": "http://www.topografix.com/GPX/1/1"}
gpxfile = etree.parse("/motoblog/gpx/20191026-Zamosc.gpx")


<trk> - root node
 <name> - element



```sql
--w jakich województwach byłem w Polsce i ile w nich zrobiłem kilometrów
SELECT
 b.gn_name AS WOJEW,
 sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000)) AS ODO
FROM tracklines a, states_provinces b
WHERE b.admin='Poland' AND ST_Intersects(a.geom, b.geometry)
GROUP BY WOJEW
ORDER BY ODO DESC;

-- ile kilometrów zrobiłem w jakich krajach?
SELECT
 b.name AS COUNTRY,
 sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000)) AS ODO
FROM tracklines a, countries b
WHERE ST_Intersects(a.geom, b.geometry)
GROUP BY COUNTRY
ORDER BY ODO DESC;

-- ile kilometrów zrobiłem w jakich latach?
SELECT
 strftime('%Y', timestamp_start) AS YEAR,
 SUM(round(length_m/1000,2)) AS LENGTH,
 SUM(round(ST_LENGTH(geom,1)/1000,2)) AS Calculated
FROM tracklines
GROUP BY YEAR;
```

#Baza wyjazdów

1. każdy ślad: trk/trkseg/trkpt (obecne rozwiązanie `gpx2spatialite` nie obsługuje plików GPX bez daty - mam takie w 2018 roku z powodów błędów w Garmin Basecamp)
1. jakiś pomysł na logiczne wiązanie wyjazdów?
