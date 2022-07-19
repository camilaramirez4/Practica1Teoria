import string
from collections import deque

print(" ___________________________________________________________________________________")
print("|                                                                                   |")
print("|        CONVERSOR DE EXPRESIONES REGULARES A AUTÓMATA FINITO DETERMINÍSTICO        |")
print("|                                                                                   |")
print("|                        ELABORADO POR: Camila Ramírez                              |")
print("|                                                                                   |")
print("| Considere las siguientes indicaciones a la hora de ingresar su expresión regular: |")
print("|  -Para representar la unión, utilice siempre el símbolo ´|´                       |")
print("|  -Para representar la concatenación utilice siempre el símbolo ´.´                |")
print("|  -Para representar el * como superíndice, simplemente ingrese ´*´                 |")
print("|  -Para representar el + como superíndice, simplemente ingrese ´+´                 |")
print("|   EJEMPLO: a.b|(a.((b.a)*.b))|a.(a|b)+                                            |")
print("|___________________________________________________________________________________|")

#Ingreso de la expresión
print("Ingrese la expresión regular a convertir de la manera indicada anteriormente")
#Capturamos la expresión regular ingresada por teclado
ER = input()
print("La expresión regular ingresada es: " + ER)

# Convertimos la expresión regular en una lista, donde cada posición es un operador o un operando
listaER = list(ER)

"""Función que crea un set que contiene todos los caracteres del alfabeto en mayúscula y minúscula, además de los dígitos del 0 al 9"""
def listaAbecedario():
    listaAbc = set(string.ascii_letters + string.digits)
    return listaAbc


# Creamos la lista del abecedario y dígitos (que son los posibles nombres para los símbolos de entrada), y una lista con los operadores
listaAbc = listaAbecedario()
listaOperadores = list("|.*+")


"""Función que verifica que la expresión regular si comience y termine de manera adecuada, retorna True si es así, False de lo contrario
recibe como parámetro la lista de la ER"""
def revInicioYFin(listaER):
    if (listaER[0] == "|" or listaER[len(listaER) - 1] == "|" or listaER[0] == "." or listaER[
        len(listaER) - 1] == "." or
            listaER[0] == ")" or listaER[len(listaER) - 1] == "(" or listaER[0] == "*" or listaER[0] == "+"):
        print("Expresión regular incorrecta, por favor ingrésela de nuevo")
        return False
    return True


"""Función que verifica que entre un operando y un paréntesis haya siempre un operador . o |, retorna True si es así, False de lo contrario,
recibe como parámetro la lista de la ER"""
def revCaracteresYParentesis(listaER):
    for i in range(0, len(listaER)):
        if i != 0:
            if listaER[i] in listaAbc and listaER[i - 1] == ")":
                print("Falta un operador entre el ) y el operando " + listaER[i])
                return False
        if i != len(listaER) - 1:
            if listaER[i] in listaAbc and listaER[i + 1] == "(":
                print("Falta un operador entre el operando " + listaER[i] + " y el (")
                return False
        if i != len(listaER) - 1 and i != len(listaER) - 2:
            if listaER[i] in listaAbc and listaER[i + 1] == "*":
                if listaER[i + 2] == "(":
                    print("Falta un operador entre el operando " + listaER[i] + listaER[i + 1] + " y el (")
                    return False
            if listaER[i] in listaAbc and listaER[i + 1] == "+":
                if listaER[i + 2] == "(":
                    print("Falta un operador entre el operando " + listaER[i] + listaER[i + 1] + " y el (")
                    return False
            if listaER[i] == ")" and listaER[i + 1] == "*":
                if listaER[i + 2] in listaAbc:
                    print("Falta un operador entre el )* y el operando " + listaER[i + 2])
                    return False
            if listaER[i] == ")" and listaER[i + 1] == "+":
                if listaER[i + 2] in listaAbc:
                    print("Falta un operador entre el )+ y el operando " + listaER[i + 2])
                    return False
    return True


"""Función que verifica que los paréntesis estén bien, retorna True si es así, False de lo contrario,
recibe como parámetro la lista de la ER"""
def revParentesis(listaER):
    # Variables
    contAbre = 0
    contCierra = 0

    for i in range(0, len(listaER)):
        if listaER[i] == "(":
            contAbre = contAbre + 1
            if listaER[i + 1] == ")":
                print("Hay paréntesis que no contienen nada")
                return False
        if listaER[i] == ")":
            contCierra = contCierra + 1

    if contAbre == contCierra:
        return True

    print("El número de apertura de paréntesis no coincide con el número de cierre de paréntesis")
    return False


