"""
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
    
    print("A continuacion, se muestran las distancias a recorrer")
    print(info_req1[2], "Distancia del punto de origen al aeropuerto de origen",info_req1[1])
    print(info_req1[5], "Distancia de trayecto entre aeropuertos")
    print(info_req1[4], "Distancia del aeropuerto de destino al punto de destino",info_req1[3])
    
    print("Se recorren", lt.size(info_req1[0]), "aeropuertos")
    print("Se demora en recorrer",info_req1[6] )
    for aeropuerto in lt.iterator(info_req1[0]):
        table.append([me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['ICAO'],
                     me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Nombre'],
                     me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Ciudad'],
                     me.getValue(mp.get(control['model']['Aeropuerto_COM'],aeropuerto))['Pais']])
    print(tabulate(table))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


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
    
    for distancia in lt.iterator(info_req7[5]): 
        dist_tot += distancia  
    
    print("A continuacion, se muestran las distancias a recorrer")
    print(info_req7[2], "Distancia del punto de origen al aeropuerto de origen",info_req7[1])
    print(dist_tot, "Distancia de trayecto entre aeropuertos")
    print(info_req7[4], "Distancia del aeropuerto de destino al punto de destino",info_req7[3])
    
    print("Se recorren", lt.size(info_req7[0]), "aeropuertos")
    print("Se demora en recorrer",info_req7[6])
    
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

def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(answer, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer:.3f}")

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', True):
        return True
    else:
        return False
    
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
            # Observar uso de memoria en la carga de datos -----------------------------------------
            print("Desea observar el uso de memoria? (True/False)")
            mem = input("Respuesta: ")
            mem = castBoolean(mem)
            # Ejecutar comando de cargar datos -----------------------------------------------------
            ans = load_data(control, memflag=mem)
            printLoadDataAnswer(ans[1])
            # Cantidad de datos guardados ----------------------------------------------------------
            print('Aeropuertos cargados: ' + str(controller.airport_size(control))) 
            print('Vuelos cargados: ' + str(controller.flight_size(control))) 
            # VISUALIZADOR CARGA DE DATOS ----------------------------------------------------------
            tipos = ['Comercial','Militar','Carga']
            i = 0
            for tipo in ans[0]:
                table1, table2 = print_load_data(tipo)
                print("Primeros y ultimos 5 aeropuertos de concurrencia " + tipos[i])
                print(tabulate(table1))
                print(tabulate(table2))
                i += 1
                
        elif int(inputs) == 2: # REQ 1 ----------------------------------------------------------
            print("Ingresar coordenadas con '.' como decimal")
            origen_lat = input("Inserta la latitud de origen: ")
            origen_lon = input("Inserta la longitud de origen: ")
            
            destino_lat = input("Inserta la latitud de destino: ")
            destino_lon = input("Inserta la longitud de destino: ")
            
            origen = (float(origen_lat), float(origen_lon))
            destino = (float(destino_lat), float(destino_lon))

            # Observar uso de memoria en la carga de datos -----------------------------------------
            print("Desea observar el uso de memoria? (True/False)")
            mem = input("Respuesta: ")
            mem = castBoolean(mem)
            # Ejecutar comando de cargar datos -----------------------------------------------------
            ans = controller.req_1(control, origen, destino, memflag = mem)
            info_req1 = ans[0]
            # Print rendimiento
            print("Tiempo [ms]: ", f"{ans[1]:.3f}")
            if (mem == True): print("Memoria [kB]: ", f"{ans[2]:.3f}")    
            # Print resultados
            if len(info_req1) == 1:
                print(info_req1)
            else:  
                print_req_1(info_req1)             
            
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

        elif int(inputs) == 8: # REQ 7 ----------------------------------------------------------
            print("Ingresar coordenadas con '.' como decimal")
            origen_lat = input("Inserta la latitud de origen: ")
            origen_lon = input("Inserta la longitud de origen: ")
            
            destino_lat = input("Inserta la latitud de destino: ")
            destino_lon = input("Inserta la longitud de destino: ")
            
            origen = (float(origen_lat), float(origen_lon))
            destino = (float(destino_lat), float(destino_lon))

            # Observar uso de memoria en la carga de datos -----------------------------------------
            print("Desea observar el uso de memoria? (True/False)")
            mem = input("Respuesta: ")
            mem = castBoolean(mem)
            # Ejecutar comando de cargar datos -----------------------------------------------------
            ans = controller.req_7(control, origen, destino, memflag = mem)
            info_req7 = ans[0]
            # Print rendimiento
            print("Tiempo [ms]: ", f"{ans[1]:.3f}")
            if (mem == True): print("Memoria [kB]: ", f"{ans[2]:.3f}")    
            # Print resultados
            if len(info_req7) == 1:
                print(info_req7)
            else:  
                print_req_7(info_req7)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)