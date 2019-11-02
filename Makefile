dbName = ludw.db
dockerImage = "ludw/spatialite:devel"
httpdPort = 9999
sqlCheckQuery = "select name, hash, round(st_length(geom,1)/1000,2) from tracks; select round(sum(st_length(geom,1))/1000,2) from tracks;"


#robię target db aby się łatwo pisało
#ale i tak wygląda, że make bierze pierwszy target
#i go wykonuje - więc mogę napisać
# make
# make db
# make ludw.db
#wszystko daje taki sam efekt

db: $(dbName)

$(dbName): gpx2spatia.py $(wildcard /*gpx) clean
	PYTHONIOENCODING=utf8 python3 gpx2spatia.py --db $(dbName) gpx/*gpx
	echo $(sqlCheckQuery) | spatialite -silent $(dbName)

.PHONY: docker server clean db run

run:
	docker run --rm -it -p $(httpdPort):$(httpdPort) -v $(CURDIR):/motoblog $(dockerImage) bash -l

server:
	python3 -m http.server 9999

docker:
	docker rmi $(dockerImage) | true
	cd docker && docker build . -t $(dockerImage)

clean:
	# pipe to true to continue even if error
	rm $(dbName) | true
