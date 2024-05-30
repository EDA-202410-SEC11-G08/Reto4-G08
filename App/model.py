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

import folium
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

from haversine import haversine, Unit

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
        # DICCIONARIOS     
        # diccionario de aeropuertos - csv
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
        catalog['COM_T'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)

        catalog['COM_D'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        catalog['MIL_COL_T'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        catalog['MIL_COL_D'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        
        catalog['CARGA_D']=gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        catalog['CARGA_T']=gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              cmpfunction=compareAir)
        
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:new_data_structs')


# Funciones para agregar informacion al 

def add_data_airports(catalog, row):
    add_airport(catalog['Aeropuerto'], row['ICAO'], row)
    gr.xinsertVertex(catalog['COM_T'], row['ICAO'])
    gr.insertVertex(catalog['COM_D'], row['ICAO'])
    if (row['PAIS'] == "Colombia"):
        gr.insertVertex(catalog['MIL_COL_T'], row['ICAO'])
        gr.insertVertex(catalog['MIL_COL_D'], row['ICAO'])
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
        
        gr.addEdge(catalog['COM_T'], row['ORIGEN'], row['DESTINO'], float(row['TIEMPO_VUELO']))
        gr.addEdge(catalog['COM_D'], row['ORIGEN'], row['DESTINO'], 
                   haversine((me.getValue(mp.get(catalog['Aeropuerto_COM'],row['ORIGEN']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],row['ORIGEN']))['Longitud']),
                             (me.getValue(mp.get(catalog['Aeropuerto_COM'],row['DESTINO']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],row['DESTINO']))['Longitud'])))

    elif (row['TIPO_VUELO'] == 'MILITAR'):
        add_airport(catalog['Aeropuerto_MIL'], row['ORIGEN'], row, 1)
        add_airport(catalog['Aeropuerto_MIL'], row['DESTINO'], row, 2)
        
        if (gr.containsVertex(catalog['MIL_COL_T'], row['ORIGEN']) and gr.containsVertex(catalog['MIL_COL_T'], row['DESTINO'])):
            gr.addEdge(catalog['MIL_COL_T'], row['ORIGEN'], row['DESTINO'], float(row['TIEMPO_VUELO']))
            gr.addEdge(catalog['MIL_COL_D'], row['ORIGEN'], row['DESTINO'], 
                    haversine((me.getValue(mp.get(catalog['Aeropuerto_MIL'],row['ORIGEN']))['Latitud'],
                                me.getValue(mp.get(catalog['Aeropuerto_MIL'],row['ORIGEN']))['Longitud']),
                                (me.getValue(mp.get(catalog['Aeropuerto_MIL'],row['DESTINO']))['Latitud'],
                                me.getValue(mp.get(catalog['Aeropuerto_MIL'],row['DESTINO']))['Longitud'])))
    elif (row['TIPO_VUELO'] == 'AVIACION_CARGA'):
        add_airport(catalog['Aeropuerto_CAR'], row['ORIGEN'], row, 1)
        add_airport(catalog['Aeropuerto_CAR'], row['DESTINO'], row, 2)
        
        if (gr.containsVertex(catalog['CARGA_T'], row['ORIGEN']) and gr.containsVertex(catalog['CARGA_T'], row['DESTINO'])):
            gr.addEdge(catalog['CARGA_T'], row['ORIGEN'], row['DESTINO'], float(row['TIEMPO_VUELO']))
            gr.addEdge(catalog['CARGA_D'], row['ORIGEN'], row['DESTINO'], 
                    haversine((me.getValue(mp.get(catalog['Aeropuerto_CAR'],row['ORIGEN']))['Latitud'],
                                me.getValue(mp.get(catalog['Aeropuerto_CAR'],row['ORIGEN']))['Longitud']),
                                (me.getValue(mp.get(catalog['Aeropuerto_CAR'],row['DESTINO']))['Latitud'],
                                me.getValue(mp.get(catalog['Aeropuerto_CAR'],row['DESTINO']))['Longitud'])))
            
    
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
    return gr.numVertices(catalog['COM_T'])

