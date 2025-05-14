import requests
import json
import re
import csv
import statistics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from openpyxl import Workbook
from openpyxl.styles import Font

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

#Otro análisis estadístico que se utilizo fue la obtencion de los porcentajes mas al principio del código, fue realizado mediante una
#sintaxis propia y es el principal pilar para resolver el problema planteado

"""Preparación para visualización"""
#Los datos que necesitaremos para nuestro análisis son los porcentajes por lo que, son primordialmente los datos mas importantes y que 
#hay que preparar para su posterior visualización, para ello los guardaremos en un array de numpy para un posterior uso de los mismos 
#mas rapido y sencillo.                                                                           

PorcEq = np.array([
    ["          ","Barca", "RM"], ["%Victorias", barcelona["Porcentaje Victorias"], madrid["Porcentaje Victorias"]],
    ["%Derrotas", barcelona["Porcentaje Derrotas"], madrid["Porcentaje Derrotas"]], 
    ["%Empates", barcelona["Porcentaje Empates"], madrid["Porcentaje Empates"]]])

#Grafica de barras superpuestas que comparan cantidad de victorias, empates y derrotas
label = ["Victorias", "Derrotas", "Empates"] #Labels que tendrian en el eje x las barras
Resultados = {
    "Barcelona": np.array([VictBC, DerrBC, EmpBC]),
    "Real Madrid": np.array([VictRM, DerrRM, EmpRM]),
}  #Equipos y su cantidad de victorias, derrotas y empates.

fig, ax = plt.subplots() #Se crea una figura, (plano) y la grafica que habra en esta figura
piso = np.zeros(3) #El valor minimo del eje y para cada barra, (0)
i = 0 #Contador
color = ["red", "white"] #Colores que tendran las barras, rojo del barcelona y blanco del real madrid ya que son representativos.
for equipo, Resultado in Resultados.items(): #Ciclo que iterara en el diccionario de resultados
    grafica = ax.bar(label, Resultado, label=equipo, bottom=piso, color = color[i]) #Creamos la grafica
    piso += Resultado #Esto hace que la siguiente barra en generar se pondra arriba de la otra, se pueden sobre poner una sobre otra,
    #sin embargo no se verian bien por como son los datos.
    i += 1
    ax.bar_label(grafica, label_type='center') #Hace que nos muestre la cantidad de datos que representa cada barra
    
ax.set_title("""Cantidad de Victorias
             Derrotas y Empates""") #Ponemos titulo a la gráfica
ax.set_facecolor("#ffffb5") #Ponemos el fondo en un amarillo claro en Hex, ya que, ambos equipos tienen amarillo en su escudo
ax.legend(loc="upper right", facecolor = "#ffffb5", edgecolor = "black" )  #Una leyenda que nos indica que color representa a cada equipo
plt.savefig("Graficas de barras sobrepuestas de los resultados de los equipos.jpg") #Guardamos la gráfica en un .jpg
plt.show() #La mostramos

#Gráfica de lineas que muestra el comportamiento de los resultados con el paso de las jornadas.
fig, (ax1, ax2) = plt.subplots(2, 1) #Creamos una figura que tendra dos filas y una columna, y dos graficas.
ax1.plot(range(0,len(ListBC),1), ListBC, marker = "^",lw = 0.2, mec = "red", color = "blue") #Creamos la primera gráfica

personalizacion = mpatches.Patch(color = "None", label="""1.- Victoria 
2.-Derrota 
3.-Empate""")
ax1.legend(handles=[personalizacion], facecolor = "#ffffb5", edgecolor = "black" )
#El codigo para realizar esta personalizacion fue obtenido de la pagina de documentacion de matplotlib, de la siguiente url:
#https://matplotlib.org/stable/users/explain/axes/legend_guide.html#legend-guide, unicamente se adapto a lo que se necesitaba

ax1.set_facecolor("#ffffb5") #Codigo Hex del color amarillo claro que s epondra en el fondo de la primera gráfica
ax1.set_xticks(range(0,len(ListBC),2)) #Se selecciona las marcas que habra en el eje x
ax1.set_yticks([1, 2, 3]) #Se seleccionan las marcas que habra en el eje y 
ax1.set_title("""Resultados Barcelona y Real Madrid respectivamente 
a lo largo de la temporada""") #Titulo 
ax1.set_ylabel("Barcelona") #Mensaje en el eje y

