
SELECT b.name, sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000)) FROM tracklines a, countries b WHERE ST_Intersects(a.geom, b.geometry) group by b.name;


SELECT  b.name, sum(round(ST_LENGTH(ST_Intersection(a.geom, b.geometry),1)/1000)) FROM tracklines a, states_provinces b WHERE ST_Intersects(a.geom, b.geometry) group by b.name;



#Baza wyjazdów

1. każdy ślad: trk/trkseg/trkpt
1. jakiś pomysł na logiczne wiązanie wyjazdów?
