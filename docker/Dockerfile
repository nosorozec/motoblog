FROM ubuntu:18.04

MAINTAINER ludw <ludwikowski@gmail.com>

# obawiam się, że brakuje tutaj python3

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    apt-utils dialog librasterlite2-1 libspatialite-dbg libspatialite7 libsqlite3-mod-rasterlite2 libsqlite3-mod-spatialite spatialite-bin curl xz-utils pixz python3 python3-geojson make git ca-certificates vim && \
  curl -LO https://github.com/gohugoio/hugo/releases/download/v0.59.1/hugo_0.59.1_Linux-64bit.deb && \
  dpkg -i ./hugo_0.59.1_Linux-64bit.deb