ax2.plot(range(0,len(ListRM),1), ListRM, marker = "*", lw = 0.2, mec = "white", mew = 1.5, color = "yellow") #Creamos la segunda gráfica
ax2.set_facecolor("grey") #Ponemos color gris en el fondo de la segunda gráfica
ax2.set_xticks(range(0,len(ListRM),2)) #Marcas que habra en el eje x
ax2.set_yticks([1, 2, 3]) #Marcas que habra en el eje y
ax2.set_xlabel("Jornada") #Mensaje en el eje x
ax2.set_ylabel("Real Madrid") #Mensaje en el eje y 

plt.savefig("Grafica lineas y puntos que indica resultados jornada a jornada.jpg") #Guardamos la gráfica
plt.show() #Mostramos

#Gráfica de pastel que contiene los porcentajes de resultados de Real Madrid y Barcelona
PorBar = [PorcEq[1][1], PorcEq[2][1], PorcEq[3][1]]#Lista con los porcentajes que representa cada cantidad de resultados sobre el total
PorRM = [PorcEq[1][2], PorcEq[2][2], PorcEq[3][2]]#Lista con los porcentajes que representa cada cantidad de resultados sobre el total
separar = (0.1, 0, 0) #Separacion que tendra cada rebanada de la gráfica de pastel, en este caso solo el primer parámetro que sera el
#victorias.

fig, (ax1, ax2) = plt.subplots(1, 2) #Se crea la figura con una fila y dos columnas y dos gráficas.
fig.set_facecolor("black") #Se pone un fondo negro a la figura
ax1.pie(PorBar, labels = label, autopct='%1.1f%%', textprops = dict(color = "#807c77", weight="bold"), 
colors = ["red", "blue", "#ffffb5"], explode = separar, shadow = True, startangle=90) #Se crea la gráfica de pastel, autopct lo
#que hace es que muestre los porcentajes que representa cada rebanada con un solo decimal, textprops nos permite modificar las propiedades
#de los textos que mostraremos en el gráfico, weight = "bold" pone en negritas el textro que se muestra en el gráfico, colors nos deja
#pasar una lista con los colores que usara cada rebanada, explode nos permite indicar la separacion de cada rebanada, shadow nos deja 
#poner una sombra a la gráfica y startangle gira la gráfica segun los grados que indiquemos.
ax1.set_title("""Porcentaje de resultados 
del Barcelona""", color = "white")#Titulo

ax2.pie(PorRM, labels = label, autopct='%1.1f%%', textprops = dict(color = "#807c77", weight="bold"), 
colors = ["white", "#e39d3f", "blue"], explode = separar, shadow = True, startangle=90) #Gráfica 2 con las mismas caracterísitcas que la 1
ax2.set_title("""Porcentaje de resultados 
del Real Madrid""", color = "white") #Titulo
plt.savefig("Grafica de Pastel con los porcentajes de los resultados del Barcelona y Real Madrid.jpg") #Guardamos la figura
plt.show() #Mostramos la gráfica

#Únicamente se realizaron estas tres gráficas debido a que realizar una cuarta únicamente seria redundante y no aportaría absolutamente nada a la resolución 
#de la problemática inicial del problema, con estas tres gráficas es mas que suficiente para realizar la comparación de los resultados del Barcelona y 
#Real Madrid de la actual liga española, como solo se realizaron estos tres gráficos fue que se enfoco en darle un aspecto más trabajado a las gráficas.

#Exportar datos a excel
wb = Workbook()

# Añadir hoja para FC Barcelona
ws_barca = wb.active
ws_barca.title = "FC Barcelona"
ws_barca.append(["Fecha", "Local", "Visitante", "Resultado", "Equipo"])
for cell in ws_barca[1]:
    cell.font = Font(bold=True)
for i in range(len(ListBC)):
    match = ResBC["matches"][i]
    resultado = {1: "Ganado", 2: "Perdido", 3: "Empatado"}.get(ListBC[i], "Sin jugar")
    ws_barca.append([
        match["utcDate"],
        match["homeTeam"]["name"],
        match["awayTeam"]["name"],
        resultado,
        "FC Barcelona"
    ])

# Añadir hoja para Real Madrid
ws_madrid = wb.create_sheet("Real Madrid")
ws_madrid.append(["Fecha", "Local", "Visitante", "Resultado", "Equipo"])
for cell in ws_madrid[1]:
    cell.font = Font(bold=True)


for i in range(len(ListRM)):
    match = ResRM["matches"][i]
    resultado = {1: "Ganado", 2: "Perdido", 3: "Empatado"}.get(ListRM[i], "Sin jugar")
    ws_madrid.append([
        match["utcDate"],
        match["homeTeam"]["name"],
        match["awayTeam"]["name"],
        resultado,
        "Real Madrid"
    ])
wb.save("resultados_laliga.xlsx")