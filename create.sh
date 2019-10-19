#!/bin/bash

apt-get update
apt-get install -y librasterlite2-1 libspatialite-dbg libspatialite7 libsqlite3-mod-rasterlite2 libsqlite3-mod-spatialite spatialite-bin python-pyspatialite python-pip curl xz-utils
pip install gpx2spatialite
#gpx2spatialite create_db moto-gpx.db

DBNAME=ludw-moto.sqlite
[[ -e $DBNAME ]] && rm $DBNAME
[[ -e natural_earth.sqlite.xz ]] || (rm -f ./natural_earth*; curl -LO https://www.gaia-gis.it/gaia-sins/gui2-samples/natural_earth.sqlite && xz natural_earth.sqlite)


#create new db with natural earth and my gpxs files + required tables to enable gpx2spatialite
xzcat natural_earth.sqlite.xz > $DBNAME
curl https://raw.githubusercontent.com/ptrv/gpx2spatialite/master/gpx2spatialite/data/sql/create_db.sql | spatialite $DBNAME
for i in gpx/*gpx
do
  echo y | gpx2spatialite -s -d $DBNAME --user ktm $i
done
