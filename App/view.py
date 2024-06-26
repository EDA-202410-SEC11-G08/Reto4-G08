﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control, memflag):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    ans = controller.load_data(control, memflag)
    return ans


def print_load_data(list):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento

    table1 = []
    table2 = []
    header = ['Nombre','ICAO','Ciudad','Concurrencia']
    table1.append(header)
    table2.append(header)
    airport1 = lt.subList(list, 1, 5)
    airport2 = lt.subList(list, lt.size(list)-5+1, 5)

    for airport in lt.iterator(airport1):
        table1.append([airport['Nombre'],
        airport['ICAO'],
        airport['Ciudad'],
        airport['Cantidad']])

    for airport in lt.iterator(airport2):
        table2.append([airport['Nombre'],
        airport['ICAO'],
        airport['Ciudad'],
        airport['Cantidad']])
        
    return table1, table2

def print_req_1(info_req1):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    table = []
    header = ['ICAO','Nombre','Ciudad','Pais', 'Tiempo']
    table.append(header)
    
    dist_tot = 0
    tiempo_tot = info_req1[6]
    i = 1
    
    dist_tot = info_req1[5]
    #1for tiempos in lt.iterator(info_req1[6]): tiempo_tot += tiempos 
    
    print("A continuacion, se muestran las distancias a recorrer")
    print(info_req1[2], "[Km] Distancia del punto de origen al aeropuerto de origen",info_req1[1])
    print(dist_tot, "[Km] Distancia de trayecto entre aeropuertos")
    print(info_req1[4], "[Km] Distancia del aeropuerto de destino al punto de destino",info_req1[3])
    
    print("Se recorren", lt.size(info_req1[0]), "aeropuertos")
    print("Se demora en recorrer",tiempo_tot,"min")
    
    for aeropuerto in lt.iterator(info_req1[0]):
        if i <= lt.size(info_req1[5]):
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        lt.getElement(info_req1[6],i),
                        lt.getElement(info_req1[5],i)])
        else:
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        "",
                        ""])
        i += 1
            
    print(tabulate(table))



def print_req_2(info_req2):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    table = []
    header = ['ICAO','Nombre','Ciudad','Pais', 'Tiempo']
    table.append(header)
    
    dist_tot = 0
    tiempo_tot = info_req2[6]
    i = 1
    
    dist_tot = info_req2[5]
    #1for tiempos in lt.iterator(info_req1[6]): tiempo_tot += tiempos 
    
    print("A continuacion, se muestran las distancias a recorrer")
    print(info_req2[2], "[Km] Distancia del punto de origen al aeropuerto de origen",info_req2[1])
    print(dist_tot, "[Km] Distancia de trayecto entre aeropuertos")
    print(info_req2[4], "[Km] Distancia del aeropuerto de destino al punto de destino",info_req2[3])
    
    print("Se recorren", lt.size(info_req2[0]), "aeropuertos")
    print("Se demora en recorrer",tiempo_tot,"min")
    
    for aeropuerto in lt.iterator(info_req2[0]):
        if i <= lt.size(info_req2[5]):
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        lt.getElement(info_req2[6],i),
                        lt.getElement(info_req2[5],i)])
        else:
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        "",
                        ""])
        i += 1
            
    print(tabulate(table))


def print_req_3(info_req3):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    table = []
    header = ['ICAO','Nombre','Ciudad','Pais', 'Tiempo']
    table.append(header)
    
    dist_tot = 0
    tiempo_tot = info_req3[6]
    i = 1
    
    dist_tot = info_req3[5]
    #1for tiempos in lt.iterator(info_req1[6]): tiempo_tot += tiempos 
    
    print("A continuacion, se muestran las distancias a recorrer")
    print(info_req3[2], "[Km] Distancia del punto de origen al aeropuerto de origen",info_req3[1])
    print(dist_tot, "[Km] Distancia de trayecto entre aeropuertos")
    print(info_req3[4], "[Km] Distancia del aeropuerto de destino al punto de destino",info_req3[3])
    
    print("Se recorren", lt.size(info_req3[0]), "aeropuertos")
    print("Se demora en recorrer",tiempo_tot,"min")
    
    for aeropuerto in lt.iterator(info_req3[0]):
        if i <= lt.size(info_req3[5]):
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        lt.getElement(info_req3[6],i),
                        lt.getElement(info_req3[5],i)])
        else:
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        "",
                        ""])
        i += 1
            
    print(tabulate(table))


