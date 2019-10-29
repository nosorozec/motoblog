--Create DB schemas
-- bike -> file

BEGIN TRANSACTION;
--
--CREATE TABLE bikes (
--  bike_uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--  bikename TEXT NOT NULL,
--  UNIQUE (username)
--);
--
--CREATE TABLE files (
--  file_uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--  filename TEXT NOT NULL,
--  md5hash TEXT NOT NULL,
--  date_entered TEXT NOT NULL,
--  first_timestamp TEXT,
--  last_timestamp TEXT,
--  user_uid INTEGER NOT NULL,
--  FOREIGN KEY (user_uid) REFERENCES users (user_uid),
--  UNIQUE (md5hash)
--);
--
CREATE TABLE tracks (
  track_uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  start TEXT NOT NULL,
  stop TEXT NOT NULL,
  name TEXT,
  description TEXT,
  hash TEXT NOT NULL UNIQUE
);

--https://www.gaia-gis.it/spatialite-3.0.0-BETA/spatialite-cookbook/html/new-geom.html
SELECT AddGeometryColumn('tracks', 'geom', 4326, 'LINESTRING', 'XY', 1);
SELECT CreateSpatialIndex('tracks', 'geom');

COMMIT;
