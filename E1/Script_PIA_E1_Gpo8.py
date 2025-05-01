import requests
import json
"""De esta api que se utilizara podemos realizar llamadas para obtener diversas informaciones del mundo del futbol, aqui mostraremos 
algunos ejemplos"""

#1er ejemplo y principal utilizacion que haremos de la api
"""La estructura del llamado a la api fue obtenida directamente de la página de documentación de la api, (por eso la utilizacion de 
headers), en este llamado obtenemos la informacion de los partidos del Barcelona en la Liga Española actual, esta api ocupa una key
que se obtuvo creando una cuenta en la pagina de la documentación"""

UrlBC = 'https://api.football-data.org/v4/teams/81/matches?competitions=PD'  
headers = {'X-Auth-Token': '8e3f8a085d2241b6888b7e4b469798f3'}#Esta parte no se repetira en los demas llamados para evitar redundancia       
RespuestaBC = requests.get(UrlBC, headers=headers)                          
ResBC = RespuestaBC.json()

"""Tambien obtenemos los partidos jugados en la Liga española actual del Real Madrid."""

UrlRM = 'https://api.football-data.org/v4/teams/86/matches?competitions=PD'         
RespuestaRM = requests.get(UrlRM, headers=headers)                          
ResRM = RespuestaRM.json()

"""En estos casos el cambio se produce en el id del equipo, el cual es escrito despues de /teams/, viendose de la sig. manera: 
https://api.football-data.org/v4/teams/{id}/matches?competitions=PD   tambien utilizamos un ?competitions=PD para indicar que 
unicamente nos muestre los partidos de la liga española"""

#print del primer ejemplo
"""Mostramos el resultado del json de los partidos del barcelona"""
print("""\n-----------
      Informacion de los partidos del Barcelona en la Primera Division Española actual
      ---------------""")
for x,y in ResBC.items():
    print(f"\n{x}: {y}")
    
"""El resultado es un diccionario con tres llaves:
1.-filters: Contiene filtros que se utilizaron para la busqueda, algunos predefinidos y otros indicados por nosotros como 
competitions
2.-resultSet: Un pequeño resumen de los partidos, la cantidad, la competencia, el primer partido y cuando sera el ultimo, los que 
ya se han jugado y los resultados, aunque los resultados estan mal contados por lo que es necesario hacer el conteo por nuestra parte
3.-matches: contiene una lista con varios diccionarios que contienen informacion relacionada al partido, lo que mas nos importa es que en
esta llave tenemos los partidos y los resultados."""

#2do ejemplo.
"""Otro llamado que podemos hacer es para que nos muestre la informacion de una competicion, en este caso mostraremos de la Primera 
Division española"""

UrlPD = "http://api.football-data.org/v4/competitions/PD"         
RespuestaPD = requests.get(UrlPD, headers=headers) 
ResPD = RespuestaPD.json()

"Mostramos la informacion obtenida"
print("""\n-----------
      Informacion de la Primera Division Española
      ---------------""")
for x,y in ResPD.items():
    print(f"\n{x}: {y}")

"""En este llamado obtenemos diversa informacion como el id de la competicion, su codigo,(en este caso PD), su nombre, su tipo, (liga,
copa nacional, copa internacional, etc), su logo, informacion de la temporada actual, asi como informacion de todas las temporadas 
disputadas en la competicion, (su inicio y fin, cantidad de partidos y el ganador e informacion del mismo)
Competitions tiene varias extensiones con sus respesctivos filtros que nos permiten diversas ver cosas como las siguientes:
1.-(http://api.football-data.org/v4/competitions/{codigo o id}/standings) nos muestra las posiciones de los equipos en la competicion con 
filtros como la temporada, la fecha y una jornada especifica.
2.-(http://api.football-data.org/v4/competitions/{id}/matches) nos muestra unicamente los partidos jugados en la competicion, con filtros
como la fecha, la competicion, el status del partido,(pendiente, jugado, por jugar, etc.)
Entre otras extensiones y filtros."""

#3er y ultimo ejemplo:
"""Tambien podemos obtener informacion de algun equipo, a diferencia de en el primer ejemplo donde solo obtuvimos la informacion de los
partidos de un equipo en concreto, tambien podemos obtener informacion como los jugadores de la plantilla, las competiciones que 
disputan, etc."""

UrlMC = "http://api.football-data.org/v4/teams/65"
RespuestaMC = requests.get(UrlMC, headers=headers)
ResMC = RespuestaMC.json()
#En este caso obtuvimos informacion del equipo del Manchester City en cual juega en la primera division de inglaterra
"""Mostramos los datos obtenidos"""

print("""\n-----------
      Informacion del Manchester City
      ---------------""")
for x,y in ResMC.items():
    print(f"\n{x}: {y}")
    
"""De aqui obtenemos datos como el nombre del equipo, la abreviacion, el id del equipo, su escudo, sitio web, estadio, fundacion,
colores, competicion actual, entrenador y staff, jugadores e informacion de los mismos.
La estructura de la url para utilizarla es:
http://api.football-data.org/v4/teams/{id del equipo}
En este caso no cuenta con filtros, pero contamos con la extension de /matches/ que se mostro en el primer ejemplo"""

"""La api nos permite otros datos muy interesantes como las estadisticas de los contribuidores de gol de los equipos y las competiciones
aunque lamentablemente para acceder a las mismas hay que pagar, las opciones mostradas anteriormente no requieren de pago, unicamente
de la key dada al registrarse en la pagina de la documentacion de la api."""

"""Para el script que estaremos realizando no ocuparemos solicitar informacion al usuario, esto debido a que la problematica planteada
a resolver con los datos que obtendremos de la api es el conocer el porcentaje de las victorias, empates y derrotas tanto del Barcelona
como del Real Madrid en la actual Primera Division Española para poder conocer los estados de forma de ambos clubes.
Entonces al tener ya definidos los equipos de los que obtendremos la informacion no necesitaremos pedirle informacion al usuario.
Sin embargo, la api permite hacer scripts donde si solictariamos informacion al usuario, un ejemplo podria ser el conocer ganadores de
competiciones de algun año indicado, o sin ir mas lejos, algo como lo que estamos realizando pero que en vez de ser de la temporada
actual que sea de alguna temporada indicada."""