# Sopa de letras
## Resumen
El archivo consta de dos programas los cuales forman una sopa de letras. Tiene un programa en C y otro el Python los cuales ambos cumplen funciones diferentes ambas necesarias para poder jugar.
La sopa de letras posee 3 dificultades las cuales son:

- Fácil: Sólo palabras horizontales de izquierda a derecha y verticales de arriba a abajo. (Complejidad = 0)
- Medio: Palabras horizontales de izquierda a derecha, verticales de arriba a abajo o diagonales de esquina sup. izq a esquina inf. der. (Complejidad = 1)
- Dificil: Palabras en horizontal, vertical o diagonal sin restricciones. (Complejidad = 2)
- Muy Dificil: Las palabras se pueden cortar, es decir, pueden compartir palabras. (Complejidad = 3)

En el repositoro se dará un archivo llamado **lemario.txt** el cual contendrá palabras para así poder jugar al juego de manera inmediata.

## Programa en C
El programa en C se encarga de crear un archivo el cuál contendrá las caracteristicas de la sopa de letras a jugar. Este archivo posteriormente será ingresado al programa en Python.

Este programa debe ser ejecutado primero. El usuario deberá previamente crear un archivo .txt el cual contendrá las palabras con las que desea jugar  
y guardarlo en la carpeta contenedora del juego.

Al comienzo de la ejecución, se le pedirá al usuario los siguientes datos:
- DIMENSION: se puede pensar a la sopa de letras como una matriz cuadrada dimension x dimension.
- CANTIDAD DE PALABRAS: cantidad de palabras a ubicar en la sopa de letras.
- COMPLEJIDAD: la dificultad del juego.
- NOMBRE DEL ARCHIVO: nombre del archivo txt creado previamente por el usuario.

Cabe aclarar que si el usuario decide ingresar un nivel de dificultad no existente o un numero de palabras mayor a las dadas en el txt, se mostrará por pantalla un mensaje de error y se terminará la ejecución del programa.

Como salida, se obtendrá un archivo txt llamado **Salida** el cual contendrá los datos ingresados previamente.

##### Forma del archivo
DIMENSION
int (numero entero que representa la dimension)

PALABRAS
(palabras elegidas por el programa al azar una debajo de la otra)

COMPLEJIDAD
int(numero entero que representa la complejidad)

##### Ejemplo de salida
DIMENSION

6

PALABRAS

computacion

codigo

teorema

COMPLEJIDAD

3

## Programa en Python
El programa en Python se encarga de generar la matriz (lista de listas) que se usará como tablero
e ir ubicando las palabras aleatoriamente sobre esta teniendo en cuenta todas las consideraciones que pudieran afectar al funcionamiento del juego,
tales como que dada la posicion aleatoria elegida la palabra no entre, que use espacios ya ocupados previamente 
o que en la generacion de letras random para completar la sopa de letras se formen de manera aleatoria palabras que se deben buscar haciendo que una misma palabra aparezca dos veces.

Como ingreso, lo único que pide este programa es el path del archivo **Salida** dado por el programa en C.
Una vez ingresado, se tratará de formar la sopa de letras con las caracteristicas expresadas en el archivo.

Pueden existir casos en los que dada la cantidad de palabras y la dimension, no sea posible ubicar correctamente las palabras o que obligatoriamente se formen palabras repetidas en el completado de la sopa de letras.
El programa en todo momento intentará un número limitado de veces (dimension x dimension, uno por cada lugar) ubicar las palabras o re-generar letras aleatorias.
Una vez cumplida esta cantidad de intentos, el programa imprimirá por pantalla un mensaje de error pidiendo al usuario una menor cantidad de palabras  para dicha dimension y se terminará su ejecución.

Si la sopa de letras puede ser generada, se imprimirá por pantalla junto con las palabras a buscar.

