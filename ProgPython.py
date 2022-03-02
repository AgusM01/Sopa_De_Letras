#El Programa en Python toma el arhivo SalidaC.
#Usando este archivo, genera una Sopa de Letras teniendo en cuenta la Complejidad:

#0. Fácil: Sólo palabras horizontales de izquierda a derecha y verticales de arriba a abajo.
#1. Medio: Palabras horizontales de izquierda a derecha, verticales de arriba a abajo o diagonales de esquina sup. izq a esquina inf. der.
#2. Dificil: Palabras en horizontal, vertical o diagonal sin restricciones.
#3. Muy Dificil: Las palabras se pueden cortar, es decir, pueden compartir palabras.

from calendar import c
from itertools import count
import random
import string
import math
#archivo: Abre el archivo y pone sus elementos en una lista
#archivo: none -> list
#No recibe nada
#Devuelve una lista formada por los elementos del archivo
def archivo ():
    juego_config_lista = []
    nombre_arhivo = input("Ingrese el path del archivo: ")
    archivo_file = open(nombre_arhivo, 'r')
    for x in archivo_file.readlines():
        juego_config_lista.append(x)
    archivo_file.close()
    return juego_config_lista

#lista_sin_ultimo: quita los \n de cada string de la lista
#lista_sin_ultimo: list -> list
#toma la lista con los elementos del archivo
#devuelve una nueva lista con los mismos elementos solo que de cada string saca el \n
def lista_sin_ultimo(juego_config_lista):
    juego_config_lista_noN = []
    c = 0
    for j in juego_config_lista:
        
        if c != (len(juego_config_lista) - 1): #EL ULTIMO ELEMENTO NO TIENE \n ASI QUE NO SE LO QUITA
            pal_actual = j[:-1]
        else:
            pal_actual = j
        juego_config_lista_noN.append(pal_actual) 
        c += 1
    return juego_config_lista_noN

#crea_lista_palabras: crea una lista con las palabras que irán en la sopa de letras
#crea_lista_palabras: list -> list
#toma la lista que contiene a todos los elementos del archivo (sin el \n)
#devuelve una lista formada unicamente por las palabras a utilizar en la sopa de letras
def crea_lista_palabras (juego_config_lista_noN):
    lista_palabras = []
    c = 0
    for k in juego_config_lista_noN:
        if k == "COMPLEJIDAD":
            c = 0            

        if c == 1:
            lista_palabras.append(k)
    
        if k == "PALABRAS":
            c = 1
    return lista_palabras

#crea_dict: crea un diccionario que contiene las configuraciones del juego el cual usa como Key las palabras tales como
# "DIMENSION", "PALABRAS", "COMPLEJIDAD" y como value cada valor asociado a estas palabras
#crea_dict: list list -> dict
#toma dos listas: una es todas las palabras del archivo (sin el \n) y la otra es la lista de solo las palabras a buscar en la sopa de letras
#devuelve un diccionario
def crea_dict(juego_config_lista_noN, lista_palabras):
    juego_config = {}
    c = 0
    for l in juego_config_lista_noN:
        if c == 1:
            juego_config["DIMENSION"] = l
            c = 2
        if c == 2:
            juego_config["PALABRAS"] = lista_palabras
            c = 0
        if c == 3:
            juego_config["COMPLEJIDAD"] = l
            c = 0
        
        if l == "DIMENSION":
            c = 1
        if l == "COMPLEJIDAD":
            c = 3
        
    return juego_config

#muestra_matriz: imprime la matriz por pantalla
#muestra_matriz list(list) list -> none
#toma la matriz de la sopa de letras 
#muestra dicha matriz por pantalla
def muestra_matriz(matriz, lista_palabras):

    print("Las palabras a buscar son: ")
    for palabra in lista_palabras:
        print("- ",palabra)
    
    print(" ")
    #MUESTRA LA SOPA DE LETRAS
    for linea in matriz:
        for letra in linea:
            print(letra, end='  ')
        print()
    print()

#completa la matriz (tablero) que ya tiene las palabras ubicadas con letras minúsculas aleatorias
#completa_matriz: list(list), int, list, int, int -> none
#toma la matriz(tablero), la dimension, la lista de palabras a buscar y la complejidad
#no devuelve nada ya que solo se encarga de completar la matriz y llamar a la funcion que realizará el checkeo final
def completa_matriz(matriz, dimension, lista_palabras, complejidad, cantidad_recursividad):
    i = 0
    j = 0

    #VA COMPLETANDO LA MATRIZ CON LETRAS RANDOM
    for linea in matriz:
        for elemento in linea:
            if elemento == 0:
                letra_random = random.choice(string.ascii_lowercase)
                matriz[i][j] = letra_random
            j += 1
        i += 1
        j = 0
    #LLAMA A LA FUNCIÓN QUE REALIZARÁ EL CHECKEO FINAL
    verificacion_final(matriz, dimension, lista_palabras, complejidad, cantidad_recursividad)

#checkea que cada palabra este una sola vez en cada linea, sea esta horizontal, vertical o las diagonales
#checkeo: string, string, string -> int
#toma la palabra formada por la linea, columna o diagonal actual a buscar
#retorna 1 si la palabra a buscar está dentro del string formado por la linea, columna o diagonal, un 2 si tambien esta la invertida y un 0 si no está.
def checkeo (palabra_formada, palabra, palabra_invertida):
    
    veces_encontrada = 0
    
    #SI ENCUENTRA LA PALABRA A BUSCAR DENTRO DE LA PALABRA FORMADA POR LA LINEA O DIAGONAL, LE ASIGNA 1 A LA CANTIDAD DE VECES ENCONTRADA 
    if (palabra in palabra_formada):
        veces_encontrada += 1
    
    #SI ENCUENTRA LA PALABRA INVERTIDA A BUSCAR DENTRO DE LA PALABRA FORMADA POR LA LINEA O DIAGONAL, LE ASIGNA 1 A LA CANTIDAD DE VECES ENCONTRADA 
    if (palabra_invertida in palabra_formada):
        veces_encontrada += 1
    
    return veces_encontrada

