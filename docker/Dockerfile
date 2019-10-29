FROM ubuntu:18.04

MAINTAINER ludw <ludwikowski@gmail.com>

# obawiam się, że brakuje tutaj python3

RUN apt-get update && \
  apt-get install -y --no-install-recommends librasterlite2-1 libspatialite-dbg libspatialite7 libsqlite3-mod-rasterlite2 libsqlite3-mod-spatialite spatialite-bin curl xz-utils pixz && \
