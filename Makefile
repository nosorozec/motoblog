DBNAME:= ludw.db

db: gpx2spatia.py
	python3 gpx2spatia.py --db $(DBNAME) gpx/*gpx

server:
	python3 -m http.server 9999