def print_req_4(info_req4, mode=1):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    distancia_total = 0
    print("El aeropuerto de mayor importancia segun la concurrencia CARGA es:")
    
    table = []
    header = ['ICAO','Nombre','Ciudad','Pais', 'Concurrencia Carga']
    header1 = ['A->B',
               'Nombre Origen','Ciudad Origen','Pais Origen',
               'Nombre Destino','Ciudad Destino','Pais Destino',
               'Distancia recorrida [Km]','Tiempo del trayecto [min]', 'Tipo de aeronave']
    table.append(header)
    table.append([me.getValue(mp.get(control['model']['Aeropuerto_CAR'],info_req4[0]))['ICAO'],
                  me.getValue(mp.get(control['model']['Aeropuerto_CAR'],info_req4[0]))['Nombre'],
                  me.getValue(mp.get(control['model']['Aeropuerto_CAR'],info_req4[0]))['Ciudad'],
                  me.getValue(mp.get(control['model']['Aeropuerto_CAR'],info_req4[0]))['Pais'],
                  me.getValue(mp.get(control['model']['Aeropuerto_CAR'],info_req4[0]))['Cantidad']])
    print(tabulate(table))
    for distancias_trayecto in lt.iterator(info_req4[5]):
        for distancia in lt.iterator(distancias_trayecto): distancia_total += float(distancia)
        
    print("El numero total de trayectos:", lt.size(info_req4[2]))
    print("La distancia total de los trayectos: ", distancia_total)
    j = 1
    if (mode == 1):   
        
        for camino in lt.iterator(info_req4[6]):
            i = 1
            table1 = []
            table1.append(header1)
            camino_size = st.size(camino)
            origen = None
            destino = None
            
            while st.isEmpty(camino) == False:
                actual = st.pop(camino)
                
                if (i == 1): 
                    origen = actual['vertexA']
                if (i == camino_size): 
                    destino = actual['vertexB']
    
                table1.append([(actual['vertexA'],"->",actual['vertexB']),
                               me.getValue(mp.get(control['model']['Aeropuerto_CAR'],actual['vertexA']))['Nombre'],
                               me.getValue(mp.get(control['model']['Aeropuerto_CAR'],actual['vertexA']))['Ciudad'],
                               me.getValue(mp.get(control['model']['Aeropuerto_CAR'],actual['vertexA']))['Pais'],
                               me.getValue(mp.get(control['model']['Aeropuerto_CAR'],actual['vertexB']))['Nombre'],
                               me.getValue(mp.get(control['model']['Aeropuerto_CAR'],actual['vertexB']))['Ciudad'],
                               me.getValue(mp.get(control['model']['Aeropuerto_CAR'],actual['vertexB']))['Pais'],
                               lt.getElement(lt.getElement(info_req4[5],j),i),
                               lt.getElement(lt.getElement(info_req4[4],j),i),
                               lt.getElement(lt.getElement(info_req4[7],j),i)])
                i += 1
            j += 1
            print("Trayecto total", origen, "->", destino)
            print(tabulate(table1))

    else:
        
        for camino in lt.iterator(info_req4[2]):
            table1 = []
            table1.append(header1)
            origen = lt.firstElement(camino)
            destino = lt.lastElement(camino)
            print("Trayecto Total",origen,"->",destino)
            distancia_tot = 0
            naves = []
            for distancia in lt.iterator(lt.getElement(info_req4[5],j)): distancia_tot += float(distancia)
            for nave in lt.iterator(lt.getElement(info_req4[7],j)): naves.append(nave)
            
            table1.append([(origen,"->",destino),
                            me.getValue(mp.get(control['model']['Aeropuerto_CAR'],origen))['Nombre'],
                            me.getValue(mp.get(control['model']['Aeropuerto_CAR'],origen))['Ciudad'],
                            me.getValue(mp.get(control['model']['Aeropuerto_CAR'],origen))['Pais'],
                            me.getValue(mp.get(control['model']['Aeropuerto_CAR'],destino))['Nombre'],
                            me.getValue(mp.get(control['model']['Aeropuerto_CAR'],destino))['Ciudad'],
                            me.getValue(mp.get(control['model']['Aeropuerto_CAR'],destino))['Pais'],
                            distancia_tot,
                            lt.getElement(info_req4[3],j),
                            naves])
            print(tabulate(table1))
            j += 1    


