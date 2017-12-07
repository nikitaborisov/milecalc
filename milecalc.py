from geopy import GoogleV3
from geopy.distance import vincenty
from itertools import product
import readline
import re
import sys
import csv

with open('airports.dat.txt') as airfile:
    airports = {r[4]: (float(r[6]),float(r[7])) for r in csv.reader(airfile)
                if r[4]}

def pathcalc(segs):
    total = 0
    for start, end in zip(segs, segs[1:]):
        if start == end:
            return -1 # hack to avoid duplicate airports
        dist = round(vincenty(airports[start.upper()],
                            airports[end.upper()]).miles)
        dist = max(dist, 500)
        total += dist
    return total

def expand_metro(path):
    path = re.sub('WAS', 'BWI/DCA/IAD', path)
    path = re.sub('CHI', 'ORD/MDW', path)
    path = re.sub('NYC', 'LGA/EWR/JFK', path)
    path = re.sub('PAR', 'CDG/ORY', path)
    return path


def paths(pathspec):
    return product(*(seg.split('/') for seg in
                     expand_metro(pathspec).split('-')))

if __name__ == "__main__":
    while True:
        l = input("Path: ")

        for cost, path in sorted((pathcalc(path),path) for path in paths(l.strip())):
            if cost < 0:
                continue
            print("{}: {}".format('-'.join(path),cost))