"""Función que verifica que cada "." y cada "|" tenga sus dos operandos como mínimo, retorna True si es así, False de lo contrario,
recibe como parámetro la lista de la ER"""
def revUnionYConcat(listaER):
    # Variables
    cont = 0
    caracAntes = 0
    caracDespues = 0
    listaAux = set("(" + ")" + "*" + "+")
    listaAbcP = set.union(listaAbc, listaAux)

    # Contamos cuantos operadores . y | hay en la expresión
    for i in range(0, len(listaER)):
        if listaER[i] == "|" or listaER[i] == ".":
            cont = cont + 1

        # Comienza en 1 porque en la posición 0  unca puede haber un . o un |
    for i in range(1, len(listaER)):
        if listaER[i] == "|" or listaER[i] == ".":
            if listaER[i - 1] in listaAbcP:
                caracAntes = caracAntes + 1
            if listaER[i + 1] in listaAbcP:
                caracDespues = caracDespues + 1

    if caracAntes == cont and caracDespues == cont:
        return True
    else:
        print("Expresión regular incompleta, por favor ingrésela de nuevo")
        return False


"""Función que verifica que a cada + y * le corresponda un operando, retorna True si es así, False de lo contrario,
recibe como parámetro la lista de la ER"""
def revSuperindices(listaER):
    # Variables
    cont = 0
    caracAntes = 0
    listaAux = set(")")
    listaAbcP = set.union(listaAbc, listaAux)

    # Contamos cuantos operadores . y | hay en la expresión
    for i in range(0, len(listaER)):
        if listaER[i] == "*" or listaER[i] == "+":
            cont = cont + 1

    for i in range(1, len(listaER)):
        if listaER[i] == "*" or listaER[i] == "+":
            if listaER[i - 1] in listaAbcP:
                caracAntes = caracAntes + 1

    if caracAntes == cont:
        return True
    else:
        print("Expresión regular incompleta, por favor ingrésela de nuevo")
        return False


"""Esta función simplemente toma todas las funciones que verifican que la ER esté correcta y las une en una sola,
recibe como parámetro la lista de la ER"""
def revCompleta(listaER):
    if (revInicioYFin(listaER) == True and revCaracteresYParentesis(listaER) == True and revParentesis(
            listaER) == True and revUnionYConcat(listaER) == True and revSuperindices(listaER) == True):
        return True
    else:
        return False


"""Función que obtiene los simbolos de entrada que tendrá el autómata, recibe como parámetro la lista de la ER"""
def getSim(listaER):
    # variables
    simbolos = set()
    simbolo = ""

    for i in range(0, len(listaER)):
        if listaER[i] in listaAbc:
            simbolo = simbolo + listaER[i]
            if i == len(listaER) - 1:
                simbolos.add(simbolo)
        else:
            if simbolo != "":
                simbolos.add(simbolo)
                simbolo = ""

    return simbolos


"""Función que recibe como parámetro la lista de la ER y retorna el número de paréntesis ( que hay en esta"""
def cuentaParentesis(listaER):
    # Variables
    contParentesis = 0

    for i in range(0, len(listaER)):
        if listaER[i] == "(":
            contParentesis = contParentesis + 1

    return contParentesis


"""Función que toma una lista y la convierte en una cadena"""
def listaToString(lista):
    #Variables
    cadena = ""

    for i in range(0, len(lista)):
        cadena = cadena + lista[i]

    return cadena


"""Función que recibe como parámetros una lista de sublistas y un operador, retorna los operandos de dicho operador para cada sublista"""
def getOperandos(lista, operador):
    #Variables
    posiciones = list()
    operandos = ""
    cadena = ""

    for i in range(0, len(lista)):
        sublista = list(lista[i])
        for j in range(0, len(sublista)):
            if sublista[j] == operador:
                posiciones.append(j)

        if len(posiciones) != 0:
            for l in range(0, len(sublista)):
                for j in range(0, len(posiciones)):
                    if l == posiciones[j]:
                        if j == 0:
                            for k in range(0, posiciones[j]):
                                cadena = cadena + sublista[k]
                            operandos = operandos + cadena
                            cadena = ""

                            if len(posiciones) != 1:
                                for k in range(l + 1, posiciones[j + 1]):
                                    cadena = cadena + sublista[k]
                                operandos = operandos + "," + cadena
                                cadena = ""
                            else:
                                if operador != "+" and operador != "*":
                                    for k in range(l + 1, len(sublista)):
                                        cadena = cadena + sublista[k]
                                    operandos = operandos + "," + cadena
                                    cadena = ""
                        elif j == len(posiciones) - 1:
                            for k in range(l + 1, len(sublista)):
                                cadena = cadena + sublista[k]
                            operandos = operandos + "," + cadena
                            cadena = ""
                        else:
                            for k in range(posiciones[j] + 1, posiciones[j + 1]):
                                cadena = cadena + sublista[k]
                            operandos = operandos + "," + cadena
                            cadena = ""
            posiciones.clear()
            if i != len(lista) - 1:
                operandos = operandos + " lista "
        else:
            return False

    return operandos


