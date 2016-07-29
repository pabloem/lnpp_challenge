#!/usr/bin/env python
import sys
import openpyxl as opx
import csv
import re

usage = "./limpiar.py infile.xlsx outfile.csv [start-row [header-list]]"
comments = """\tstart-row - Linea donde empiezan los datos. Default es 1
\theader-list - Lista de encabezados en el archivo, separados por comas. Sin espacios. Default:
  numero,refugio,municipio,direccion,uso,servicios,capacidad,latitud,longitud,altitud,responsable,telefono
"""

# Un renglon valido tiene cuando mucho dos valores faltantes
def valid_row(row, headers):
    values = sum(1 for a in row if a.value != '' and a.value is not None)
    return True if values > len(headers) - 2 else False

def transform_coord(x):
    spl = re.sub('([0-9]+)[^0-9]+([0-9]{2})[^0-9]+([0-9."]*[0-9])[^0-9]?',
                 '\\1 \\2 \\3',x).strip().split()
    res = sum(float(re.sub('[^0-9]','.',i))/60**ex for ex,i in enumerate(spl))
    return res

def transform_if_number(x):
    try:
        return int(x)
    except:
        return x.strip().encode('utf-8') if x is not None else None

f_transf = {
    'latitud': lambda x : transform_coord(x),
    'longitud': lambda x : transform_coord(x),
    'default': lambda x : transform_if_number(x)
}

start_row = 1

if len(sys.argv) < 3:
    print usage 
    print comments 
    sys.exit(1)

if len(sys.argv) > 3:
    start_row = int(sys.argv[3])

headers = ['numero','refugio','municipio','direccion','uso','servicios',
           'capacidad','latitud','longitud','altitud','responsable','telefono']

if len(sys.argv) > 4:
    headers = [a for a in sys.argv[4].split(',')]

wb = opx.load_workbook(sys.argv[1])

snames = wb.get_sheet_names()

out_rows = []
for sn in snames:
    sheet = wb.get_sheet_by_name(sn)
    i = start_row

    while len(sheet.rows) > i:
        rw = sheet.rows[i]
        i += 1
        if not valid_row(rw, headers):
            continue
        next_row = {hd:f_transf.get(hd,f_transf['default'])(val.value) 
                                            for hd,val in zip(headers,rw)}
        out_rows.append(next_row)

outf = open(sys.argv[2],'w')
wr = csv.DictWriter(outf,headers)
wr.writeheader()
wr.writerows(out_rows)
outf.close()