#realiza la verificacion final para tener en cuenta los casos donde al completar la sopa con letras random se formen palabras que haya que buscar
#lo que hace es buscar cuantas veces aparece cada palabra y si lo hace mas de una vuelve a crear la sopa de letras hasta que cada palabra
#aparezca solo una vez
#verificacion_final: list(list), int, list, int, int -> none
#toma la matriz(seria el tablero), la dimension, la lista de palabras a buscar y la complejidad
#no devuelve nada ya que solo checkea que no haya palabras repetidas
def verificacion_final(matriz, dimension, lista_palabras, complejidad, cantidad_recursividad):
    palabra_caracter = []
    fila = 0
    palabra_formada = " "
    veces_encontrada = 0
    repetida = 0
    veces_cada_palabra = {}
    
    for palabra in lista_palabras:
        palabra_invertida = invertir_cadena(palabra)

        #VERIFICACION PARA CADA PALABRA QUE PUEDA ESTAR EN HORIZONTAL
        for fila in range (0, dimension):
            for columna in range (0, dimension):
                palabra_caracter.append(matriz[fila][columna]) #SE VAN GUARDANDO LOS CARACTERES DE LA LINEA ACTUAL A BUSCAR EN UNA LISTA

            palabra_formada = "".join(palabra_caracter)
            
            veces_encontrada += checkeo (palabra_formada, palabra, palabra_invertida)      
            palabra_formada = " "
            palabra_caracter = []    
        

        #VERIFICACION PARA CADA PALABRA QUE PUEDA ESTAR EN VERTICAL
        for columna in range (0, dimension):
            for fila in range (0, dimension):
                palabra_caracter.append(matriz[fila][columna]) #SE VAN GUARDANDO LOS CARACTERES DE LA COLUMNA ACTUAL A BUSCAR EN UNA LISTA
        
            palabra_formada = "".join(palabra_caracter)
            
            veces_encontrada += checkeo (palabra_formada, palabra, palabra_invertida)      
            palabra_formada = " "
            palabra_caracter = []           
           
        #VERIFICA LAS PALABRAS DIAGONALES DE DERECHA A IZQUIERDA
        
        #DE DERECHA A IZQUIERDA PRIMERA MITAD (DESDE ESQUINA INFERIOR IZQUIERDA HASTA DIAGONAL MEDIA)
        posicion_linea = 0
        columna = 0
        linea = 0
        for linea in range (0, dimension):
            posicion_linea = (dimension - 1) - linea
            for columna in range(0, linea + 1):
                palabra_caracter.append(matriz[posicion_linea + columna][columna]) #SE VAN GUARDANDO LOS CARACTERES DE LA DIAGONAL ACTUAL A BUSCAR EN UNA LISTA
        
            palabra_formada = "".join(palabra_caracter)  
            veces_encontrada += checkeo (palabra_formada, palabra, palabra_invertida)      
            palabra_formada = " "
            palabra_caracter = []    
        
        #DE DERECHA A IZQUIERDA SEGUNDA MITAD (DESDE ESQUINA SUPERIOR DERECHA HASTA DIAGONAL MEDIA SIN INCLUIR)
        posicion_columna = 0
        for columna in range (0, dimension - 1):
            posicion_columna = (dimension - 1) - columna
            
            for linea in range(0, columna + 1):  
                palabra_caracter.append(matriz[linea][posicion_columna + linea]) #SE VAN GUARDANDO LOS CARACTERES DE LA DIAGONAL ACTUAL A BUSCAR EN UNA LISTA
        
            palabra_formada = "".join(palabra_caracter)
            veces_encontrada += checkeo (palabra_formada, palabra, palabra_invertida)      
            palabra_formada = " "
            palabra_caracter = []    
        
        #DE IZQUIERDA A DERECHA PRIMERA MITAD (DESDE ESQUINA INFERIOR IZQUIERDA HASTA DIAGONAL MEDIA)
        posicion_linea = 0
        for linea in range (0, dimension):
            for columna in range(0, linea + 1):
                palabra_caracter.append(matriz[linea - columna][columna]) #SE VAN GUARDANDO LOS CARACTERES DE LA DIAGONAL ACTUAL A BUSCAR EN UNA LISTA
        
            palabra_formada = "".join(palabra_caracter)
            veces_encontrada += checkeo (palabra_formada, palabra, palabra_invertida)      
            palabra_formada = " "
            palabra_caracter = []    
        
        #DE IZQUIERDA A DERECHA PRIMERA MITAD (DESDE ESQUINA INFERIOR IZQUIERDA HASTA DIAGONAL MEDIA SIN INCLUIR)
        posicion_columna = 0
        posicion_linea = 0
        for columna in range (0, dimension - 1):
            posicion_columna = (dimension - 1) - columna
            for linea in range(0, columna + 1):
                posicion_linea = (dimension - 1) - linea
                palabra_caracter.append(matriz[posicion_linea][posicion_columna + linea])#SE VAN GUARDANDO LOS CARACTERES DE LA DIAGONAL ACTUAL A BUSCAR EN UNA LISTA
        
            palabra_formada = "".join(palabra_caracter)
            veces_encontrada += checkeo (palabra_formada, palabra, palabra_invertida)      
            palabra_formada = " "
            palabra_caracter = []    

        veces_cada_palabra[palabra] = veces_encontrada
        veces_encontrada = 0

    #SE VERIFICA QUE LAS PALABRAS APAREZCAN SOLO UNA VEZ 
    for elemento in veces_cada_palabra:
        if veces_cada_palabra[elemento] > 1:
            repetida = 1
    
    #SI APARECE MAS DE UNA VEZ, AUMENTA LA VARIABLE RECURSIVIDAD Y REARMA LA SOPA DE LETRAS
    if repetida == 1:
        cantidad_recursividad += 1
        sopa_de_letras(lista_palabras, complejidad, dimension, cantidad_recursividad)
        repetida = 0
    else: #DE LO CONTRARIO MUESTRA LA SOPA DE LETRAS
        muestra_matriz(matriz, lista_palabras)
        repetida = 0

