#!/usr/bin/env python
import csv
from geopy.distance import great_circle
import sys
import re

usage = "tres_centros.py infile.csv lat long"
comment = """\tinfile.csv - La base de datos con informacion de centros de acopio
\tlat - Latitud del ciudadano que busca un centro. Formato decimal o en GMS.
\tlong - Longitud del ciudadano que busca un centro con direccion OESTE como positiva. Decimal o GMS.
"""

# Transforma una coordenada que viene en modo decimal o GMS.
def transform_coord(x):
    try: # Intentamos modo decimal
        return float(x)
    except: # Si no, intentamos modo GMS
        spl = re.sub('([0-9]+)[^0-9]+([0-9]{2})[^0-9]+([0-9."]*[0-9])[^0-9]?',
                     '\\1 \\2 \\3',x).strip().split()
        res = sum(float(re.sub('[^0-9]','.',i))/60**ex 
                            for ex,i in enumerate(spl))
        return res

def coord_distance(x,y):
    return great_circle(x,y).kilometers

def print_center(c, dist):
    print("A {:.2f} kilometros:".format(dist))
    print(c['refugio'])
    print(c['direccion'])
    print('Capacidad: {}. Responsable: {}.\nTelefono: {}.'
          .format(c['capacidad'].encode('utf-8'),
                  c['responsable'].encode('utf-8'),
                  c['telefono'].encode('utf-8')))
    print('Lat: {:.4f}, Long: {:.4f}'.format(float(c['latitud']),
                                             float(c['longitud'])))
    print("")

if len(sys.argv) < 4:
    print(usage)
    print(comment)
    sys.exit(1)

centers = None
with open(sys.argv[1]) as f:
    centers = map(lambda x: {k:e.decode('utf-8') for k,e in x.items()},
                  list(csv.DictReader(f)))
centers = filter(lambda x: x.get('latitud') is not None and x.get('longitud') is not None,
                 centers)

lat = transform_coord(sys.argv[2])
long = transform_coord(sys.argv[3])

sorted_cents = sorted(centers, 
                      key = lambda x: coord_distance(
                                               (transform_coord(x['latitud']), 
                                                transform_coord(x['longitud'])),
                                               (lat,long)))

print("Centros de acopio mas cercanos: ")
for c in sorted_cents[0:3]:
    ds = coord_distance((transform_coord(c['latitud']),
                         transform_coord(c['longitud'])),
                        (lat,long))
    print_center(c, ds)
