# Desafio LNPP
Autor: Pablo Estrada <polecito.em (a) gmail>

Este proyecto resuelve el problema de encontrar los tres centros
de acopio mas cercanos para un poblador del estado de Nayarit.

Para obtener instrucciones sobre como correr cada script, es 
posible correrlos *sin argumentos*.

*NOTA:* El script `limpiar.py` lanza un pequeno warning al cargar el archivo
de excel. Esto no representa ningun problema, y el resto del programa corre normalmente.

### Asumpciones del modelo
* El archivo original es XLSX.
* Todas las paginas del archivo XLSX contienen tablas con el mismo formato
* Los datos empiezan en la columna A.
* Los datos empiezan en una fila cualquiera.
* La *longitud* esta dada en grados hacia **el oeste** siempre. (inverso del estandar)
* Un centro de acopio con dos o mas datos faltantes es considerado corrupto y es ignorado
* El archivo XLSX contiene los datos en orden: numero de centro, refugio, municipio, direccion, uso, servicios, capacidad, latitud, longitud, altitud, responsable y telefono. Si los cambios cambian, el nuevo orden puede ser pasado como argumento a `limpiar.py`. 

### Requerimientos del programa
El programa requiere dos librerias no estandar de Python: 
*`geopy` - Para calculos de distancia geodesica
*`openpyxl` - Para manipular archivos en excel

### Corriendo el programa
Primero es necesario limpiar los datos. Para esto, se corre:

`$> ./scripts/limpiar.py data/refugios_nayarit.xlsx data/resultado.csv 6`

*NOTA:* El script `limpiar.py` lanza un pequeno warning al cargar el archivo
de excel. Esto no representa ningun problema, y el resto del programa corre normalmente.


Esto extrae los datos del archivo XLSX empezando con el renglon 7 (porque ahi
empiezan los datos). 

Una vez que se tiene un archivo 'limpio' en csv, es posible correr el
script para encontrar los centros mas cercanos a las coordenadas 21.03059 104.670088:

`$> ./scripts/tres_centros.py data/resultado.csv 21.03059 104.670088`

El programa `tres_centros.py` puede recibir coordenadas en decimal, o en grados-minutos-segundos. 