#ubicacion_horizontal_vertical: ubica aleatoriamente la palabra dada de manera horizontal o vertical
#ubicacion_horizontal_vertical: int, list(list), string, int, int, int --> none
#recibe como entrada la dimension de la sopa de letras, la matriz, la palabra, la ubicacion predeterminada, la complejidad y el numero_recursivo
#va ubicando cada caracter de la palabra eligiendo aleatoriamente la orientacion vertical u horizontal de la palabra
def ubicacion_horizontal_vertical(dimension, matriz, palabra, ubicacion_predeterminada, complejidad, numero_recursivo):
    #INICIALIZACION DE VARIABLES
        ubicacion_nivel_1 = 0
        palabra_letra_por_letra_actual = []
        posicion_i = 0
        posicion_j = 0
        bandera = 0
        cantidad_letras = 0
        posicion_fin_palabra_j = 0
        posicion_fin_palabra_i = 0
        contador_veces = 0
        no_ubico = 0

        #SI HIZO LA RECURSION UN TOTAL DE ELEMENTOS DE LA MATRIZ, SIGNIFICA QUE NO PUDO UBICAR LAS PALABRAS Y SE DEBEN ELEGIR MENOS
        if (numero_recursivo == dimension*dimension):
            print("No se pudo ubicar la palabra. Pruebe con una menor cantidad de palabras. ")
            numero_recursivo = 0
            exit()

        if ubicacion_predeterminada == 0:
            #ELIJE LA ORIENTACION DE LA PALABRA
            ubicacion_nivel_1 = random.randint(1,2) 
        else:
            ubicacion_nivel_1 = ubicacion_predeterminada

        #CREA UNA LISTA CON LOS CARACTERES DE LA PALABRA
        for caracter in palabra:
            palabra_letra_por_letra_actual.append(caracter) 
            cantidad_letras += 1
            
        #HABRÁ 3 OPCIONES:
        #SI UBICACION ES 1 --> PALABRA HORIZONTAL
        #SI UBICACION ES 2 --> PALABRA VERTICAL   
            
        if ubicacion_nivel_1 == 1: #PALABRA EN HORIZONTAL --> DADO ELEMENTO MATRIZ ij, DEBO VARIAR EL J
            
            while bandera != cantidad_letras:
                #REINICIA LA BANDERA
                bandera = 0
                
                #POSICION i DE LA LETRA
                posicion_i = random.randint(0, (dimension - 1))
                #POSICION j DE LA LETRA
                posicion_j = random.randint(0, (dimension - 1))
                    
                #VERIFICA QUE LA PALABRA ENTRE HORIZONTALMENTE 
                while (posicion_j > (dimension - cantidad_letras)):
                    posicion_j = random.randint(0,(dimension - 1))

                #CALCULA DONDE FINALIZARÁ LA PALABRA EN HORIZONTAL
                posicion_fin_palabra_j = posicion_j + (cantidad_letras - 1)
                    
                #CALCULA LAS POSICIONES QUE OCUPARÁ LA PALABRA Y CHECKEA SI ESTÁ OCUPADO 
                if (complejidad == 3):  
                    k = 0
                    for caracter in palabra_letra_por_letra_actual:
                       
                        if (matriz[posicion_i][posicion_j + k] == 0) or (caracter == matriz[posicion_i][posicion_j + k]):
                            bandera += 1
                        else: bandera = 0
                        k += 1
                        
                else:    
                    for i in range (posicion_j, posicion_fin_palabra_j + 1): 
                        if matriz[posicion_i][i] == 0:
                            bandera += 1
                        else: bandera = 0
                
                contador_veces += 1 #VA LLEVANDO LA CANTIDAD DE VECES QUE TRATA DE UBICAR LA PALABRA
                if contador_veces == (dimension*dimension): #SI LA TRATA DE UBICAR LA CANTIDAD DE CARACTERES Y NO PUEDE LEVANTA LA BANDERA
                    bandera = cantidad_letras
                    no_ubico = 1
                    contador_veces = 0

            if no_ubico == 1: #SI NO UBICO ES 1 SIGNIFICA QUE NO ENCONTRÓ LUGAR POR LO QUE LA UBICA EN VERTICAL
                numero_recursivo += 1
                ubicacion_horizontal_vertical(dimension, matriz, palabra,2, complejidad,numero_recursivo)
            else:
                #UBICA CARACTER POR CARACTER EN LA MATRIZ, VARIANDO LA POSICION j YA QUE LA PALABRA ES HORIZONTAL
                for caracter in palabra_letra_por_letra_actual:
                    matriz[posicion_i][posicion_j] = caracter
                    posicion_j += 1
                    
            #REINICIO DE VARIABLES Y VACIADO DE LISTAS
            posicion_i = 0
            posicion_j = 0
            cantidad_letras = 0
            palabra_letra_por_letra_actual = []
            ubicacion_nivel_1 = 0
            bandera = 0
            posicion_fin_palabra_i = 0
            posicion_fin_palabra_j = 0
            contador_veces = 0
            no_ubico = 0
        
            
        if ubicacion_nivel_1 == 2: #PALABRA EN VERTICAL--> DADO ELEMENTO MATRIZ ij, DEBO VARIAR EL i
            
            while bandera != cantidad_letras:
                bandera = 0
            
                #POSICION i DE LA LETRA
                posicion_i = random.randint(0, (dimension - 1))
                #POSICION j DE LA LETRA
                posicion_j = random.randint(0, (dimension - 1))
                    
                #VERIFICA QUE LA PALABRA ENTRE VERTICALMENTE 
                while (posicion_i > (dimension - cantidad_letras)):
                    posicion_i = random.randint(0,(dimension - 1))
                    
                #CALCULA DONDE FINALIZARÁ LA PALABRA EN VERTICAL
                posicion_fin_palabra_i = posicion_i + (cantidad_letras - 1)

                #CALCULA LAS POSICIONES QUE OCUPARÁ LA PALABRA Y CHECKEA SI ESTÁ OCUPADO O NO
                if complejidad == 3:
                    k = 0
                    for caracter in palabra_letra_por_letra_actual:
                        
                        if (matriz[posicion_i + k][posicion_j] == 0) or (caracter == matriz[posicion_i + k][posicion_j]):
                            bandera += 1
                        else: bandera = 0
                        k += 1
                        
                else:
                    
                    for i in range (posicion_i, posicion_fin_palabra_i + 1):
                        if matriz[i][posicion_j] == 0:
                            bandera += 1
                        else: bandera = 0
                
                contador_veces += 1 #VA LLEVANDO LA CANTIDAD DE VECES QUE TRATA DE UBICAR LA PALABRA
                if contador_veces == (dimension*dimension): #SI LA TRATA DE UBICAR LA CANTIDAD DE CARACTERES Y NO PUEDE LEVANTA LA BANDERA
                    bandera = cantidad_letras
                    no_ubico = 1
                    contador_veces = 0
            

        
            if no_ubico == 1: #SI NO UBICO ES 1 SIGNIFICA QUE NO ENCONTRÓ LUGAR POR LO QUE LA UBICA EN HORIZONTAL
                numero_recursivo += 1
                ubicacion_horizontal_vertical(dimension, matriz, palabra,1, complejidad,numero_recursivo)
            else:
                #UBICA CARACTER POR CARACTER EN LA MATRIZ, VARIANDO LA POSICION i YA QUE LA PALABRA ES VERTICAL
                for caracter in palabra_letra_por_letra_actual:
                    matriz[posicion_i][posicion_j] = caracter
                    posicion_i += 1
                              
            #REINICIO DE VARIABLES Y VACIADO DE LISTA DE CARACTERES DE PALABRA
            posicion_i = 0
            posicion_j = 0
            cantidad_letras = 0
            palabra_letra_por_letra_actual = []
            ubicacion_nivel_1 = 0
            bandera = 0
            posicion_fin_palabra_i = 0
            posicion_fin_palabra_j = 0
            contador_veces = 0
            no_ubico = 0
            

