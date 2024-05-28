"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import math
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.Utils import error as error


assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_catalog():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    
    Aeropuertos: Estructura para almacenar los vértices del grafo
    Vuelos: grafo
    
    """
    #TODO: Inicializar las estructuras de datos
    try:
        catalog = {
            'Aeropuerto': None,
            'vuelos': None,
            'vuelosComerciales': None,
            'vuelosCarga': None,
            'vuelosMilitares': None,
            'tiempo':None
        }
        # LISTAS     
       
        # DICCIONARIOS     
        # diccionario de aeropuertos - csv
        catalog['airports'] = lt.newList(datastructure='ARRAY_LIST')
        catalog['fligths'] = lt.newList(datastructure='ARRAY_LIST')
        catalog['Aeropuerto']= mp.newMap(numelements=14000,
                                          maptype="CHAINING",
                                          cmpfunction=compareAir)
        # diccionario de aeropuertos alimentado con la info de vuelos
        # Cada diccionario corresponde para un tipo de vuelo, comercial, militar y de carga        
        catalog['Aeropuerto_COM']= mp.newMap(numelements=3021,
                                          maptype="CHAINING",
                                          loadfactor= 0.7,
                                          cmpfunction=compareAir)
        catalog['Aeropuerto_MIL']= mp.newMap(numelements=3021,
                                          maptype="CHAINING",
                                          loadfactor= 0.7,
                                          cmpfunction=compareAir)
        catalog['Aeropuerto_CAR']= mp.newMap(numelements=3021,
                                          maptype="CHAINING",
                                          loadfactor= 0.7,
                                          cmpfunction=compareAir)
        
        # GRAFOS     
        catalog['aeropuertos'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)

        catalog['vuelosComerciales'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        catalog['vuelosCarga'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        catalog['vuelosMilitares'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:new_data_structs')


# Funciones para agregar informacion al 

def add_data_airports(catalog, row):
    add_airport(catalog['Aeropuerto'], row['ICAO'], row)
    lt.addLast(catalog['airports'], row)
    return catalog

def add_airport(map, airport, row, mode = 0):
    airports = map
    existairport = mp.contains(airports, airport)
    if existairport:
        entry = mp.get(airports, airport)
        airporttemp = me.getValue(entry)
    else:
        airporttemp = new_airport(row)
        mp.put(airports, airport, airporttemp)
    
    if mode == 1:
        lt.addLast(airporttemp['Vuelos_origen'], row)
        airporttemp['Cantidad_VO'] = lt.size(airporttemp['Vuelos_origen'])
        
    elif mode == 2:     
        lt.addLast(airporttemp['Vuelos_destino'], row)
        airporttemp['Cantidad_VD'] = lt.size(airporttemp['Vuelos_destino']) 
    
    airporttemp['Cantidad'] = airporttemp['Cantidad_VO'] + airporttemp['Cantidad_VD']

   
def new_airport(airport_in):
    airport = {'Nombre': airport_in['NOMBRE'],
               'ICAO': airport_in['ICAO'],
               'Ciudad': airport_in['CIUDAD'],
               'Pais': airport_in['PAIS'],
               'Latitud': float(airport_in['LATITUD'].replace(",",".")),
               'Longitud': float(airport_in['LONGITUD'].replace(",",".")),
               'Altitud': float(airport_in['ALTITUD'].replace(",",".")),
               'Vuelos_origen': None,
               'Cantidad_VO': 0,
               'Vuelos_destino': None,
               'Cantidad_VD': 0,
               'Cantidad': 0
    }
    
    airport['Vuelos_origen'] = lt.newList('ARRAY_LIST')
    airport['Vuelos_destino'] = lt.newList('ARRAY_LIST')

    return airport

def add_data_flights(catalog, row):
    
    if (row['TIPO_VUELO'] == 'AVIACION_COMERCIAL'):
        add_airport(catalog['Aeropuerto_COM'], row['ORIGEN'], row, 1)
        add_airport(catalog['Aeropuerto_COM'], row['DESTINO'], row, 2)
    elif (row['TIPO_VUELO'] == 'MILITAR'):
        add_airport(catalog['Aeropuerto_MIL'], row['ORIGEN'], row, 1)
        add_airport(catalog['Aeropuerto_MIL'], row['DESTINO'], row, 2)
    elif (row['TIPO_VUELO'] == 'AVIACION_CARGA'): 
        add_airport(catalog['Aeropuerto_CAR'], row['ORIGEN'], row, 1)
        add_airport(catalog['Aeropuerto_CAR'], row['DESTINO'], row, 2)
    lt.addLast(catalog['fligths'], row)

    return catalog

def show_data(map):
    airports = mp.valueSet(map)
    airports = merg.sort(airports, cmp_total_flights)
    
    # Eliminar aeropuertos en 0, gasto temporal muy alto, MEJORAR/ARREGLAR/ELIMINAR
    """ 
    stop = False
    while stop == False:
        ultimo = lt.lastElement(airports)
        if (ultimo['Cantidad'] == 0):
            lt.removeLast(airports)
        else: stop == True
    """ 
    return airports

def addAirportConnection(analyzer, org, dst):
    """
    Adiciona los aeropuertos al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificadol aeropuerto
    seguido de la ruta que sirve.

    """
    try:
        origin = org['ICAO']
        destination = dst['ICAO']
        
        distance = float(haversine(org['LATITUD'],org['LONGITUD'],dst['LATITUD'],dst['LONGITUD']))
        
        addDistance(analyzer, origin)
        addDistance(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        addRouteAirport(analyzer, org)
        addRouteAirport(analyzer, dst)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addAirportConnection')

def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.pow(math.sin(dlon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    
    return R * c

def addDistance(analyzer, airport):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['aeropuertos'], airport):
            gr.insertVertex(analyzer['aeropuertos'], airport)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addDistance')

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
    edge = gr.getEdge(analyzer['aeropuertos'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['aeropuertos'], origin, destination, distance)
    return analyzer


def addRouteAirport(analyzer, fligth):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = mp.get(analyzer['aeropuertos'], fligth['ICAO'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, fligth['ICAO'])
        mp.put(analyzer['stops'], fligth['ICAO'], lstroutes)
    else:
        lstroutes = entry['value']
        info = fligth['ICAO']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer











def add_vertex(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    try:
        if not gr.containsVertex(data_structs['aeropuerto'], data):
            gr.insertVertex(data_structs['aeropuerto'], data)
        return data_structs
    except Exception as exp:
        error.reraise(exp, 'model:addVertex')
        
def addVertex(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['aeropuerto'], stopid):
            gr.insertVertex(analyzer['aeropuerto'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addVertex')        


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

def airport_size(catalog):
    return lt.size(catalog['airports'])

def flight_size(catalog):
    return lt.size(catalog['fligths'])

def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compareAir(ciudad, llave):
    code =llave['key']
    if (ciudad == code):
        return 0
    elif (ciudad > code):
        return 1
    else:
        return -1  
    

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
     

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def cmp_total_flights(oferta1, oferta2): # Comparacion para organizar aeropuertos por mayor numero de vuelos
    if (oferta1['Cantidad'] > oferta2['Cantidad']):
        return True
    elif (oferta1['Cantidad'] == oferta2['Cantidad']):
        if (oferta1['ICAO'] > oferta2['ICAO']):
            return True
        else: return False
    else: return False


