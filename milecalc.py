from geopy import GoogleV3
from geopy.distance import vincenty
from functools import lru_cache
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
        dist = int(vincenty(airports[start.upper()],
                            airports[end.upper()]).miles)
        dist = max(dist, 500)
        total += dist
    return total

def expand_metro(path):
    path = re.sub('WAS', 'BWI/DCA/IAD', path)
    path = re.sub('CHI', 'ORD/MDW', path)
    path = re.sub('NYC', 'LGA/EWR/JFK', path)
    return path


def paths(pathspec):
    return product(*(seg.split('/') for seg in
                     expand_metro(pathspec).split('-')))

if __name__ == "__main__":
    while True:
        l = input("Path: ")
        if '/' in l:
            l = re.sub('WAS', 'BWI/DCA/IAD', l)
            l = re.sub('CHI', 'ORD/MDW', l)
            segs = [alts.split('/') for alts in re.split(r'[-=]', l.strip())]
            print(segs)
            paths = [(pathcalc(path),path) for path in product(*segs)]
            for cost, path in sorted(paths):
                print(cost,path)
                print("{}: {}".format('-'.join(path),cost))
            continue
        paths = l.strip().split(',')
        total = 0
        for p in paths:
            psum = 0
            print("Path:", p)
            double = False
            if p[-1] == '*':
                double = True
                p = p[:-1]
            segs = re.split(r'([-=])', p)
            for i in range(0,len(segs)-2,2):
                start = airports[segs[i].upper()]
                end = airports[segs[i+2].upper()]
                dist = int(vincenty(start, end).miles)
                dist = max(dist, 500)
                if double:
                    dist = dist*2
                if segs[i+1] == '=':
                    dist = dist*2
                if i > 0:
                    print(" + ", end='')
                print("{}[{}]".format(''.join(segs[i:i+3]), dist), end='')
                psum += dist
            print(" = {}".format(psum))
            total += psum
        print("Total: {}".format(total))
