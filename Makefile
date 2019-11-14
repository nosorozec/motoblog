spatiaDB = /usr/bin/spatialite
dbName = ludw.db
dockerImage = "ludw/spatialite:devel"
httpdPort = 9999
naturalEarth = $(wildcard natural_earth/*sql.gz)
gpxFiles = $(wildcard gpx/*gpx)
sqlCheckQuery = "select name, hash, round(st_length(geom,1)/1000,2) from tracks; select round(sum(st_length(geom,1))/1000,2) from tracks;"


#robię target db aby się łatwo pisało
#ale i tak wygląda, że make bierze pierwszy target
#i go wykonuje - więc mogę napisać
# make
# make db
# make ludw.db
#wszystko daje taki sam efekt

db: $(dbName)

$(dbName): gpx2spatia.py $(gpxFiles) $(naturalEarth)
	rm $(dbName) | true
	PYTHONIOENCODING=utf8 python3 gpx2spatia.py --db $(dbName) $(gpxFiles)
	for i in $(naturalEarth); do \
		zcat $$i | $(spatiaDB) $(dbName); \
	done
	echo $(sqlCheckQuery) | $(spatiaDB) -silent $(dbName)

.PHONY: docker server clean db run

run:
	docker run --rm -it -p $(httpdPort):$(httpdPort) -v $(CURDIR):/motoblog $(dockerImage) bash -l

server:
	python3 -m http.server 9999

docker:
	docker rmi $(dockerImage) | true
	cd docker
	#in docker catalog!!!
	[[ ! -e ACCC4CF8.asc ]] && curl -LO https://www.postgresql.org/media/keys/ACCC4CF8.asc
	docker build . -t $(dockerImage)

clean:
	# pipe to true to continue even if error
	rm $(dbName) | true
