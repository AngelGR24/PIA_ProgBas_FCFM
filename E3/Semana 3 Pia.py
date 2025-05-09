import requests
import json
import re
import csv
import statistics
import numpy

#Sermana 2
def analizar_partidos(data_json, equipo_nombre):
    resultados = {"Victorias": 0, "Derrotas": 0, "Empates": 0, "Sin jugar": 0}

    for partido in data_json.get("matches", []):
        casa = partido["homeTeam"]["name"]
        visita = partido["awayTeam"]["name"]
        ganador = partido["score"]["winner"]
        fecha = partido["utcDate"]

        resultado = "Sin jugar"

        if ganador == "HOME_TEAM":
            if casa == equipo_nombre:
                resultado = "Ganado"
                resultados["Victorias"] += 1
            else:
                resultado = "Perdido"
                resultados["Derrotas"] += 1
        elif ganador == "AWAY_TEAM":
            if visita == equipo_nombre:
                resultado = "Ganado"
                resultados["Victorias"] += 1
            else:
                resultado = "Perdido"
                resultados["Derrotas"] += 1
        elif ganador == "DRAW":
            resultado = "Empatado"
            resultados["Empates"] += 1
        else:
            resultados["Sin jugar"] += 1

        partidos_analizados.append({
            "fecha": fecha,
            "local": casa,
            "visitante": visita,
            "resultado": resultado,
            "equipo": equipo_nombre
        })

    return resultados

#Semana 3
def leer_resultados(archivo):
    datos = {}
    with open(archivo, 'r') as f:
        for linea in f:
            clave, valor = linea.strip().split(':')
            datos[clave.strip()] = float(valor.strip())
    return datos


UriBC = 'https://api.football-data.org/v4/teams/81/matches?competitions=PD'#Llamado a la api obtenido de la pagina de la documentacion de
headers = { 'X-Auth-Token': '8e3f8a085d2241b6888b7e4b469798f3' }           #la api, en este llamado obtenemos la informacion 
ResponseBC = requests.get(UriBC, headers=headers)                          #de los partidos del barcelona en la Liga Española actual.
ResBC = ResponseBC.json()

"""En la informacion de los partidos propocionada por la api hay un apartado que nos resume la informacion, en este resumen nos muestra
las victorias, derrotas y empates, sin embargo, la informacion esta erronea por lo que lo tenemos que hacer nosotros manualmente"""
#Definimos las variables donde alamacenaremos la informacion de los resultados
VictBC = 0
DerrBC = 0
EmpBC = 0
SinJugBC = 0
ListBC = [] #En esta lista se registraran con un 1 las victorias, 2 las derrotas, 3 los empates, sin tomar en cuenta los partidos sin
#jugar. Esto se realizo durante la elaboracion del entregable 3 