def flight_size(catalog):
    total = (gr.numEdges(catalog['COM_T'])) # COMPLETAR CON VUELOS MIL Y CAR
    return total 

def req_1(catalog, origen, destino): # REQ 1 ----------------------------------------------------------
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    min_origen = 30 
    aero_origen = None
    aero_destino = None
    min_destino = 30
    for aeropuerto in lt.iterator(mp.valueSet(catalog['Aeropuerto_COM'])):
        distancia_origen = haversine((aeropuerto['Latitud'],
                              aeropuerto['Longitud']),
                              (origen))
        
        distancia_destino = haversine((aeropuerto['Latitud'],
                              aeropuerto['Longitud']),
                              (destino))
        
        if (distancia_origen <= min_origen): 
            min_origen = distancia_origen
            aero_origen = aeropuerto['ICAO']
        if (distancia_destino <= min_destino): 
            min_destino = distancia_destino
            aero_destino = aeropuerto['ICAO']
        
    if (aero_destino == None): return ['No hay aeropuerto de destino cercano']
    elif (aero_origen == None): return ['No hay aeropuerto de origen cercano']
    else:
        search = bfs.BreathFirstSearch(catalog['COM_D'], aero_origen)
        camino = bfs.pathTo(search, aero_destino)
        if camino == None:
            return ['No hay conexion entre aeropuertos']
        else:
            info = get_stack_req1(catalog, camino)
            recorrido = info[0]
            tiempo = info[1]
            distancia_camino = info[2]
            return recorrido, aero_origen, min_origen, aero_destino, min_destino, distancia_camino, tiempo