"""Recibe una cadena y un operador y verifica si en dicha cadena está contenido ese operador, retorna True si es así, False de lo contrario"""
def tieneOperador(cadenaOperandos, operador):
    operandos = list(cadenaOperandos)

    for i in range(0, len(operandos)):
        if operandos[i] == operador:
            return True

    return False


"""Recibe como parámetro el número de filas y columnas y retorna una matriz de esas dimensiones llena de """""
def creaMatriz(filas, columnas):
    #Variables
    matriz = list()
    lista = list()

    for i in range(0, filas):
        for j in range(0, columnas):
            lista.append("")
        matriz.append(lista)
        lista = list()

    return matriz


"""
ACLARACIONES:
origen: es una lista donde se encuentra el origen de cada transición en la construcción de Thompson correspondiente a la ER en cuestión
destino: es una lista donde se encuentra el destino de cada transición en la construcción de Thompson correspondiente a la ER en cuestión
simbolo: es una lista donde se encuentra el simbolo de cada transición en la construcción de Thompson correspondiente a la ER en cuestión
estadoRef: es el estado de referencia después del cual se va a insertar nuevas transiciones"""

"""Recibe como parámetros un estado de referencia, la cantidad de estados a sumar, una lista origen y otra destino,
se usa cuando se va a añadir estados nuevos en medio de la construcción de Thompson, re asigna los valores a los estados"""
def sumaEstRef(estadoRef, sumaEstados, origen, destino):
    for i in range(len(origen)):
        if origen[i] > estadoRef:
            origen[i] = origen[i] + sumaEstados

    for i in range(len(destino)):
        if destino[i] > estadoRef:
            destino[i] = destino[i] + sumaEstados


"""Construcción de Thompson básica, recibe un estado de referencia, una lista de operandos y las listas origen, destino y símbolos"""
def basica(estadoRef, listaoperandos, origen, destino, simbolo):
    for i in range(0, 2):
        origen.append(estadoRef + i)
        destino.append(estadoRef + i)
        simbolo.append("lambda")

    origen.append(estadoRef)
    destino.append(estadoRef + 1)
    simbolo.append(listaoperandos)


"""Construcción de Thompson para la concatenación, recibe un estado de referencia, 
una lista de operandos y las listas origen, destino y símbolos"""
def concatenacion(estadoRef, listaOperandos, origen, destino, simbolo):
    #Variables
    operandos = list(listaOperandos)

    for i in range(1, len(operandos)):
        origen.append(estadoRef + i)
        destino.append(estadoRef + i)
        simbolo.append("lambda")

    origen.append(estadoRef)
    destino.append(estadoRef + 1)
    simbolo.append(operandos[0])

    for i in range(1, len(operandos)):
        origen.append(estadoRef + i)
        destino.append(estadoRef + i + 1)
        simbolo.append(operandos[i])


"""Construcción de Thompson correspondiente a la unión, recibe un estado de referencia, 
una lista de operandos y las listas origen, destino y símbolos"""
def union(estadoRef, listaOperandos, origen, destino, simbolo):
    #Variables
    operandos = list(listaOperandos)

    for i in range(1, (len(operandos)) * 2 + 2):
        origen.append(estadoRef + i)
        destino.append(estadoRef + i)
        simbolo.append("lambda")

    for i in range(0, len(operandos)):
        origen.append(estadoRef)
        destino.append(estadoRef + (i * 2) + 1)
        simbolo.append("lambda")

    for i in range(0, len(operandos)):
        origen.append(estadoRef + (i * 2) + 1)
        destino.append(estadoRef + (i * 2) + 2)
        simbolo.append(operandos[i])

    for i in range(0, len(operandos)):
        origen.append(estadoRef + (i * 2) + 2)
        destino.append(estadoRef + (len(operandos) * 2) + 1)
        simbolo.append("lambda")

    origen.append(estadoRef + (len(operandos) * 2) + 1)
    destino.append(estadoRef + (len(operandos) * 2) + 2)
    simbolo.append("lambda")