for x, y in ResBC.items(): #Iteramos el json de la api.
    if x == "matches": #La llave matches tiene como valor una lista con diccionarios de cada partido, siendo lo que nos interesa
        ContBC = len(ResBC["matches"]) #Contamos los elementos de la lista para iterarlos
        for i in range(ContBC): #Iteramos la lista
            #print(f"\nPartido numero: {i+1}") #Indicamos el numero del partido para ver que la impresion este bien
            
            """for z,w in ResBC["matches"][i].items():#Obtenemos el items de cada diccionario de la lista            
                print(f"{z}: {w}") #Imprimimos iterado los diccionarios de la lista matches
            Con este for, obtenemos cada diccionario de la lista contenida en la llave matches, no es necesario imprimirla para
            el trabajo final, sin embargo si fue necesario imprimirla para comprender mejor que es lo que se haria, se deja como
            comentario por si se quiere volver a ver la informacion de cada diccionario de la lista contenida en la llave matches"""
            
            Casa = ResBC["matches"][i]["homeTeam"]["name"]  #Registrariamos las victorias, derrotas o empates de la sig manera. Primero 
            Visit = ResBC["matches"][i]["awayTeam"]["name"] #guardamos a los equipos visitantes y locales en una variable, despues 
            Gan = ResBC["matches"][i]["score"]["winner"]    #guardamos el ganador en otra variable, el ganador, perdedor o un empate
                                                            # es indicado con un AWAY_TEAM, HOME_TEAM o DRAW dependiendo el caso,
            """"Hay muchas maneras de realizar el conteo de partidos ganados, empataados, perdidos y sin jugar, nosotros lo realizamos
            de la sig manera, utilizando try y except, asi como el modulo re"""                                            
            try: 
                posib = re.compile(r"HOME_TEAM") #Creamos el objeto con la expresion "HOME_TEAM"
                lol = posib.search(Gan)  #La buscamos y el resultado lo asignamos a una variable
                lol.group() #Con esto nos aseguramos que si el resultado buscado devuelve un valor el codigo siga, si no, no devolveria 
                #un valor y no se podria utilizar .group, dando un error y pasandonos a la seccion de la exepcion, asi igual con las
                #excepciones.
                #print(f"El {Casa} gano ante el {Visit}") #Mostramos quien gano
                if Casa == "FC Barcelona": #Como estamos analizando si Gan es "HOME_TEAM", entonces el ganador tiene que ser el equipo
                    #de casa, comprobamos si el equipo de casa es el barcelona y si es asi, entonces sumamos uno a las victorias
                    VictBC += 1
                    ListBC.append(1)
                elif Casa != "FC Barcelona": #Si el equipo de casa no es el Barcelona entonces sumamos uno a las derrotas.
                    DerrBC += 1
                    ListBC.append(2)
            except:
                try: 
                    posib = re.compile(r"AWAY_TEAM") #Realizamos el mismo procedimiento que en el try anterior unicamente que ahora 
                    #el objeto con la epxresion "AWAY_TEAM"
                    lol = posib.search(Gan)
                    lol.group()
                    #print(f"El {Visit} gano ante el {Casa}")
                    
                    if Visit == "FC Barcelona":  #Si el visitante es el barcelona le sumamos uno a las victorias
                        VictBC += 1
                        ListBC.append(1)
                    elif Visit != "FC Barcelona":  #Si no lo es le sumamos uno a las derrotas
                        DerrBC += 1
                        ListBC.append(2)
                except:
                    try:
                        posib = re.compile(r"DRAW") #Ahora el objeto sera creado con la expresion "DRAW"
                        lol = posib.search(Gan)
                        lol.group()
                        #print(f"Se empato el partido entre {Casa}-{Visit}")
                        EmpBC += 1 #Si se empato el partido no hay que comprobar quien empato asi que solo se suma 1 a los empates.
                        ListBC.append(3)
                    except:
                        #Si no es ninguna de las tres opciones anteriores entonces significa que el partido no se ha jugado no ocupamos
                        #comprobarlo con utilizando re, por lo que unicamente sumamos uno a los partidos sin jugar
                        #print(f"No se ha jugado el partido entre {Casa}-{Visit}")
                        SinJugBC += 1
                        
#Ya que ya conocemos la cantidad de partidos ganados, empatados, perdidos y sin jugar calculamos los porcentajes que representan estos
#partidos del total de los mismos.
PorVictBC = round(((VictBC/(VictBC+DerrBC+EmpBC+SinJugBC))*100),2)
PorDerrBC = round(((DerrBC/(VictBC+DerrBC+EmpBC+SinJugBC))*100),2)
PorEmpBC = round(((EmpBC/(VictBC+DerrBC+EmpBC+SinJugBC))*100),2)
PorSinJugBC = round(((SinJugBC/(VictBC+DerrBC+EmpBC+SinJugBC))*100),2)

#Imprimimos los partidos jugados, sus resultados y el porcentaje que representan los mismos
#print(f"""\nEl FC Barcelona ha ganado {VictBC} partidos de liga esta temporada, es decir un:
#      {PorVictBC}% de los partidos""")
#print(f"""El FC Barcelona ha perdido {DerrBC} partidos de liga esta temporada, es decir un:
#      {PorDerrBC}% de los partidos""")
#print(f"""El FC Barcelona ha empatado {EmpBC} partidos de liga esta temporada, es decir un:
#      {PorEmpBC}% de los partidos""")
#print(f"""El FC Barcelona tiene {SinJugBC} partidos de liga sin jugar esta temporada, es decir un:
#      {PorSinJugBC}% de los partidos""")
#Se guarda como comentario por que no es necesario su impresion sin embargo, puede ser relevante para ver lo que realiza el codigo.

#Ahora hay que trabajar de manera similar pero con la informacion de los partidos del Real Madrid.

UriRM = 'https://api.football-data.org/v4/teams/86/matches?competitions=PD'#Llamado a la api para obtener la informacion de los 
headers = { 'X-Auth-Token': '8e3f8a085d2241b6888b7e4b469798f3' }           #partidos del Real Madrid en la liga española actual
ResponseRM = requests.get(UriRM, headers=headers)                          
ResRM = ResponseRM.json()

