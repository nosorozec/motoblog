
# Moto blog

1. prepare raw gpx files
1. import do spatialite
1. query the data with Spatial SQL (SQL with spatial extension)
 * https://en.wikipedia.org/wiki/SQL_syntax
 * https://en.wikipedia.org/wiki/Spatial_database
 * https://en.wikipedia.org/wiki/Spatial_query
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


```sql
SELECT
 strftime('%Y', a.timestamp_start) AS YEAR
 b.name AS COUNTRY,
 sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000)) AS ODO
FROM tracklines a, countries b
WHERE ST_Intersects(a.geom, b.geometry)
GROUP BY YEAR
ORDER BY Odo DESC;


SELECT b.name, sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000))
FROM tracklines a, states_provinces b
WHERE ST_Intersects(a.geom, b.geometry)
GROUP BY b.name;

```

#Baza wyjazdów

1. każdy ślad: trk/trkseg/trkpt
1. jakiś pomysł na logiczne wiązanie wyjazdów?