"""Construcción de Thompson correspondiente al + como superíndice, recibe un estado de referencia, 
una lista de operandos y las listas origen, destino y símbolos"""
def superiMas(estadoRef, operando, origen, destino, simbolo):
    #Variables
    operando = operando[0]

    for i in range(1, 3):
        origen.append(estadoRef + i)
        destino.append(estadoRef + i)
        simbolo.append("lambda")

    for i in range(0, 3):
        origen.append(estadoRef + i)
        destino.append(estadoRef + i + 1)
        if i == 1:
            simbolo.append(operando)
        else:
            simbolo.append("lambda")

    origen.append(estadoRef + 2)
    destino.append(estadoRef + 1)
    simbolo.append("lambda")


"""Construcción de Thompson correspondiente al * como superíndice, recibe un estado de referencia, 
una lista de operandos y las listas origen, destino y símbolos"""
def superiAsterisco(estadoRef, listaOperando, origen, destino, simbolo):
    superiMas(estadoRef, listaOperando, origen, destino, simbolo)

    origen.append(estadoRef)
    destino.append(estadoRef + 3)
    simbolo.append("lambda")


"""Función que crea la construcción de Thompson para una ER dada o un pedazo de esta (funciona para ER que no contengasn ()),
retorna una lista cuya posición 0 corresponde al contador de estados (total de estados), su posición 1, 2 y 3 son, respectivamente, 
las listas origen, destino y símbolo"""
def creaThompson(comienzo, lista):
    #Variables
    origen = list()
    destino = list()
    simbolo = list()
    global oper, noEjecutar, expresion
    cadenaLista = listaToString(lista)
    operandos = list()
    contEstados = comienzo
    estadoRef = comienzo
    salir = False

    basica(estadoRef, cadenaLista, origen, destino, simbolo)

    while not salir:
        for m in range(0, len(simbolo)):
            if simbolo[m] != "lambda":
                revision = list(simbolo[m])
                for n in range(0, len(revision)):
                    if revision[n] in listaOperadores:
                        expresion = simbolo[m]
                        estadoRef = origen[m]

                        aux = list()
                        aux.append(expresion)
                        operandos.append(aux)

                        for i in range(0, len(listaOperadores)):
                            for j in range(0, len(operandos)):
                                noEjecutar = False
                                opMayor = listaOperadores[i]
                                oper = getOperandos(operandos[j], opMayor)
                                if oper == False:
                                    noEjecutar = True
                                    break
                                aux = operandos
                                operandos = list()
                                oper = oper.split(sep=" lista ")

                                for k in range(0, len(oper)):
                                    operandos.append(oper[k].split(sep=","))

                            if not noEjecutar:
                                for l in range(0, len(aux)):
                                    aux = aux[l]
                                    for j in range(0, len(operandos)):
                                        comparar = aux[j]

                                        for k in range(0, len(origen)):
                                            if simbolo[k] == comparar:
                                                estadoRef = origen[k]
                                                del origen[k]
                                                del destino[k]
                                                del simbolo[k]
                                                break

                                        if i == 0:
                                            if tieneOperador(comparar, "|"):
                                                sumaEstados = (len(operandos[j])) * 2 + 1
                                                sumaEstRef(estadoRef, sumaEstados, origen, destino)
                                                union(estadoRef, operandos[j], origen, destino, simbolo)
                                                contEstados = contEstados + sumaEstados
                                        elif i == 1:
                                            if tieneOperador(comparar, "."):
                                                sumaEstados = len(operandos[j]) - 1
                                                sumaEstRef(estadoRef, sumaEstados, origen, destino)
                                                concatenacion(estadoRef, operandos[j], origen, destino, simbolo)
                                                contEstados = contEstados + sumaEstados
                                        elif i == 2:
                                            if tieneOperador(comparar, "*"):
                                                sumaEstados = 2
                                                sumaEstRef(estadoRef, sumaEstados, origen, destino)
                                                superiAsterisco(estadoRef, operandos[j], origen, destino, simbolo)
                                                contEstados = contEstados + sumaEstados
                                        elif i == 3:
                                            if tieneOperador(comparar, "+"):
                                                sumaEstados = 2
                                                sumaEstRef(estadoRef, sumaEstados, origen, destino)
                                                superiMas(estadoRef, operandos[j], origen, destino, simbolo)
                                                contEstados = contEstados + sumaEstados

                        operandos.clear()
                        break

        cont = 0
        for m in range(0, len(simbolo)):
            incrementar = True
            if simbolo[m] != "lambda":
                revision = list(simbolo[m])
                for n in range(0, len(revision)):
                    if revision[n] in listaOperadores:
                        salir = False
                        incrementar = False
                        break
                if incrementar:
                    cont = cont + 1
            else:
                cont = cont + 1

        if cont == len(simbolo):
            salir = True

    contEstados = contEstados + 1
    lista = list()
    lista.append(contEstados)
    lista.append(origen)
    lista.append(destino)
    lista.append(simbolo)

    return lista