## Ejecucion del programa
### C
Para la ejecucion del programa en C, lo primero es pedir al usuario las caracteristicas de las sopas de letra. Estas serán ingresadas normalmente mediante el uso de la libreria stdio.h.
En el caso que la complejidad ingresada no esté permitida, se le pedirá al usuario mediante el uso de un bucle while que ingrese nuevamente la complejidad. Se hará esto hasta que sea ingresada una complejidad válida.

Posteriormente,  se pide el ingreso del nombre del archivo el cual será guardado en un bloque de memoria apto para contener a 20 caracteres. 
De existir dicho nombre, el programa continúa su ejecución, de lo contrario, mostrará un mensaje de error y terminará la ejecución.

A continuacion, se realizará la apertura del archivo y su lectura. En caso de haber un error en la apertura, esto se le comunicará al usuario.
El archivo se lee una sola vez y en la unica lectura va guardando cada palabra en un arreglo de punteros a punteros de caracteres el cual cuando se guardan una cantidad de 1000 palabras, aumenta la dimension del bloque de memoria utilizado mediante la funcion realloc así puede seguir guardando.

En cada componente del arreglo de punteros a punteros a caracteres, se pide memoria para guardar la longitud de la palabra a guardar + 1 (para tener en cuenta el /0).

Hay una variable k la cual aumentará con cada iteración que llevará la cuenta de cuantas palabras se van ingresando.

Una vez guardadas todas las palabras, se cierra el archivo para evitar errores y se verifica que la cantidad de palabras pedidas no sea mayor a la cantidad de palabras guardadas.

En el caso de ser mayor,  se da un mensaje de error y se termina la ejecucion del programa liberando toda la memoria pedida.

En caso de ser menor, se continua con la ejecucion.

Continuando con la ejecucion, se llama a una funcion la cual es la encargada de elegir las palabras al azar de todas las palabras guardadas y escribirlas en el archivo de salida. Así tambien como escribir las caracteristicas del juego y los títulos correspondientes.

Para la toma de palabras al azar, se realiza un bucle for el cual en cada iteracion elige un numero random entre 0 y la cantidad de palabras totales, de esta manera, se selecciona la palabra correspondiente al lugar del numero random elegido. Esto se realiza un total de la cantidad de palabras a elegir.
En cada iteracion, se verifica que el numero no se encuentre dentro de una lista con los números ya tomados previamente.
En caso que se encuentre, se elige otro numero y en caso que no, se sigue adelante con dicho numero elegido.
Esto se hace para que no se elija una palabra dos veces.

Finalmente, se termina de escribir el archivo de salida, y se libera toda la memoria utilizada.
### Python
El programa en Python como primera medida, inicializa todas la variables a utilizar y pide el path del archivo de salida dado por C.
Realiza una lectura del archivo guardando todo su contenido y segregandolo en diversas variables a utilizar posteriormente y lo cierra.

Dependiendo de la complejidad dada, se llaman a las funciones con una palabra o la misma palabra pero invertida y se ubicarán dentro de la sopa de letras.

La función de ubicacion diagonal, en caso de no poder ubicar la palabra dada, recurrirá a la función que ubica las palabras horizontales o verticales en los niveles 2 y 3,
la cual, a su vez, llama a la función de ubicacion horizontal o vertical base, solo que pasandole un parametro el cual representará la ubicacion de la palabra (horizontal o vertical). 
Esto se hace ya que la ubicacion de las palabras horizontales o verticales es aleatoria, es decir, se elije dentro de la funcion mediante un numero random si la palabra irá horizontal o vertical.
El parámetro pasado por la funcion de ubicacion horizontal y vertical de los niveles 2 o 3 anula esta aleatoriedad y obliga a la palabra a ubicarse de manera horizontal (el parámetro es 1) o vertical (el parámetro es 2).

La funcion ubicacion_horizontal_vertical, intentará ubicar todas las palabras que tengan que ser ubicadas en horizontal y vertical o aquellas que no puedan ser ubicadas en diagonal. 
Para hacer esto, se realiza una recursividad de esta misma función una cantidad finita de veces (dimension x dimension). 
Si la palabra no puede ser ubicada luego de esta cantidad de intentos, se avisa al usuario mediante un mensaje de error y se termina la ejecución del programa.