#invertir_cadena: Invierte una cadena dada, haciendo que las ultimas letras sean las primeras y viceversa
#invertir_cadena: string -> string
#toma un string
#retorna el string invertido
#input: hola ; output: aloh
#input: chau ; output: uahc
def invertir_cadena(cadena):
    return cadena[::-1]

#ubica las palabras verticales u horizontales en los niveles 2 y 3
#ubica_palabras_verticales_horizontales_nivel_2_3: int, int, list(list), string, int, int -> none
#toma el numero que representa la ubicacion de la palabra, la dimension, la matriz(seria el tablero), la palabra, la complejidad y el numero recursivo
#no devuelve nada ya que ubica las palabras en la matriz de manera horizontal o vertical
def ubica_palabras_verticales_horizontales_nivel_2_3(ubicacion_nivel, dimension, matriz, palabra, complejidad,numero_recursivo):
        
    if(ubicacion_nivel == 1):
            ubicacion_predeterminada = 1
            ubicacion_horizontal_vertical(dimension, matriz, palabra,ubicacion_predeterminada, complejidad,numero_recursivo)
    elif (ubicacion_nivel == 2):
            ubicacion_predeterminada = 1
            palabra_invertida = invertir_cadena(palabra)
            ubicacion_horizontal_vertical(dimension, matriz, palabra_invertida,ubicacion_predeterminada, complejidad,numero_recursivo)
    elif(ubicacion_nivel == 3):
            ubicacion_predeterminada = 2
            ubicacion_horizontal_vertical(dimension, matriz, palabra,ubicacion_predeterminada, complejidad,numero_recursivo)
    elif(ubicacion_nivel == 4):
            ubicacion_predeterminada = 2
            palabra_invertida = invertir_cadena(palabra)
            ubicacion_horizontal_vertical(dimension, matriz, palabra_invertida,ubicacion_predeterminada, complejidad,numero_recursivo)