"""Obtiene los cierres lambda de una construcción de Thompson, recibe una lista de transiciones, un contador de estados, 
y las listas origen, destino y simbolo, retorna una lista con los cierres"""
def cierreLambda(transicion, contEstados, origen, destino, simbolo):
    #Variables
    cierres = list()
    lista = list()
    cont = contEstados - 1

    for i in range(0, contEstados):
        cierres.append(list())

    for i in range(0, contEstados):
        for j in range(0, len(origen)):
            if origen[j] == i:
                if simbolo[j] == transicion:
                    cierres[i].append(destino[j])

    while cont > 0:
        aux = cierres[cont]
        for i in range(0, len(aux)):
            if aux[i] != cont:
                lista.append(aux[i])

        for i in range(0, len(cierres)):
            if cont in cierres[i]:
                for j in range(0, len(lista)):
                    if i != cont:
                        if lista[j] != i:
                            cierres[i].append(lista[j])

        cont = cont - 1
        lista.clear()

    lista = list()
    lista.append(contEstados)
    cierres.append(lista)

    return cierres


"""Toma como parámetros las listas origen, destino y símbolo, además de la lista de cierres lambda, lo que hace es hallar 
los estados del autómata, verificando las transiciones existentes en la construcción de Thompson para cada símbolo de entrada.
Retorna una lista cuya posición 0 corresponde a los estados de partida, en la posición 1 transición que son los estados 
de llegada y en la posición 2 entrada que es el símbolo de las transiciones entre estados y transición"""
def hallaEstados(origen, destino, simbolo, cierres):
    #Variables
    global cierreActual
    cont = 1
    pila = deque()
    pila.append(cierres[cont])
    sim = getSim(listaER)
    estado = list()
    entrada = list()
    transicion = list()
    aux = list()
    seguir = True
    huboCambio = False

    while seguir:
        salir = False
        while not salir:
            if len(pila) != 0:
                cierreActual = pila.pop()
                if cont == 1 or (cierreActual not in estado):
                    salir = True
            else:
                seguir = False
                salir = True

        if cierreActual in estado:
            break
        for elemento in sim:
            for i in range(0, len(cierreActual)):
                posicion = cierreActual[i]
                cierreAux = cierres[posicion]
                for l in range(0, len(cierreAux)):
                    for k in range(0, len(origen)):
                        if origen[k] == cierreAux[l]:
                            if simbolo[k] == elemento:
                                if destino[k] not in aux:
                                    aux.append(destino[k])
                                    huboCambio = True
            if huboCambio:
                estado.append(cierreActual)
                entrada.append(elemento)
                transicion.append(aux)
                pila.append(aux)
            huboCambio = False
            cont = 0
            aux = list()

    lista = list()
    lista.append(estado)
    lista.append(entrada)
    lista.append(transicion)
    return lista


