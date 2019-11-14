FROM ludw/python3

MAINTAINER ludw <ludwikowski@gmail.com>

RUN apt-get update && \
  apt-get install gnupg2

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main"  > /etc/apt/sources.list.d/pgdg.list

RUN curl -LO https://www.postgresql.org/media/keys/ACCC4CF8.asc && \
  apt-key add ACCC4CF8.asc

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    apt-utils dialog librasterlite2-1 libspatialite-dbg libspatialite7 libsqlite3-mod-rasterlite2 libsqlite3-mod-spatialite spatialite-bin curl xz-utils pixz python3 python3-geojson make git ca-certificates vim postgresql-11 && \
  curl -LO https://github.com/gohugoio/hugo/releases/download/v0.59.1/hugo_0.59.1_Linux-64bit.deb && \
  dpkg -i ./hugo_0.59.1_Linux-64bit.deb