def get_stack_req1(catalog, pila):
    camino = lt.newList('ARRAY_LIST')
    tiempo = 0
    distancia = 0
    
    while st.isEmpty(pila) == False:
        actual = st.pop(pila)
        sig = st.top(pila)
        lt.addLast(camino, actual)
        for vuelo in lt.iterator(me.getValue(mp.get(catalog['Aeropuerto_COM'], actual))['Vuelos_origen']):
            if vuelo['DESTINO'] == sig:
                tiempo += float(vuelo['TIEMPO_VUELO'])
                distancia += haversine((me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Longitud']),
                             (me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Longitud']))
                
    return camino, tiempo, distancia
        

def req_2(catalog, origen, destino): # REQ 2 ----------------------------------------------------------
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2    
    min_origen = 30
    aero_origen = None
    aero_destino = None
    min_destino = 30

    for aeropuerto in lt.iterator(mp.valueSet(catalog['Aeropuerto_COM'])):
        distancia_origen = haversine((aeropuerto['Latitud'], aeropuerto['Longitud']), (origen))
        distancia_destino = haversine((aeropuerto['Latitud'], aeropuerto['Longitud']), (destino))

        if distancia_origen <= min_origen:
            min_origen = distancia_origen
            aero_origen = aeropuerto['ICAO']
        if distancia_destino <= min_destino:
            min_destino = distancia_destino
            aero_destino = aeropuerto['ICAO']

    if aero_destino is None or aero_origen is None:
        return 'No hay aeropuerto de origen o destino cercano'

    search = bfs.BreadthFirstSearch(catalog['COM_T'], aero_origen)
    camino = bfs.pathTo(search, aero_destino)

    if camino is None:
        return 'No hay conexión entre aeropuertos'
    else:
        info = get_stack_req2(catalog, camino)
        recorrido = info[0]
        distancia_camino = info[2]

        return distancia_camino, len(recorrido) - 1, recorrido

def get_stack_req2(catalog, pila):
    camino = lt.newList('ARRAY_LIST')
    tiempo = 0
    distancia = 0

    while st.isEmpty(pila) == False:
        actual = st.pop(pila)
        sig = st.top(pila)
        lt.addLast(camino, actual)
        for vuelo in lt.iterator(me.getValue(mp.get(catalog['Aeropuerto_COM'], actual))['Vuelos_origen']):
            if vuelo['DESTINO'] == sig:
                tiempo += float(vuelo['TIEMPO_VUELO'])
                distancia += haversine((me.getValue(mp.get(catalog['Aeropuerto_COM'], vuelo['ORIGEN']))['Latitud'],
                                       me.getValue(mp.get(catalog['Aeropuerto_COM'], vuelo['ORIGEN']))['Longitud']),
                                      (me.getValue(mp.get(catalog['Aeropuerto_COM'], vuelo['DESTINO']))['Latitud'],
                                       me.getValue(mp.get(catalog['Aeropuerto_COM'], vuelo['DESTINO']))['Longitud']))

    return camino, tiempo, distancia

def req_3(catalog):
    """
    Función que soluciona el requerimiento 3 utilizando el algoritmo de Prim.
    
    """
    max_concurrencia = 0
    aero_max = None
    distancias_tot = 0
    trayectos_totales = 0
    caminos = []

    aeropuertos_carga = gr.vertices(catalog['CARGA_D'])

    for aeropuerto in lt.iterator(aeropuertos_carga):
        concurrencia = mp.getValue(mp.get(catalog['Aeropuerto_CAR'], aeropuerto))['Cantidad']
        if concurrencia > max_concurrencia or (concurrencia == max_concurrencia and aeropuerto < aero_max):
            max_concurrencia = concurrencia
            aero_max = aeropuerto
    
    mst = prim.PrimMST(catalog['CARGA_D'], aero_max)

    trayectos_totales = gr.numVertices(catalog['CARGA_D']) - 1

    distancias_tot = prim.weightMST(catalog['CARGA_D'], mst)


    trayectos = prim.edgesMST(mst,aero_max)
    caminos=trayectos

    return aero_max, max_concurrencia, distancias_tot, trayectos_totales, caminos


def req_4(catalog):
    """
    Función que soluciona el requerimiento 4.
    
    """
    max_concurrencia = 0
    aero_max = None
    destinos = lt.newList('ARRAY_LIST')
    tiempos_tot = lt.newList('ARRAY_LIST')
    distancias_tot = 0
    trayectos_totales = 0
    caminos = lt.newList('ARRAY_LIST')
    aeronaves = lt.newList('ARRAY_LIST')

    aeropuertos_carga = gr.vertices(catalog['CARGA_D'])# Obtener lista de aeropuertos de carga


    # Encontrar aeropuerto con mayor concurrencia de carga
    for aeropuerto in lt.iterator(aeropuertos_carga):
        concurrencia = me.getValue(mp.get(catalog['Aeropuerto_CAR'], aeropuerto))['Cantidad']
        if concurrencia > max_concurrencia or (concurrencia == max_concurrencia and aeropuerto < aero_max):
            max_concurrencia = concurrencia
            aero_max = aeropuerto
    
    search = djk.Dijkstra(catalog['CARGA_D'], aero_max)
    for aeropuerto in lt.iterator(aeropuertos_carga):
        if aeropuerto != aero_max:
            camino = djk.pathTo(search, aeropuerto)
            if camino is not None: 
                trayectos_totales += 1
                lt.addLast(caminos, camino)
                lt.addLast(tiempos_tot, djk.distTo(search, aeropuerto))
                lt.addLast(destinos, aeropuerto)

                # Calcular distancia total
                distancias_tot += djk.distTo(search, aeropuerto)

                # Obtener información de los vuelos
                info = get_stack_req4(catalog, camino)
                lt.addLast(distancias_tot, info[2])
                lt.addLast(aeronaves, info[3])
                
    return aero_max, destinos, distancias_tot, trayectos_totales, caminos

def get_stack_req4(catalog, pila):
    """
    Función auxiliar que obtiene información detallada de los trayectos encontrados.
    """
    camino = lt.newList('ARRAY_LIST')
    tiempo = lt.newList('ARRAY_LIST')
    distancia = lt.newList('ARRAY_LIST')
    aeronave = lt.newList('ARRAY_LIST')
    
    while not st.isEmpty(pila):
        actual = st.pop(pila)
        lt.addLast(camino, actual['vertexB'])
        for vuelo in lt.iterator(me.getValue(mp.get(catalog['Aeropuerto_CAR'], actual['vertexA']))['Vuelos_origen']):
            if vuelo['DESTINO'] == actual['vertexB']:
                lt.addLast(tiempo, float(vuelo['TIEMPO_VUELO']))
                lt.addLast(distancia, haversine((me.getValue(mp.get(catalog['Aeropuerto_CAR'],vuelo['ORIGEN']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_CAR'],vuelo['ORIGEN']))['Longitud']),
                             (me.getValue(mp.get(catalog['Aeropuerto_CAR'],vuelo['DESTINO']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_CAR'],vuelo['DESTINO']))['Longitud'])))
                lt.addLast(aeronave, vuelo['TIPO_AERONAVE'])
                
    return camino, tiempo, distancia, aeronave

def req_5(catalog):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    max = 0
    aero_max = None
    destinos = lt.newList('ARRAY_LIST')
    tiempos_tot = lt.newList('ARRAY_LIST')
    distancias = lt.newList('ARRAY_LIST')
    tiempos = lt.newList('ARRAY_LIST')
    caminos = lt.newList('ARRAY_LIST')
    aeronaves = lt.newList('ARRAY_LIST')

    
    aeropuertos = gr.vertices(catalog['MIL_COL_T'])
    
    
    for aeropuerto in lt.iterator(aeropuertos): # Obtener aeropuerto de mayor concurrencia militar
        if me.getValue(mp.get(catalog['Aeropuerto_MIL'], aeropuerto))['Cantidad'] >= max:
            max = me.getValue(mp.get(catalog['Aeropuerto_MIL'],aeropuerto))['Cantidad'] # concurrencia
            aero_max = aeropuerto  # aeropuerto 
    
    search = djk.Dijkstra(catalog['MIL_COL_T'], aero_max)
    for aeropuerto in lt.iterator(aeropuertos):
        if aeropuerto != aero_max:
            camino = djk.pathTo(search, aeropuerto)
            if camino != None: 
                lt.addLast(tiempos_tot, djk.distTo(search, aeropuerto))
                lt.addLast(caminos, djk.pathTo(search, aeropuerto))

                info = get_stack_req5(catalog, camino)
                lt.addLast(destinos, info[0])
                lt.addLast(tiempos, info[1])
                lt.addLast(distancias, info[2])
                lt.addLast(aeronaves, info[3])
                
    return aero_max, max, destinos, tiempos_tot, tiempos, distancias, caminos, aeronaves

def get_stack_req5(catalog, pila):
    i = 1
    camino = lt.newList('ARRAY_LIST')
    tiempo = lt.newList('ARRAY_LIST')
    distancia = lt.newList('ARRAY_LIST')
    aeronave = lt.newList('ARRAY_LIST')
    
    while st.isEmpty(pila) == False:
        actual = st.pop(pila)
        if i == 1:
            lt.addLast(camino, actual['vertexA'])
        lt.addLast(camino, actual['vertexB'])
        #lt.addLast(tiempo, actual['weight'])
        for vuelo in lt.iterator(me.getValue(mp.get(catalog['Aeropuerto_COM'], actual['vertexA']))['Vuelos_origen']):
            if vuelo['DESTINO'] == actual['vertexB']:
                lt.addLast(tiempo, float(vuelo['TIEMPO_VUELO']))
                lt.addLast(distancia, haversine((me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Longitud']),
                             (me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Longitud'])))
                lt.addLast(aeronave, vuelo['TIPO_AERONAVE'])
                
    return camino, tiempo, distancia, aeronave





def req_6(catalog, M):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6

    max_concurrencia = 0
    aero_max = None
    destinos = lt.newList('ARRAY_LIST')
    tiempos_tot = lt.newList('ARRAY_LIST')
    distancias_tot = lt.newList('ARRAY_LIST')
    caminos = lt.newList('ARRAY_LIST')
    aeronaves = lt.newList('ARRAY_LIST')

    aeropuertos_militares = gr.vertices(catalog['MIL_COL_T'])
    
    # Encontrar aeropuerto con mayor concurrencia militar
    for aeropuerto in lt.iterator(aeropuertos_militares):
        concurrencia = me.getValue(mp.get(catalog['Aeropuerto_MIL'], aeropuerto))['Cantidad']
        if concurrencia >= max_concurrencia:
            max_concurrencia = concurrencia
            aero_max = aeropuerto


    search = djk.Dijkstra(catalog['MIL_COL_T'], aero_max)
    for aeropuerto in lt.iterator(aeropuertos_militares):
        if aeropuerto != aero_max:
            camino = djk.pathTo(search, aeropuerto)
            if camino is not None:
                distancia_total = djk.distTo(search, aeropuerto)

                lt.addLast(destinos, aeropuerto)
                lt.addLast(tiempos_tot, distancia_total)
                lt.addLast(caminos, camino)

                info = get_stack_req6(catalog, camino)
                lt.addLast(distancias_tot, info[0])
                lt.addLast(aeronaves, info[1])
    
    return aero_max, destinos, tiempos_tot, distancias_tot, caminos, aeronaves


def get_stack_req6(catalog, pila):
    """
    Función auxiliar para obtener información detallada de los vuelos en el camino.
    """
    distancia = lt.newList('ARRAY_LIST')
    aeronave = lt.newList('ARRAY_LIST')

    while not st.isEmpty(pila):
        actual = st.pop(pila)
        for vuelo in lt.iterator(me.getValue(mp.get(catalog['Aeropuerto_COM'], actual['vertexA']))['Vuelos_origen']):
            if vuelo['DESTINO'] == actual['vertexB']:
                lt.addLast(distancia, haversine((me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Longitud']),
                             (me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Longitud'])))
                lt.addLast(aeronave, vuelo['TIPO_AERONAVE'])

    return distancia, aeronave


def req_7(catalog, origen, destino): # REQ 7 ----------------------------------------------------------
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    min_origen = 30 
    aero_origen = None
    aero_destino = None
    min_destino = 30
    for aeropuerto in lt.iterator(mp.valueSet(catalog['Aeropuerto_COM'])):
        distancia_origen = haversine((aeropuerto['Latitud'],
                              aeropuerto['Longitud']),
                              (origen))
        
        distancia_destino = haversine((aeropuerto['Latitud'],
                              aeropuerto['Longitud']),
                              (destino))
        
        if (distancia_origen <= min_origen): 
            min_origen = distancia_origen
            aero_origen = aeropuerto['ICAO']
        if (distancia_destino <= min_destino): 
            min_destino = distancia_destino
            aero_destino = aeropuerto['ICAO']
        
    if (aero_destino == None): return ['No hay aeropuerto de destino cercano']
    elif (aero_origen == None): return ['No hay aeropuerto de origen cercano']
    else:
        search = djk.Dijkstra(catalog['COM_T'], aero_origen)
        camino = djk.pathTo(search, aero_destino)
        if camino == None:
            return ['No hay conexion entre aeropuertos']
        else:
            info = get_stack_req7(catalog, camino)
            recorrido = info[0]
            tiempo = djk.distTo(search, aero_destino)
            tiempo_camino = info[1]
            distancia_camino = info[2]
            return recorrido, aero_origen, min_origen, aero_destino, min_destino, distancia_camino, tiempo, tiempo_camino

def get_stack_req7(catalog, pila):
    i = 1
    camino = lt.newList('ARRAY_LIST')
    tiempo = lt.newList('ARRAY_LIST')
    distancia = lt.newList('ARRAY_LIST')
    
    while st.isEmpty(pila) == False:
        actual = st.pop(pila)
        if i == 1:
            lt.addLast(camino, actual['vertexA'])
        lt.addLast(camino, actual['vertexB'])
        #lt.addLast(tiempo, actual['weight'])
        for vuelo in lt.iterator(me.getValue(mp.get(catalog['Aeropuerto_COM'], actual['vertexA']))['Vuelos_origen']):
            if vuelo['DESTINO'] == actual['vertexB']:
                lt.addLast(tiempo, float(vuelo['TIEMPO_VUELO']))
                lt.addLast(distancia, haversine((me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['ORIGEN']))['Longitud']),
                             (me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Latitud'],
                             me.getValue(mp.get(catalog['Aeropuerto_COM'],vuelo['DESTINO']))['Longitud'])))
                
    return camino, tiempo, distancia

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