"""Toma el estado final, la lista de cierres lambda y la lista que retorna la función hallaEstados, lo que hace es 
crear el autómata a partir de dichos parámetros, retorna una matriz en la cual está representado el autómata"""
def AFND(estadoFinal, cierresLambda, lista):
    #Variables
    estadoTemp = lista[0]
    estado = list()
    estadosTemp = list()
    estados = list()
    entrada = lista[1]
    tranTemp = lista[2]
    transicion = list()
    simbolos = getSim(listaER)

    #Identificación de los estados
    estadosTemp.append(estadoTemp[0])
    for i in range(0, len(tranTemp)):
        if tranTemp[i] not in estadosTemp:
            estadosTemp.append(tranTemp[i])

    # Llenamos estado, estados y transicion de 0
    for i in range(0, len(estadosTemp)):
        estados.append(0)

    for i in range(0, len(estadoTemp)):
        estado.append(0)

    for i in range(0, len(tranTemp)):
        transicion.append(0)

    """"#Identificación de las transiciones
    for i in range(0, len(tranTemp)):
        if tranTemp[i] not in transicion:
            transicion.append(tranTemp[i])"""

    #Creación de la matriz
    filas = len(estados) + 1
    columnas = len(simbolos) + 2
    matriz = creaMatriz(filas, columnas)

    #Se renombran los estados
    for i in range(0, len(estadosTemp)):
        for j in range(0, len(tranTemp)):
            if estadosTemp[i] == tranTemp[j]:
                transicion[j] = i
        for j in range(0, len(estadoTemp)):
            if estadosTemp[i] == estadoTemp[j]:
                estado[j] = i
        estados[i] = i

    #Ingresamos los estados en la columna 0 de la matriz
    for i in range(1, filas):
        fila = matriz[i]
        fila[0] = estados[i - 1]

    #Ingresamos los símbolos de entrada en la fila 0 de la matriz
    for j in range(1, columnas - 1):
        fila = matriz[0]
        fila[j] = simbolos.pop()

    # Asignación de los estados de aceptación
    for j in range(1, len(matriz)):
        fila = matriz[j]
        aceptacion = False
        actual = fila[0]
        tran = estadosTemp[actual]
        for k in range(0, len(tran)):
            cierre = cierresLambda[tran[k]]
            if estadoFinal in cierre:
                aceptacion = True
                fila[columnas - 1] = 1
                break
        if not aceptacion:
            fila[columnas - 1] = 0

    #Se añaden las transiciones correspondientes a la matriz
    encabezado = matriz[0]
    for i in range(1, len(matriz)):
        fila = matriz[i]
        for j in range(0, len(estadoTemp)):
            if fila[0] == estado[j]:
                for k in range(1, len(encabezado) - 1):
                    if encabezado[k] == entrada[j]:
                        fila[k] = transicion[j]

    return matriz


"""Función que recibe como parámetro un autómata representado en una matriz y elimina sus estados extraños
(estados a los cuales nunca se llega), retorna el autómata sin los estados extraños"""
def eliminaExtra(automata):
    #Variables
    fila = automata[1]
    actual = fila[0]
    pila = deque()
    alcanzados = set()
    alcanzados.add(actual)

    for i in range(1, len(fila) - 1):
        if fila[i] != "":
            pila.append(fila[i])

    while len(pila) != 0:
        actual = pila.pop()
        if actual not in alcanzados:
            alcanzados.add(actual)
            for i in range(1, len(automata)):
                fila = automata[i]
                if fila[0] == actual:
                    for j in range(1, len(fila) - 1):
                        if fila[j] != "":
                            pila.append(fila[j])

    i = 1
    long = len(automata)
    while i < long:
        fila = automata[i]
        if fila[0] not in alcanzados:
            automata.remove(fila)
            i = 0
            long = len(automata)
        i = i + 1

    return automata