#Definimos las variables donde alamacenaremos la informacion de los resultados
VictRM = 0
DerrRM = 0
EmpRM = 0
SinJugRM = 0
ListRM = [] #Variable definida durante la elaboracion del entregable 3 

for x, y in ResRM.items(): 
    if x == "matches": 
        ContRM = len(ResRM["matches"]) 
        for i in range(ContRM): 
            #print(f"\nPartido numero: {i+1}") 
            #for z,w in ResBC["matches"][i].items():#Obtenemos el items de cada diccionario de la lista            
                #print(f"{z}: {w}")
            Casa = ResRM["matches"][i]["homeTeam"]["name"]  
            Visit = ResRM["matches"][i]["awayTeam"]["name"] 
            Gan = ResRM["matches"][i]["score"]["winner"]
            
            #Se realiza el mismo procedimiento realizado para recabar los datos del FCB, unicamente que ahora se recabaran los datos del 
            #Real Madrid, y se guardaran en otras variables.                                  
            try: 
                posib = re.compile(r"HOME_TEAM")
                lol = posib.search(Gan)
                lol.group()
                #print(f"El {Casa} gano ante el {Visit}")
                if Casa == "Real Madrid CF":
                    VictRM += 1
                    ListRM.append(1)
                elif Casa != "Real Madrid CF":
                    DerrRM += 1
                    ListRM.append(2)
            except:
                try: 
                    posib = re.compile(r"AWAY_TEAM")
                    lol = posib.search(Gan)
                    lol.group()
                    #print(f"El {Visit} gano ante el {Casa}")
                    
                    if Visit == "Real Madrid CF":  #Si el visitante es el barcelona le sumamos uno a las victorias
                        VictRM += 1
                        ListRM.append(1)
                    elif Visit != "Real Madrid CF":  #Si no lo es le sumamos uno a las derrotas
                        DerrRM += 1
                        ListRM.append(2)  
                except:
                    try:
                        posib = re.compile(r"DRAW")
                        lol = posib.search(Gan)
                        lol.group()
                        #print(f"Se empato el partido entre {Casa}-{Visit}")
                        EmpRM += 1 #Si se empato el partido no hay que comprobar quien empato asi que solo se suma 1 a los empates.
                        ListRM.append(3)
                    except:
                        #print(f"No se ha jugado el partido entre {Casa}-{Visit}")
                        SinJugRM += 1

PorVictRM = round(((VictRM/(VictRM+DerrRM+EmpRM+SinJugRM))*100),2)
PorDerrRM = round(((DerrRM/(VictRM+DerrRM+EmpRM+SinJugRM))*100),2)
PorEmpRM = round(((EmpRM/(VictRM+DerrRM+EmpRM+SinJugRM))*100),2)
PorSinJugRM = round(((SinJugRM/(VictRM+DerrRM+EmpRM+SinJugRM))*100),2)

#Imprimimos los partidos jugados, sus resultados y el porcentaje que representan los mismos
#print(f"""\nEl Real Madrid ha ganado {VictRM} partidos de liga esta temporada, es decir un:
#      {PorVictRM}% de los partidos""")
#print(f"""El Real Madrid ha perdido {DerrRM} partidos de liga esta temporada, es decir un:
#      {PorDerrRM}% de los partidos""")
#print(f"""El Real Madrid ha empatado {EmpRM} partidos de liga esta temporada, es decir un:
#      {PorEmpRM}% de los partidos""")
#print(f"""El Real Madrid tiene {SinJugRM} partidos de liga sin jugar esta temporada, es decir un:
#      {PorSinJugRM}% de los partidos""")

""""El unico proceso de limpieza de datos que se realizo fue que nosotros tuvimos que realizar el conteo de las victorias, empates,
derrotas y partidos sin jugar, por nuestra cuenta debido a que el conteo que nos proporcionaba la api directamente tenia datos 
erroneos."""

# Estructura para almacenar los partidos procesados

partidos_analizados = []

resultados_barcelona = analizar_partidos(ResBC, "FC Barcelona")
resultados_madrid = analizar_partidos(ResRM, "Real Madrid CF")

