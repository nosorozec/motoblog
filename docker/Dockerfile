FROM ludw/python3

MAINTAINER ludw <ludwikowski@gmail.com>

RUN apt-get update && \
  apt-get install gnupg2

COPY psql/patch /tmp

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main"  > /etc/apt/sources.list.d/pgdg.list

RUN curl -LO https://www.postgresql.org/media/keys/ACCC4CF8.asc && \
  apt-key add ACCC4CF8.asc && \
  rm ACCC4CF8.asc

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    apt-utils dialog librasterlite2-1 libspatialite-dbg libspatialite7 libsqlite3-mod-rasterlite2 libsqlite3-mod-spatialite spatialite-bin curl xz-utils pixz python3 python3-geojson make git ca-certificates vim postgresql-12 postgresql-12-postgis-3 postgresql-12-postgis-3-scripts && \
  curl -LO https://github.com/gohugoio/hugo/releases/download/v0.59.1/hugo_0.59.1_Linux-64bit.deb && \
  dpkg -i ./hugo_0.59.1_Linux-64bit.deb && \
  rm ./hugo_0.59.1_Linux-64bit.deb

EXPOSE 5423