"""Función que recibe como parámetro un autómata representado como matriz y unifica los estados equivalentes,
a su vez los renombre y devuelve el autómata modificado en forma de matriz"""
def equivalentes(automata):
    #Variables
    particiones = list()
    particiones.append(list())
    particiones.append(list())
    simbolos = getSim(listaER)
    dest = list()

    for i in range(1, len(automata)):
        fila = automata[i]
        if fila[len(fila) - 1] == 0:
            particiones[0].append(fila[0])
        elif fila[len(fila) - 1] == 1:
            particiones[1].append(fila[0])

    i = 0
    long = len(particiones)
    while i < long:
        pActual = particiones[i]
        if len(pActual) != 1:
            huboCambios = False
            for j in range(1, len(simbolos)):
                for k in range(0, len(pActual)):
                    eActual = pActual[k]
                    for l in range(1, len(automata)):
                        fila = automata[l]
                        if fila[0] == eActual:
                            dest.append(fila[j])
                for k in range(0, len(dest)):
                    for l in range(0, len(particiones)):
                        part = particiones[l]
                        if dest[k] in part:
                            dest[k] = l
                            break
                todosIguales = False
                while not todosIguales:
                    if len(dest) == 1:
                        todosIguales = True
                    else:
                        comparar = dest[0]
                        cont = 0
                        for k in range(1, len(dest)):
                            if dest[k] == comparar:
                                cont = cont + 1
                        if cont == len(dest) - 1:
                            todosIguales = True
                        if not todosIguales:
                            k = 0
                            lon = len(dest)
                            while k < lon:
                                reinicio = False
                                if dest[k] != comparar:
                                    reinicio = True
                                    trasladar = dest[k]
                                    lista = list()
                                    lista.append(pActual.pop(k))
                                    dest.pop(k)
                                    l = 0
                                    longi = len(dest)
                                    while l < longi:
                                        deNuevo = False
                                        if dest[l] == trasladar:
                                            deNuevo = True
                                            lista.append(pActual.pop(l))
                                            dest.pop(l)
                                        if deNuevo:
                                            l = 0
                                            longi = len(dest)
                                        else:
                                            l = l + 1
                                    particiones.append(lista)
                                    lista = list()
                                if reinicio:
                                    k = 0
                                    lon = len(dest)
                                else:
                                    k = k + 1
                            huboCambios = True
                dest = list()
                if huboCambios:
                    break
            if huboCambios:
                i = 0
                long = len(particiones)
            else:
                i = i + 1
                long = len(particiones)

        else:
            i = i + 1
            long = len(particiones)

    lista = list()
    for i in range(0, len(particiones)):
        particion = particiones[i]
        if len(particion) != 1:
            lista.append(list())

    i = 1
    long = len(automata)
    for l in range(0, len(lista)):
        sublista = lista[l]
        while i < long:
            fila = automata[i]
            for j in range(0, len(particiones)):
                particion = particiones[j]
                if len(particion) != 1:
                    if fila[0] in particion:
                        sublista.append(fila)
            i = i + 1
            long = len(automata)

    for i in range(0, len(lista)):
        sublista = lista[i]
        for j in range(0, len(sublista)):
            actual = sublista[j]
            automata.remove(actual)

    cadenaEstado = ""
    cadenaAceptacion = 0
    listaTransiciones = list()
    renombrar = list()
    for i in range(0, len(simbolos)):
        listaTransiciones.append("")

    for i in range(0, len(lista)):
        sublista = lista[i]
        for j in range(0, len(sublista)):
            actual = sublista[j]
            cadenaEstado = cadenaEstado + str(actual[0])
            cadenaAceptacion = cadenaAceptacion + actual[len(actual) - 1]
            for k in range(1, len(actual) - 1):
                if listaTransiciones[k - 1] != "":
                    if int(listaTransiciones[k - 1]) != actual[k]:
                        listaTransiciones[k - 1] = listaTransiciones[k - 1] + str(actual[k])
                else:
                    listaTransiciones[k - 1] = listaTransiciones[k - 1] + str(actual[k])

        nuevoEstado = list()
        nuevoEstado.append(cadenaEstado)
        renombrar.append(cadenaEstado)
        for j in range(0, len(listaTransiciones)):
            nuevoEstado.append(int(listaTransiciones[j]))
        if cadenaAceptacion > 0:
            nuevoEstado.append(1)
        else:
            nuevoEstado.append(0)
        automata.append(nuevoEstado)

    filas = len(automata)
    columnas = len(simbolos) + 2
    fila = automata[0]

    modificado = creaMatriz(filas, columnas)

    for i in range(1, len(automata)):
        fila = automata[i]
        cambiar = fila[0]
        if cambiar in renombrar:
            for m in range(0, len(renombrar)):
                if cambiar == renombrar[m]:
                    aux = list(renombrar[m])
                    for k in range(0, len(automata)):
                        filaTemp = automata[k]
                        filaMod = modificado[k]
                        for l in range(1, len(filaTemp) - 1):
                            enTemp = str(filaTemp[l])
                            for m in range(0, len(enTemp)):
                                if enTemp[m] in aux:
                                    if filaMod[l] != True:
                                        filaTemp[l] = i
                                        filaMod[l] = True
                                        break
        else:
            for k in range(1, len(automata)):
                filaTemp = automata[k]
                filaMod = modificado[k]
                for l in range(0, len(filaTemp) - 1):
                    if filaTemp[l] == cambiar:
                        if filaMod[l] != True:
                            filaTemp[l] = i
                            filaMod[l] = True
        fila[0] = i

    return automata