#ubicará las palabras en diagonal tanto de izquierda a derecha como de derecha a izquierda
#ubica_diagonal: string, int, list(list), int, int -> none
#toma la palabra, la dimension de la sopa, la matriz (seria el tablero), la orientacion de cada palabra y la complejidad
#no devuelve nada, solo ubica la palabra en la matriz 
def ubica_diagonal (palabra, dimension, matriz, orientacion, complejidad):
    bandera = 0
    bandera2 = 0
    posicion_i = 0
    posicion_j = 0
    posicion_fin_palabra_i = 0
    posicion_fin_palabra_j = 0
    posicion_i_predecida = 0
    posicion_j_predecida = 0
    cantidad_caracteres = 0
    contador_veces = 0
    palabra_letra_por_letra_actual = []
    no_ubico1 = 0
    numero_recursivo = 0
    
    
    
    #CREA UNA LISTA CON LOS CARACTERES DE LA PALABRA
    for caracter in palabra:
        palabra_letra_por_letra_actual.append(caracter) 
        cantidad_caracteres += 1
                
    while(bandera == 0): #VERIFICACION DE POSICIONES A UTILIZAR
        
        posicion_i = random.randint(0, dimension - 1) #ELIJE LAS POSICIONES AL AZAR
        posicion_j = random.randint(0, dimension - 1) #ELIJE LAS POSICIONES AL AZAR
        

        if (orientacion == 1): #SI LA ORIENTACION ES 1, LA UBICA DIAGONAL DE DERECHA A IZQUIERDA

            posicion_fin_palabra_i = posicion_i + (cantidad_caracteres - 1) #CALCULA EL FINAL DE LA PALABRA EN I
            posicion_fin_palabra_j = posicion_j + (cantidad_caracteres - 1) #CALCULA EL FINAL DE LA PALABRA EN J
            
            if ((posicion_fin_palabra_i <= (dimension - 1)) and (posicion_fin_palabra_j <= (dimension - 1))): #PREGUNTA SI LA PALABRA ENTRA
            
                #VARIABLES QUE VERIFICARAN QUE LOS ESPACIOS QUE VA A OCUPAR LA PALABRA ESTEN VACIOS
                posicion_i_predecida = posicion_i
                posicion_j_predecida = posicion_j

                #VERIFICA QUE NO HAYA CARACTERES OCUPADOS   
                if (complejidad == 3):
                    k = 0
                    for caracter in palabra_letra_por_letra_actual:
                        
                        if ((matriz[posicion_i_predecida][posicion_j_predecida] == 0) or (caracter == matriz[posicion_i_predecida][posicion_j_predecida])): #VERIFICA QUE HAYA UN 0 EN EL LUGAR O QUE SEA EL MISMO CARACTER
                            bandera2 += 1 #SI HAY UN CERO, O ES EL MISMO CARACTER AUMENTA LA BANDERA
                        else: bandera2 = 0 #SI NO HAY UN CERO, LA REINICIA 
                        
                        posicion_i_predecida += 1 #AUMENTA LA POSICION PREDECIDA EN i EN CADA ITERACION 
                        posicion_j_predecida += 1 #AUMENTA LA POSICION PREDECIDA EN j EN CADA ITERACION   
                        k += 1
                        
                else:    
                    for posicion_linea in range (0, cantidad_caracteres):
                        
                        if (matriz[posicion_i_predecida][posicion_j_predecida] == 0): #VERIFICA QUE HAYA UN 0 EN EL LUGAR
                            bandera2 += 1 #SI HAY UN CERO, AUMENTA LA BANDERA
                        else: bandera2 = 0 #SI NO HAY UN CERO, LA REINICIA 
                        
                        posicion_i_predecida += 1 #AUMENTA LA POSICION PREDECIDA EN i EN CADA ITERACION 
                        posicion_j_predecida += 1 #AUMENTA LA POSICION PREDECIDA EN j EN CADA ITERACION 

            #SI LA BANDERA2 ES IGUAL A LA CANTIDAD DE CARACTERES SIGNIFICA HAY UN LUGAR OPTIMO PARA UBICAR LA PALABRA
            if bandera2 == cantidad_caracteres:
                bandera = 1
                bandera2 = 0
            #SI ES DISTINTA, SIGNIFICA QUE NO ENCONTRÓ UN LUGAR Y SUMA UN INTENTO
            else:
                bandera2 = 0
                contador_veces += 1

        elif (orientacion == 2): #SI LA ORIENTACION ES 2, LA UBICA DIAGONAL DE IZQUIERDA A DERECHA
            posicion_fin_palabra_i = posicion_i + (cantidad_caracteres - 1) #CALCULA EL FINAL DE LA PALABRA EN I
            posicion_fin_palabra_j = posicion_j - (cantidad_caracteres - 1) #CALCULA EL FINAL DE LA PALABRA EN J
            
            if ((posicion_fin_palabra_i <= (dimension - 1)) and (posicion_fin_palabra_j >= 0)): #PREGUNTA SI LA PALABRA ENTRA
                
                #VARIABLES QUE VERIFICARAN QUE LOS ESPACIOS QUE VA A OCUPAR LA PALABRA ESTEN VACIOS
                posicion_i_predecida = posicion_i
                posicion_j_predecida = posicion_j
                
                if (complejidad == 3):
                    k = 0
                    for caracter in palabra_letra_por_letra_actual:
                    
                        if ((matriz[posicion_i_predecida][posicion_j_predecida] == 0) or (caracter == matriz[posicion_i_predecida][posicion_j_predecida])): #VERIFICA QUE HAYA UN 0 EN EL LUGAR
                            bandera2 += 1 #SI HAY UN CERO, AUMENTA LA BANDERA
                        else: bandera2 = 0 #SI NO HAY UN CERO, LA REINICIA 
                        
                        posicion_i_predecida += 1 #AUMENTA LA POSICION PREDECIDA EN i EN CADA ITERACION 
                        posicion_j_predecida -= 1 #DISMINUYE LA POSICION PREDECIDA EN j EN CADA ITERACION    
                        k += 1
                        
                else:    
                    for posicion_linea in range (0, cantidad_caracteres): 
                        
                        if (matriz[posicion_i_predecida][posicion_j_predecida] == 0): #VERIFICA QUE HAYA UN 0 EN EL LUGAR
                            bandera2 += 1 #SI HAY UN CERO, AUMENTA LA BANDERA
                        else: bandera2 = 0 #SI NO HAY UN CERO, LA REINICIA 
                        
                        posicion_i_predecida += 1 #AUMENTA LA POSICION PREDECIDA EN i EN CADA ITERACION 
                        posicion_j_predecida -= 1 #DISMINUYE LA POSICION PREDECIDA EN j EN CADA ITERACION 

            #SI LA BANDERA2 ES IGUAL A LA CANTIDAD DE CARACTERES SIGNIFICA HAY UN LUGAR OPTIMO PARA UBICAR LA PALABRA    
            if bandera2 == cantidad_caracteres:
                bandera = 1
                bandera2 = 0
            #SI ES DISTINTA, SIGNIFICA QUE NO ENCONTRÓ UN LUGAR Y SUMA UN INTENTO
            else:
                bandera2 = 0
                contador_veces += 1

        #SI LA CANTIDAD DE VECES ES TAL LA CANTIDAD DE POSICIONES DE LA MATRIZ EN TOTAL, TERMINA EL WHILE
        if contador_veces == (dimension * dimension):
            no_ubico1 = 1
            bandera = 1 
    
    if (bandera == 1) and no_ubico1 == 0: #SI LA BANDERA ES IGUAL A 1 Y QUEDAN INTENTOS, PUDO UBICAR LA PALABRA
            bandera = 1
            contador_veces = 0 
    else: #SI NO, SIGNIFICA QUE SE TERMINARON LOS INTENTOS Y PONE LA BANDERA EN 0
            bandera = 0
            contador_veces = 0
            no_ubico1 = 0

    if (bandera == 1): #SI LA BANDERA ES IGUAL A 1 SIGNIFICA QUE ENCONTRÓ UN ESPACIO OPTIMO PARA UBICAR LA PALABRA
        
        bandera = 0  #REINICIA LA BANDERA

        if (orientacion == 1):
            #UBICA LA PALABRA
            for caracter in palabra_letra_por_letra_actual:
                matriz[posicion_i][posicion_j] = caracter
                posicion_i += 1
                posicion_j += 1
            
        elif (orientacion == 2):
            #UBICA LA PALABRA
            for caracter in palabra_letra_por_letra_actual:
                matriz[posicion_i][posicion_j] = caracter
                posicion_i += 1
                posicion_j -= 1
    else: #SI LA BANDERA NO ES 1 SIGNIFICA QUE NO ENCONTRÓ LUGAR PARA UBICAR LA PALABRA EN DIAGONAL POR LO QUE LA UBICA HORIZONTAL O VERTICAL
        ubicacion_nivel_3 = random.randint(1,4)
        ubica_palabras_verticales_horizontales_nivel_2_3(ubicacion_nivel_3, dimension, matriz, palabra, complejidad, numero_recursivo) 