La variable llamada numero_recursivo sirve para hacer esto. En cada ejecucion, va aumentando de manera que se vaya teniendo la cuenta de la cantidad de veces que se intentó ubicar la palabra.

Luego de haber ubicado correctamente todas las palabras, se llama a la funcion encargada de completar todos los espacios vacios con letras random. 
Estas letras son elegidas mediante la funcion ``random.choice(string.ascii_lowercase)`` la cual devuelve una letra minuscula al azar del diccionario (sin la ñ).

Al completar esta función su ejecución, se llama a ``verificacion_final``. Funcion que se encarga de checkear que en el llenado con letras aleatorias previamente hecho, 
no se haya formado alguna palabra que se deba buscar, teniendo asi dos palabras iguales a buscar dentro de la sopa de letras.

Para esto, esta funcion recorre todas las filas, columnas y diagonales de la matriz, guardando los caracteres en una lista y transformando esta lista de caracteres en un string. 
Una vez hecho esto, llama a la funcion ``checkeo`` la cual mediante el uso de las estructura ``for in`` se encarga de verificar que la palabra a buscar y su inversa no se encuentren dentro del string correspondiente a la linea de la matriz.
Si la palabra actual se encuentra dentro de esa linea, la funcion retorna una variable llamada ``veces_encontrada`` la cual valdrá 1.
Caso contrario, vale 0.

Al final de completar el checkeo de cuantas veces aparece la palabra en todas las direcciones posibles, se guardará en un diccionario el cual la clave será la palabra actual y el valor será la cantidad de veces que aparece.
Esto se hará una vez por cada palabra a buscar.

Al final de ``verificacion_final``, se recorrerá el diccionario preguntando si algun valor es mayor a 1.
Caso positivo, se llama a la funcion ``sopa_de_letras`` la cual es encargada de generar el juego y se vuelve a generar el juego.
Esto se hará un total de veces equivalente a dimension x dimension para así evitar posibles bucles infinitos.
Una vez cumplida esta cantidad de veces, se muestra un mensaje de error pidiendo el ingreso de menos palabras y se termina el programa.
La variable ``cantidad_recursividad`` sirve para llevar la cuenta de esto.

Caso negativo, se llama a la funcion ``muestra_matriz`` la cual mostrará las palabras a buscar junto con la sopa de letras ya creada.

Otra forma de hacer esto para no tener que rearmar la sopa de letras desde cero, es crear dos matrices. Una principal la cual será el tablero del juego final y la otra auxiliar. Al momento de completar la matriz en los espacios no ocupados por palabras con letras aleatorias, también se completa la matiz auxiliar en los mismos espacios, quedando ceros en los lugares ocupados por palabras.
Si en la verificacion final aparece una palabra repetida, simplemente se re-eligen letras random en los lugares de la matriz principal donde en la matriz auxiliar no hay un 0. Se repite este proceso hasta que no se repita ninguna palabra.

La implementacion seria:
    
	for linea in matriz_auxiliar:
            for elemento in linea:
                if elemento != 0:
                    letra_random = random.choice(string.ascii_lowercase)
                    matriz_principal[i][j] = letra_random
                j += 1
            i += 1
            j = 0


La ultima funcion de todas es la llamada ``test``, la cual mediante el uso de ``assert``, permite el testeo del correcto funcionamiento de las funciones que son posibles de testear.
__________________________________________________________________________________________________________________________________________________________________
ARREGLO DE EFICIENCIA
El programa sería eficiente si en lugar de intentar ubicar las palabras un numero finito de intentos en el tablero, se utilizaria el algoritmo conocido como "Backtracking" donde se haria una iteracion o recursividad que permitiria checkear si la palabra puede entrar en el tablero lo cual en caso positivo la ubicaria y en caso negativo volvería al nodo anterior asi se genera un nuevo tablero en el cual se volvería a checkear si la palabra puede ser ubicada.
