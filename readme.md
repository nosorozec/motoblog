
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


```
gpx - root node
  trk - child node
    name - child node
    trkseg - segment track
      trkpt
        time
        lat
```

 create SQL from GPX. Można by użyć do tego gpxpy ale my nie idziemy na łatwiznę. Sami przeorami te XMLe :)

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