#inicializa todas las variables que van a ser utilizadas y llena las listas que contendrán la informacion del juego
#inicializacion: none -> none
#no toma valores
#no devuelve valores
def inicializacion():

    juego_config_lista = []
    juego_config_lista_noN = []
    lista_palabras = []
    juego_config = {}
    cantidad_recursividad = 0
    
    juego_config_lista = archivo()
    juego_config_lista_noN = lista_sin_ultimo(juego_config_lista)
    lista_palabras = crea_lista_palabras(juego_config_lista_noN)
    juego_config = crea_dict(juego_config_lista_noN, lista_palabras)
    
    complejidad = int(juego_config["COMPLEJIDAD"])
    dimension = int(juego_config["DIMENSION"])

    sopa_de_letras(lista_palabras, complejidad, dimension, cantidad_recursividad)

#se encarga de armar el juego, eligiendo aleatoriamente las posiciones de las palabras en base a la complejidad y llamando a las funciones que ubicaran las palabras
#sopa_de_letras: list, int, int -> none
#toma la lista de palabras, la complejidad de la sopa de letras y la dimension
#no devuelve nada ya que solo arma el juego y llama a las funciones correspondientes para finalmente mostrarlo  
def sopa_de_letras(lista_palabras, complejidad, dimension, cantidad_recursividad):
    
    #INTENTA UNA CANTIDAD IGUAL AL CUADRADO DE LA DIMENSION DE QUE NO HAYA REPETIDOS. SI NO PUEDE HACERLO TERMINA EL PROGRAMA PIDIENDO MENOS PALABRAS
    if cantidad_recursividad == dimension*dimension:
        print("Error al generar la sopa de letras. Intente con menor cantidad de palabras.\n")
        cantidad_recursividad = 0
        exit()
    
    matriz = []
    if (complejidad == 0):
        ubicacion_predeterminada = 0
        numero_recursivo = 0

        #CREA LA MATRIZ COMENZANDO CON TODOS CEROS
        for x in range(dimension):
            matriz.append([0]*dimension)
        
        #PARA CADA PALABRA LLAMA A LA FUNCION QUE LAS UBICARÁ VERTICAL U HORIZONTALMENTE DE MANERA RANDOM
        for palabra in lista_palabras:
            ubicacion_horizontal_vertical(dimension, matriz, palabra, ubicacion_predeterminada, complejidad,numero_recursivo)
                    
    
    elif (complejidad == 1):
        ubicacion_nivel_1 = 0
        ubicacion_predeterminada = 0
        cantidad_caracteres = 0
        posicion_fin_palabra = 0
        palabra_letra_por_letra_actual = []
        numero_recursivo = 0
        #NIVEL MEDIO: PALABRAS HORIZONTALES DE IZQUIERDA A DERECHA
        #             VERTICALES DE ARRIBA A ABAJO
        #             DIAGONALES DE ESQUINA SUPERIOR IZQ. A ESQUINA SUPERIOR DER.
        
        #CREA LA MATRIZ COMENZANDO CON TODOS CEROS
        for x in range(dimension):
            matriz.append([0]*dimension)
        
        
        
        #COMO EMPIEZA DE LA POSICION 00 Y POR COMO ESTÁ HECHO EL CÓDIGO EN C NO VA A HABER PALABRAS CON MAS CARACTERES QUE LA DIMENSION
        #SOLO DEBO CHECKEAR SI NO HAY POSICIONES OCUPADAS
        for palabra in lista_palabras:
            
            #ELIJE LA ORIENTACION DE LA PALABRA
            ubicacion_nivel_1 = random.randint(1,3) 
            

            #REINICIO DE VARIABLES Y VACIADO DE LISTAS
            bandera = 0
            posicion_i = 0
            posicion_j = 0
            posicion_fin_palabra = 0
            cantidad_caracteres = 0
            palabra_letra_por_letra_actual = []

            for caracter in palabra:
                palabra_letra_por_letra_actual.append(caracter)
                cantidad_caracteres += 1
                       
            if (ubicacion_nivel_1 == 3):

                posicion_i = 0
                posicion_j = 0
                
                #COMO VA A ESTAR EN DIAGONAL, LAS POSICIONES i Y j SERAN IGUALES
                posicion_fin_palabra = posicion_i + (cantidad_caracteres - 1)
                
                #DEBO CHECKEAR SI ENTRA
                for i in range (posicion_i, posicion_fin_palabra + 1):
                    if matriz[i][i] == 0:
                        bandera += 1
                    else: bandera = 0

                #EN CASO QUE PUEDA ENTRAR, UBICARLA DIAGONALMENTE
                #CASO CONTRARIO, LLAMAR A LA FUNCION QUE LAS UBICA HORIZONTAL O VERTICALMENTE ASI SE REALOCA LA PALABRA
                if bandera == cantidad_caracteres:
                    #UBICA CARACTER POR CARACTER EN LA MATRIZ, VARIANDO LA POSICION j YA QUE LA PALABRA ES HORIZONTAL
                    for caracter in palabra_letra_por_letra_actual:
                        matriz[posicion_i][posicion_j] = caracter
                        posicion_i += 1
                        posicion_j += 1
                else:
                    ubicacion_horizontal_vertical(dimension, matriz, palabra,ubicacion_predeterminada, complejidad,numero_recursivo)
            else:
                ubicacion_horizontal_vertical(dimension, matriz, palabra,ubicacion_predeterminada, complejidad,numero_recursivo)
    
    elif (complejidad == 2):
        ubicacion_nivel_2 = 0
        ubicacion_predeterminada = 0
        cantidad_caracteres = 0
        posicion_fin_palabra = 0
        palabra_letra_por_letra_actual = []
        numero_recursivo = 0
        
        #NIVEL DIFICIL:
            #PALABRAS HORIZONTALES:
                # 1: DE IZQUIERDA A DERECHA
                # 2: DE DERECHA A IZQUIERDA
            #PALABRAS VERTICALES:
                # 3: DE ARRIBA HACIA ABAJO
                # 4: DE ABAJO HACIA ARRIBA
            #PALABRAS DIAGONALES:
                # 5: DE IZQUIERDA A DERECHA - DE ARRIBA HACIA ABAJO
                # 6: DE IZQUIERDA A DERECHA - DE ABAJO HACIA ARRIBA
                # 7: DE DERECHA A IZQUIERDA - DE ARRIBA HACIA ABAJO
                # 8: DE DERECHA A IZQUIERDA - DE ABAJO HACIA ARRIBA

        #CREA LA MATRIZ COMENZANDO CON TODOS CEROS
        for x in range(dimension):
            matriz.append([0]*dimension)

        for palabra in lista_palabras:
            ubicacion_nivel_2 = random.randint(1,8)

            #REINICIO DE VARIABLES Y VACIADO DE LISTAS
            bandera = 0
            posicion_i = 0
            posicion_j = 0
            cantidad_caracteres = 0
            orientacion = 0
            palabra_letra_por_letra_actual = []
            
            
            if (ubicacion_nivel_2 < 5):
                ubica_palabras_verticales_horizontales_nivel_2_3(ubicacion_nivel_2, dimension, matriz, palabra, complejidad, numero_recursivo)         
            elif(ubicacion_nivel_2 == 5):
                orientacion = 1
                ubica_diagonal (palabra, dimension, matriz, orientacion, complejidad)
            elif(ubicacion_nivel_2 == 6):
                orientacion = 1
                palabra_invertida = invertir_cadena(palabra)
                ubica_diagonal (palabra_invertida, dimension, matriz, orientacion, complejidad)
            elif(ubicacion_nivel_2 == 7):
                orientacion = 2
                ubica_diagonal (palabra, dimension, matriz, orientacion, complejidad)
            elif(ubicacion_nivel_2 == 8):
                orientacion = 2
                palabra_invertida = invertir_cadena(palabra)
                ubica_diagonal (palabra_invertida, dimension, matriz, orientacion, complejidad)
    elif (complejidad == 3):
        #NIVEL MUY DIFICIL: AL NIVEL DIFICIL SE LE AGREGA LA POSIBILIDAD QUE LAS PALABRAS SE PUEDAN CORTAR
        
        #LAS PALABRAS PUEDEN COMPARTIR LETRAS 

        #PARA QUE COMPARTAN LETRAS, EN CADA CHECKEO DE LETRA OCUPADA DE CADA POSICION, DEBO PERMITIR QUE SI ESA LETRA ES IGUAL A ALGUNA DE LA PALABRA, QUE PASE EL IF        
        
        ubicacion_nivel_3 = 0
        ubicacion_predeterminada = 0
        cantidad_caracteres = 0
        posicion_fin_palabra = 0
        palabra_letra_por_letra_actual = []
        numero_recursivo = 0

        #CREA LA MATRIZ COMENZANDO CON TODOS CEROS
        for x in range(dimension):
            matriz.append([0]*dimension)

        for palabra in lista_palabras:
            ubicacion_nivel_3 = random.randint(1,8)

            #REINICIO DE VARIABLES Y VACIADO DE LISTAS
            bandera = 0
            posicion_i = 0
            posicion_j = 0
            cantidad_caracteres = 0
            orientacion = 0
            palabra_letra_por_letra_actual = []
            
            if (ubicacion_nivel_3 < 5):
                ubica_palabras_verticales_horizontales_nivel_2_3(ubicacion_nivel_3, dimension, matriz, palabra, complejidad, numero_recursivo)         
            elif(ubicacion_nivel_3 == 5):
                orientacion = 1
                ubica_diagonal (palabra, dimension, matriz, orientacion, complejidad)
            elif(ubicacion_nivel_3 == 6):
                orientacion = 1
                palabra_invertida = invertir_cadena(palabra)
                ubica_diagonal (palabra_invertida, dimension, matriz, orientacion, complejidad)
            elif(ubicacion_nivel_3 == 7):
                orientacion = 2
                ubica_diagonal (palabra, dimension, matriz, orientacion, complejidad)
            elif(ubicacion_nivel_3 == 8):
                orientacion = 2
                palabra_invertida = invertir_cadena(palabra)
                ubica_diagonal (palabra_invertida, dimension, matriz, orientacion, complejidad)

    #LLAMA A LA FUNCION LA CUAL SE ENCARGA DE COMPLETAR LA MATRIZ CON CARACTERES RANDOM Y VERIFICAR QUE NO SE REPITAN PALABRAS
    completa_matriz(matriz, dimension, lista_palabras, complejidad, cantidad_recursividad)

