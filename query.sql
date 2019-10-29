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