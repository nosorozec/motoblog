DROP table if exists tracks;
CREATE TABLE tracks (
  track_uid SERIAL NOT NULL,
  start TEXT NOT NULL,
  stop TEXT NOT NULL,
  name TEXT,
  description TEXT,
  hash TEXT NOT NULL UNIQUE
);
SELECT AddGeometryColumn('tracks', 'geom', 4326, 'LINESTRING', 2);