#testeo de las funciones que son posibles de testear
#test : none -> none
#no toma nada
#no devuelve nada ya que simplemente se encarga de testear las funciones
def test ():
    assert(lista_sin_ultimo(["PEDRO\n","JUAN\n","MARCOS"]) == ["PEDRO","JUAN","MARCOS"]) 
    assert(lista_sin_ultimo(["TEOREMA","COMPUTACION","CODIGO"])== ["TEOREM","COMPUTACIO","CODIGO"])
    assert(lista_sin_ultimo(["T","C","C"])== ["","","C"])
    assert(crea_lista_palabras(["DIMENSION","5","PALABRAS","PEDRO","JUAN","MARCOS", "COMPLEJIDAD", "3"]) == ["PEDRO","JUAN","MARCOS"])
    assert(crea_lista_palabras(["DIMENSION","5","PALABRAS","TEOREMA","COMPUTACION","CODIGO", "COMPLEJIDAD", "3"]) == ["TEOREMA","COMPUTACION","CODIGO"])
    assert(crea_lista_palabras(["DIMENSION","5","PALABRAS","COMPUTACION","TEOREMA","COMPLEJIDAD", "3"]) == ["COMPUTACION", "TEOREMA"])
    assert(crea_dict(["DIMENSION","5","PALABRAS","PEDRO","JUAN","MARCOS", "COMPLEJIDAD", "3"], ["PEDRO","JUAN","MARCOS"]) == {"DIMENSION" : "5", "PALABRAS": ["PEDRO","JUAN","MARCOS"], "COMPLEJIDAD" : "3"})
    assert(crea_dict(["DIMENSION","5","PALABRAS","TEOREMA","COMPUTACION","CODIGO","COMPLEJIDAD", "3"], ["TEOREMA","COMPUTACION","CODIGO"]) == {"DIMENSION" : "5", "PALABRAS": ["TEOREMA","COMPUTACION","CODIGO"], "COMPLEJIDAD" : "3"})
    assert(crea_dict(["DIMENSION","5","PALABRAS","COMPUTACION","CODIGO","COMPLEJIDAD", "3"], ["COMPUTACION", "CODIGO"]) == {"DIMENSION" : "5", "PALABRAS": ["COMPUTACION","CODIGO"], "COMPLEJIDAD" : "3"})
    assert(invertir_cadena("computacion") == "noicatupmoc")
    assert(invertir_cadena("codigo") == "ogidoc")
    assert(invertir_cadena("teorema") == "ameroet")
    assert(checkeo("computacion","tacion","noicat") == 1)
    assert(checkeo("teorema","tacion","noicat") == 0)
    assert(checkeo("noicatupmoc","tacion","noicat") == 1)

#llama a las funciones encargadas de jugar y probar al resto de funciones
inicializacion()
test()