# Guardar la información en un archivo CSV
with open('partidos_liga.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
    campos = ["fecha", "local", "visitante", "resultado", "equipo"]
    escritor = csv.DictWriter(archivo_csv, fieldnames=campos)

    escritor.writeheader()
    for partido in partidos_analizados:
        escritor.writerow(partido)

print("Archivo 'partidos_liga.csv' generado exitosamente.")


#Semana 3

# Guardar resultados del Barcelona
with open('resultados_barcelona.txt', 'w') as f:
    f.write(f"Victorias: {VictBC}\n")
    f.write(f"Derrotas: {DerrBC}\n")
    f.write(f"Empates: {EmpBC}\n")
    f.write(f"Sin jugar: {SinJugBC}\n")
    f.write(f"Porcentaje Victorias: {PorVictBC}\n")
    f.write(f"Porcentaje Derrotas: {PorDerrBC}\n")
    f.write(f"Porcentaje Empates: {PorEmpBC}\n")
    f.write(f"Porcentaje Sin jugar: {PorSinJugBC}\n")

# Guardar resultados del Real Madrid
with open('resultados_madrid.txt', 'w') as f:
    f.write(f"Victorias: {VictRM}\n")
    f.write(f"Derrotas: {DerrRM}\n")
    f.write(f"Empates: {EmpRM}\n")
    f.write(f"Sin jugar: {SinJugRM}\n")
    f.write(f"Porcentaje Victorias: {PorVictRM}\n")
    f.write(f"Porcentaje Derrotas: {PorDerrRM}\n")
    f.write(f"Porcentaje Empates: {PorEmpRM}\n")
    f.write(f"Porcentaje Sin jugar: {PorSinJugRM}\n")

    # Segundo script: Lectura y transformación de datos

# Leer archivos
barcelona = leer_resultados('resultados_barcelona.txt')
madrid = leer_resultados('resultados_madrid.txt')

# Mostrar resultados leídos
print("Datos leídos del archivo (Barcelona):")
for k, v in barcelona.items():
    print(f"{k}: {v}")

print("\nDatos leídos del archivo (Madrid):")
for k, v in madrid.items():
    print(f"{k}: {v}")

# Ejemplo de transformación: comparar victorias
if barcelona['Victorias'] > madrid['Victorias']:
    print("\nEl Barcelona tiene más victorias que el Madrid.")
elif madrid['Victorias'] > barcelona['Victorias']:
    print("\nEl Madrid tiene más victorias que el Barcelona.")
else:
    print("\nBarcelona y Madrid tienen las mismas victorias.")

# Ejemplo de análisis adicional: ¿quién tiene mayor porcentaje de empates?
if barcelona['Porcentaje Empates'] > madrid['Porcentaje Empates']:
    print("El Barcelona empata más proporcionalmente.")
else:
    print("El Madrid empata más proporcionalmente (o igual).")

"""Para nuestro analisis la utilizacion del calculo de una media es irrelevante, sin embargo, es interesante conocer la moda, así que
conseguiremos la moda de los resultados utilizando statistics"""

ModaBC = statistics.mode(ListBC)
ModaRM = statistics.mode(ListRM)

if ModaBC == 1:
    print(f"La moda de los resultados del Barcelona es {ModaBC}, es decir victorias.")
elif ModaBC == 2:
    print(f"La moda de los resultados del Barcelona es {ModaBC}, es decir Derrotas.")
elif ModaBC == 3:
    print(f"La moda de los resultados del Barcelona es {ModaBC}, es decir Empates.")  

if ModaRM == 1:
    print(f"La moda de los resultados del Real Madrid es {ModaRM}, es decir victorias.")
elif ModaRM == 2:
    print(f"La moda de los resultados del Real Madrid es {ModaRM}, es decir Derrotas.")
elif ModaRM == 3:
    print(f"La moda de los resultados del Real Madrid es {ModaRM}, es decir Empates.")  

"""Preparación para visualización"""
#Los datos que necesitaremos para nuestro análisis son los porcentajes por lo que, son primordialmente los datos mas importantes y que 
#hay que preparar para su posterior visualización, para ello los guardaremos en un array de numpy para un posterior uso de los mismos 
#mas rapido y sencillo.                                                                           

PorcEq = numpy.array([
    ["          ","Barca", "RM"], ["%Victorias", barcelona["Porcentaje Victorias"], madrid["Porcentaje Victorias"]],
    ["%Derrotas", barcelona["Porcentaje Derrotas"], madrid["Porcentaje Derrotas"]], 
    ["%Empates", barcelona["Porcentaje Empates"], madrid["Porcentaje Empates"]]])
print(PorcEq)