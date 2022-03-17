/*El programa debe tener como entrada:
-Lemario: archivo que contiene todas las palabras válidas
-Tamaño de la Sopa de Letras: Un entero que representa el tamaño de la matriz que será la sopa de letras
-Cantidad de palabras: Un entero que representa la cantidad de palabras a buscar
-Complejidad del juego: Un entero de 0 a 3 que representa la complejidad de la sopa de letras

El programa generará:
-Un archivo el cual tendrá toda la información detallada anteriormente
Tipo del archivo:

DIMENSION
-Tamaño (int)
PALABRAS
-Palabra1
-Palabra2
-Palabra3
.
.
.
-Palabra[Cantidad de palabras]
COMPLEJIDAD
-Complejidad (int)*/

#include<stdio.h>
#include<stdlib.h>
#include<assert.h>
#include<time.h>
#include<string.h>

#define BUFFER 30 //Tamaño maximo de caracteres en una palabra

//CONFIGURACION DE SOPA DE LETRAS
void ingreso(int* Dimension, int* CantPalabras, int* Complejidad){
    int D, CP, C, check = 0;

    printf("Ingrese la dimension de la sopa de letras: \n");
    scanf("%d", &D);

    *Dimension = D;    

    printf("Ingrese la cantidad de palabras: \n");
    scanf("%d", &CP);

    *CantPalabras = CP;

    while (check == 0){
        printf("Ingrese el nivel de complejidad: \n");
        scanf("%d", &C);
        if (C >= 0){
            if (C <= 3){
                check = 1;
            }
            else{
                printf("La complejidad debe estar entre 0 y 3. \n");
            }
        }
        else{
            printf("La complejidad debe estar entre 0 y 3. \n");
        }
    }

    *Complejidad = C;
}

//GENERACION DE ARCHIVO DE SALIDA
void archivo_salida(int CantPalabras, int k, int Dimension, int Complejidad, long int r, FILE* SalidaC, char** palabras_archivo){

    SalidaC = fopen("SalidaC.txt","w");
    fputs("DIMENSION\n", SalidaC);
    fprintf(SalidaC, "%d", Dimension);
    fputs("\nPALABRAS\n", SalidaC);
    
    int numeros_elegidos[CantPalabras], bandera = 0;
    
    for (int i = 0; i < CantPalabras; i++){ //Elección de palabras a ubicar en la sopa de letras
        while ((strlen(palabras_archivo[r]) > Dimension + 1)){ //Checkea si la palabra puede caber en la sopa de letras
            while (bandera != i){ //Verifico que los numeros no hayan sido previamente elegidos
            r = random() % k;
            for (int k = 0; k < i; k++){
                
                if (r != numeros_elegidos[k]){
                    bandera += 1;
                }
                else{
                    bandera = 0;
                }       
            }           
        }
        }
        bandera = 0; //Reinicio la bandera
        numeros_elegidos[i] = r;
        fputs(palabras_archivo[r], SalidaC);
    }
    fputs("COMPLEJIDAD\n", SalidaC);
    fprintf(SalidaC, "%d", Complejidad);
    fclose(SalidaC);

}

int main (){
    
    srand(time(NULL)); //Inicalizacion uso de random
    
    //INICIALIZACION DE VARIABLES A UTILIZAR
    int Dimension, CantPalabras, Complejidad, k = 0, t_bloque = 1000;
    char PalabraLeida[BUFFER]; //Crea el arreglo de palabras
    char* nombre_archivo;
    char** palabras_archivo = malloc(sizeof(char*)*t_bloque); //Va doble asterisco ya que estoy guardando la direccion donde esta el puntero de la palabra
    long int r; //Contendrá los numeros random
    FILE* lemario; //Crea la variable ripo FILE que representará al Lemario
    FILE* SalidaC; //Crea la variable ripo FILE que representará a la Salida

    ingreso(&Dimension, &CantPalabras, &Complejidad); //Ingreso de variables mediante el uso de punteros a caracteres.
 
    //APERTURA DE ARCHIVO LEMARIO

    nombre_archivo = malloc(sizeof(char)*20); //ASIGNA UN BLOQUE DE MEMORIA PARA GUARDAR 20 CARACTERES
    if (nombre_archivo == NULL){
        printf("Ha ocurrido un error pidiendo memoria. \n");
        return 0;
    }
    printf("Ingrese el nombre de su archivo incluido el tipo: \n"); //PIDE EL NOMBRE DEL ARCHIVO
    scanf("%s", nombre_archivo); //GUARDA EL NOMBRE DEL ARCHIVO DADO POR EL USUARIO

    lemario = fopen(nombre_archivo,"r"); //ABRE EL ARCHIVO
    
    free (nombre_archivo); //LIBERA EL ESPACIO DE MEMORIA UTILIZADO
    
    //VERIFICACION APERTURA CORRECTA ARCHIVO LEMARIO
    if (lemario == NULL){ 
        printf("Nombre de archivo inválido\n");
        return 0;
    }

    //VERIFICACION PEDIDO DE MEMORIA CORRECTO
    if (palabras_archivo == NULL){
        printf("Ha ocurrido un error pidiendo memoria.\n");
        return 0;
    }

    //TOMA DE PALABRAS DEL LEMARIO Y GUARDADO EN UN ARRAY DE PUNTEROS A PUNTEROS DE CARACTERES

    while (fgets(PalabraLeida, BUFFER, lemario) != NULL){  //Recorre el lemario hasta el final
         
        if (k == t_bloque){
            palabras_archivo = realloc(palabras_archivo, sizeof(char*)*(2 * t_bloque)); //Cuando k llega al final de la memoria, pido más con realloc. 
            t_bloque = t_bloque*2; //Aumenta la variable que será el bloque a pedir
        }  
        palabras_archivo[k] = malloc(sizeof(char)* strlen(PalabraLeida) + 1); //En la direccion correspondiente a palabras_archivo[k], pide memoria para almacenar la palabra leida
        if (palabras_archivo == NULL){
            printf("Ha ocurrido un error pidiendo memoria.\n");
            return 0;
        }
        strcpy(palabras_archivo[k], PalabraLeida); //Copia la palabra leida a esa direccion de memoria.
        k += 1; //Incrementa el contador asi va variando las posiciones en memoria, a su vez K representará la cantidad de palabras en el lemario.   
    }
    
    //CERRADO DE LEMARIO
    fclose(lemario);

    //VERIFICA QUE LA CANTIDAD DE PALABRAS SEA MAYOR O IGUAL A LAS QUE HAY EN EL LEMARIO
    if(CantPalabras > k){
        
        printf("La cantidad de palabras del lemario es menor a la cantidad deseada para jugar.\n");
        
        //LIBERA LA MEMORIA UTILIZADA POR PALABRAS ARCHIVO Y CADA LUGAR DE MEMORIA DE ESTE QUE APUNTABA A ALGUN STRING DEL LEMARIO
        for(int i = 0; i < k; i++){
            free(palabras_archivo[i]);
        }
        free(palabras_archivo);
        
        return 0;
    }
    else{
        //CREA EL ARCHIVO DE SALIDA
        archivo_salida(CantPalabras, k, Dimension, Complejidad, r, SalidaC, palabras_archivo);
    }
    
    //LIBERA LA MEMORIA UTILIZADA POR PALABRAS ARCHIVO Y CADA LUGAR DE MEMORIA DE ESTE QUE APUNTABA A ALGUN STRING DEL LEMARIO
    for(int i = 0; i < k; i++){
        free(palabras_archivo[i]);
    }
    free(palabras_archivo);
    
    return 0;
}
