#!/ust/bin/python3

# https://gis.stackexchange.com/questions/142970/dump-a-geojson-featurecollection-from-spatialite-query-with-python

import os
import argparse
import geojson
import sqlite3

parser = argparse.ArgumentParser()