def print_req_5(info_req5, mode = 0):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    distancia_total = 0
    print("El aeropuerto de mayor importancia segun la concurrencia militar es:")
    
    table = []
    header = ['ICAO','Nombre','Ciudad','Pais', 'Concurrencia Militar']
    header1 = ['A->B',
               'Nombre Origen','Ciudad Origen','Pais Origen',
               'Nombre Destino','Ciudad Destino','Pais Destino',
               'Distancia recorrida [Km]','Tiempo del trayecto [min]', 'Tipo de aeronave']
    table.append(header)
    table.append([me.getValue(mp.get(control['model']['Aeropuerto_MIL'],info_req5[0]))['ICAO'],
                  me.getValue(mp.get(control['model']['Aeropuerto_MIL'],info_req5[0]))['Nombre'],
                  me.getValue(mp.get(control['model']['Aeropuerto_MIL'],info_req5[0]))['Ciudad'],
                  me.getValue(mp.get(control['model']['Aeropuerto_MIL'],info_req5[0]))['Pais'],
                  me.getValue(mp.get(control['model']['Aeropuerto_MIL'],info_req5[0]))['Cantidad']])
    print(tabulate(table))
    for distancias_trayecto in lt.iterator(info_req5[5]):
        for distancia in lt.iterator(distancias_trayecto): distancia_total += float(distancia)
        
    print("El numero total de trayectos:", lt.size(info_req5[2]))
    print("La distancia total de los trayectos: ", distancia_total)
    j = 1
    if (mode == 1):   
        
        for camino in lt.iterator(info_req5[6]):
            i = 1
            table1 = []
            table1.append(header1)
            camino_size = st.size(camino)
            origen = None
            destino = None
            
            while st.isEmpty(camino) == False:
                actual = st.pop(camino)
                
                if (i == 1): 
                    origen = actual['vertexA']
                if (i == camino_size): 
                    destino = actual['vertexB']
    
                table1.append([(actual['vertexA'],"->",actual['vertexB']),
                               me.getValue(mp.get(control['model']['Aeropuerto_MIL'],actual['vertexA']))['Nombre'],
                               me.getValue(mp.get(control['model']['Aeropuerto_MIL'],actual['vertexA']))['Ciudad'],
                               me.getValue(mp.get(control['model']['Aeropuerto_MIL'],actual['vertexA']))['Pais'],
                               me.getValue(mp.get(control['model']['Aeropuerto_MIL'],actual['vertexB']))['Nombre'],
                               me.getValue(mp.get(control['model']['Aeropuerto_MIL'],actual['vertexB']))['Ciudad'],
                               me.getValue(mp.get(control['model']['Aeropuerto_MIL'],actual['vertexB']))['Pais'],
                               lt.getElement(lt.getElement(info_req5[5],j),i),
                               lt.getElement(lt.getElement(info_req5[4],j),i),
                               lt.getElement(lt.getElement(info_req5[7],j),i)])
                i += 1
            j += 1
            print("Trayecto total", origen, "->", destino)
            print(tabulate(table1))

    else:
        
        for camino in lt.iterator(info_req5[2]):
            table1 = []
            table1.append(header1)
            origen = lt.firstElement(camino)
            destino = lt.lastElement(camino)
            print("Trayecto Total",origen,"->",destino)
            distancia_tot = 0
            naves = []
            for distancia in lt.iterator(lt.getElement(info_req5[5],j)): distancia_tot += float(distancia)
            for nave in lt.iterator(lt.getElement(info_req5[7],j)): naves.append(nave)
            
            table1.append([(origen,"->",destino),
                            me.getValue(mp.get(control['model']['Aeropuerto_MIL'],origen))['Nombre'],
                            me.getValue(mp.get(control['model']['Aeropuerto_MIL'],origen))['Ciudad'],
                            me.getValue(mp.get(control['model']['Aeropuerto_MIL'],origen))['Pais'],
                            me.getValue(mp.get(control['model']['Aeropuerto_MIL'],destino))['Nombre'],
                            me.getValue(mp.get(control['model']['Aeropuerto_MIL'],destino))['Ciudad'],
                            me.getValue(mp.get(control['model']['Aeropuerto_MIL'],destino))['Pais'],
                            distancia_tot,
                            lt.getElement(info_req5[3],j),
                            naves])
            print(tabulate(table1))
            j += 1
            
def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(info_req7):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    table = []
    header = ['ICAO','Nombre','Ciudad','Pais', 'Tiempo', 'Distancia']
    table.append(header)
    
    dist_tot = 0
    i = 1
    
    for distancia in lt.iterator(info_req7[5]): dist_tot += distancia  
    
    print("A continuacion, se muestran las distancias a recorrer")
    print(info_req7[2], "[Km] Distancia del punto de origen al aeropuerto de origen",info_req7[1])
    print(dist_tot, "[Km] Distancia de trayecto entre aeropuertos")
    print(info_req7[4], "[Km] Distancia del aeropuerto de destino al punto de destino",info_req7[3])
    
    print("Se recorren", lt.size(info_req7[0]), "aeropuertos")
    print("Se demora en recorrer",info_req7[6],"min")
    
    for aeropuerto in lt.iterator(info_req7[0]):
        if i <= lt.size(info_req7[5]):
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        lt.getElement(info_req7[7],i),
                        lt.getElement(info_req7[5],i)])
        else:
            table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                        me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais'],
                        "",
                        ""])
        i += 1
            
    print(tabulate(table))


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1: # CARGA DE DATOS ------------------------------------------------------
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)