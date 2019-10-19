#!/bin/bash

DBNAME=ludw-moto.sqlite
[[ -e $DBNAME ]] && rm -f $DBNAME
[[ -e natural_earth.sqlite.xz ]] || (rm -f ./natural_earth*; curl -LO https://www.gaia-gis.it/gaia-sins/gui2-samples/natural_earth.sqlite && xz natural_earth.sqlite)

#create new db with natural earth and my gpxs files + required tables to enable gpx2spatialite
xzcat natural_earth.sqlite.xz > $DBNAME
curl https://raw.githubusercontent.com/ptrv/gpx2spatialite/master/gpx2spatialite/data/sql/create_db.sql | spatialite $DBNAME
for i in gpx/*gpx
do
  echo y | gpx2spatialite -s -d $DBNAME --user ktm $i
done