"""Función que toma la lista de la ER y crea una lista de sublistas, donde cada sublista es un () de la ER"""
def divideER(listaER):
    #Variables
    tam = cuentaParentesis(listaER) + 1
    listaGeneral = list()
    simbolos = getSim(listaER)

    # Se crea la lista de sublistas
    for i in range(0, tam):
        listaGeneral.append(list())

    # Se analiza la ER y se divide en las sublistas
    # i va recorriendo la ER
    # j se mueve en la lista general
    # k se mueve en cada sublista
    i = 0
    j = 0
    contAbrePar = 0
    contCierraPar = 0
    listaEstYOp = set.union(simbolos, listaOperadores)

    for k in range(0, len(listaER)):
        if listaER[i] in listaEstYOp:
            # En la posicion actual de a sublista en la que estamos, vamos a escribir el simbolo u operador que estamos analizando de la listaER
            listaGeneral[j].append(listaER[i])
            # Avanzamos en listaER
            i = i + 1
        elif listaER[i] == "(":
            contAbrePar = contAbrePar + 1
            # En la posición actual de la sublista en la que estamos, vamos a tener un apuntador a la sublista correspondiente al () que estamos leyendo de listaER
            listaGeneral[j].append("L" + str(contAbrePar))
            # Nos movemos a la sublista corresondiente al () a analizar
            j = contAbrePar
            k = 0
            # Avanzamos en la listaER
            i = i + 1
        elif listaER[i] == ")":
            contCierraPar = contCierraPar + 1
            # Retrocedemos a la sublista correspondiente para seguir analizando la ER
            j = contAbrePar - contCierraPar
            k = 0
            # Avanzamos en la listaER
            i = i + 1

    return listaGeneral


"""NOTA: Hasta este punto, el programa funciona para ER simples (que no se componen de paréntesis los cuales
contienen más ER simples)"""

"""Función que toma una expresión regular cualquiera y utiliza los métodos necesarios para realizar todo el proceso
de convertirla en un autómata finito determinístico, retornando este último como una matriz"""
def ERaAFD(lista):
    #Variables
    comienzo = 1
    origen = list()
    destino = list()
    simbolo = list()

    #Se crea la construccion de Thompson para la ER
    if cuentaParentesis(lista) != 0:
        listaDiv = divideER(lista)
        sublista = listaDiv[0]
        thompson = creaThompson(comienzo, sublista)
        contEstados = thompson[0]
        origen = thompson[1]
        destino = thompson[2]
        simbolo = thompson[3]
        i = 0
        long = len(simbolo)

        while i < long:
            huboCambio = False
            if len(simbolo[i]) > 1 and simbolo[i] != "lambda":
                aux = simbolo.pop(i)
                apuntador = ""
                for j in range(1, len(aux)):
                    apuntador = apuntador + aux[j]
                apuntador = int(apuntador)
                comienzo = origen.pop(i)
                final = destino.pop(i)
                thompson = creaThompson(comienzo, listaDiv[apuntador])
                contDespues = thompson[0]
                suma = contDespues - comienzo - 1
                sumaEstRef(comienzo, suma, origen, destino)
                origen.append(thompson[0])
                destino.append(final + suma)
                simbolo.append("lambda")
                origTemp = thompson[1]
                destTemp = thompson[2]
                simboTemp = thompson[3]
                for j in range(0, len(origTemp)):
                    origen.append(origTemp[j])
                for j in range(0, len(origTemp)):
                    destino.append(destTemp[j])
                for j in range(0, len(origTemp)):
                    simbolo.append(simboTemp[j])
                contEstados = contEstados + suma
                i = 0
                long = len(simbolo)
                huboCambio = True
            if not huboCambio:
                i = i + 1
                long = len(simbolo)
    else:
        thompson = creaThompson(comienzo, lista)
        contEstados = thompson[0]
        origen = thompson[1]
        destino = thompson[2]
        simbolo = thompson[3]

    #Verificamos que no haya transiciones repetidas, si las hay se eliminan
    i = 0
    long = len(origen)
    while i < long:
        cambio = False
        for j in range(0, len(origen)):
            if i != j:
                if origen[i] == origen[j] and destino[i] == destino[j] and simbolo[i] == simbolo[j]:
                    cambio = True
                    origen.pop(i)
                    destino.pop(i)
                    simbolo.pop(i)
            if cambio:
                i = 0
                long = len(origen)
                break
        i = i + 1

    #Se obtienen los cierres lambda
    cierresL = cierreLambda("lambda", contEstados, origen, destino, simbolo)

    #Se obtienen los estados
    estados = hallaEstados(origen, destino, simbolo, cierresL)

    #Se crea el autómata finito no determinístico para la ER
    automata = AFND(contEstados, cierresL, estados)

    #Se eliminan los estados extraños
    sinExtra = eliminaExtra(automata)

    #Se unifican estados equivalentes haciendo mínimo y determinístico el autómata
    afd = equivalentes(automata)

    return afd

if revCompleta(listaER):
    construccion = ERaAFD(listaER)
    print("Atómata finito determinístico correspondiente a la expresión regular ingresada:")
    for i in range(0, len(construccion)):
        print(construccion[i])