FROM ubuntu:18.04

MAINTAINER ludw <ludwikowski@gmail.com>

RUN apt-get update && \
  apt-get install -y librasterlite2-1 libspatialite-dbg libspatialite7 libsqlite3-mod-rasterlite2 libsqlite3-mod-spatialite spatialite-bin \
    python-pyspatialite python-pip curl xz-utils pixz && \
  pip install gpx2spatialite
