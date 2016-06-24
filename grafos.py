import copy


# Un grafo se define con una lista de adyacencia G =[a0,a1,...]
#  1) los vertices son 0,1,...,len(G)-1
#  2) ai lista de vertices adyacentes a i.
#  3) j in ai sii i in aj
#  4) ai no tiene elementos repetidos (0 <= i <= len(G)-1).

# OPERACIONES ELEMENTALES SOBRE GRAFOS
# valencia de un vertice, vertices adyacentes, agregar arista, quitar arista

def grafo(graph):
    # pre: graph es un lista. La coordenada i es una lista de enteros j, con 0 <= j < len(graph) tq ij arista
    # post: devuelve una lista de adyacencia (que cumple 2), 3) y 4) de arriba)
    for i in range(len(graph)):
        # print graph[i]
        j = 0
        while j < len(graph[i]):
            k = graph[i][j]
            if i not in graph[k]:
                graph[k].append(i)
            if graph[i][j] == i or graph[i][j] >= len(graph):
                del graph[i][j]
            else:
                j += 1
    for i in range(len(graph)):
        graph[i].sort()
        j = 1
        while j < len(graph[i]):
            if graph[i][j] == graph[i][j - 1]:
                del graph[i][j]
                pass
            else:
                j += 1
        graph[i].sort()
    return graph


def valencia(graph):
    # pre: graph es un grafo
    # post: devuelve la lista de valencias. La valencia(graph)[i] = valencia del vertice i
    graph = grafo(graph)  # por las dudas chequea el grafo
    val = []
    for i in range(len(graph)):
        val.append(len(graph[i]))
    return val


def aristas(graph):
    # pre: graph es un  grafo
    # post:  devuelve una lista de aristas, una copia del mismo grafo
    hgraph = copy.deepcopy(graph)
    return hgraph


def vertices(graph):
    # pre: graph es un grafo
    # post:  devuelve una lista de vertices de graph
    verts = []
    for i in range(len(graph)):
        verts.append(i)
    return verts


def adyacentes(vert, graph):
    # pre: graph graph, vert vertice
    # post: devuelve los vertices adyacentes a vert
    hgraph = aristas(graph)
    return hgraph[vert]


def quitar_arista(graph, i, j):
    # pre: graph grafo, i, j vertices
    # post: devuelve el grafo sin la arista ij (si existe)
    # mod: no modifica graph, devuelve otro grafo
    k = 0
    hgraph = aristas(graph)
    while k < len(hgraph[i]):
        if hgraph[i][k] == j:
            del hgraph[i][k]
        k += 1
    k = 0
    while k < len(hgraph[j]):
        if hgraph[j][k] == i:
            del hgraph[j][k]
        k += 1
    return hgraph


def agregar_arista(graph, i, j):
    # pre: graph grafo, i, j vertices
    # post: agrega la arista ij (si no existe)
    h = aristas(graph)
    if j not in h[i]:
        h[i].append(j)
        h[j].append(i)
    return h


# ALGORITMOS SOBRE GRAFOS


def caminata_euleriana_from(graph, v):
    # pre: graph grafo que 1) todas los son pares o 2) solo hay 2 vertices impares
    #      v es un vertice tal que en 1) es arbitrario, en 2) es uno de los vertices de valencia impar.
    # post: devuelve  la lista de vertices de la caminata euleriana
    #       La caminata empieza en v.
    recorrido = [v]
    libres = aristas(graph)  # en cada vertice nos dira que arista no hemos usado
    usados = []
    for i in range(len(graph)):
        usados.append([])
    pos = v
    while len(libres[pos]) > 0:
        prox = libres[pos][0]
        # print pos, libres[pos], prox
        recorrido.append(prox)
        libres = quitar_arista(libres, pos, prox)
        usados = agregar_arista(usados, pos, prox)
        # print 'lib:', libres
        # print 'usa:', usados
        pos = prox
    return recorrido


def caminata_euleriana(graph):
    # pre: graph grafo.
    # post: devuelve un par. La primera coordenada es True si hay camina euleriana y False en otro caso.
    #       La segunda coordenada es vacia si no hay c e y es la lista de vertices de la caminata si existe  c e
    #       La caminata empieza desde un vertice arbitrario (0 en el caso to_do par).
    val = valencia(graph)
    extremos = []
    for i in range(len(val)):
        if val[i] % 2 == 1:
            extremos.append(i)
    if len(extremos) == 0 or len(extremos) == 2:
        vini, vfin = 0, 0
        if len(extremos) == 2:
            vini, vfin = extremos[0], extremos[1]
        recorrido = caminata_euleriana_from(graph, vini)
        return True, recorrido
    else:
        return False, []


def coloracion_vertices(graph):
    # pre: graph grafo
    # post: devuelve la cantidad de colores usados  y  una lista de i:c donde i es vertice y
    #       c es color (c in N); de tal forma que si i:c,  k:c' y ij arista, entonces c != c'.
    color = []  # si  j < len(color), color[j] = c dice que el color de j es c.
    # si j <= len(color), todavia no esta asignado el color a j
    colores = 0  # cantidad de colores utilizados
    for i in range(len(graph)):
        s = []  # conjunto de colores asignados a los vertices j (1 <= j < i) que son
        # adyacentes a vi (comienza vacio)
        for j in range(i):  # recorre todos los vertices j < i
            if j in graph[i]:  # si j es adyacente a i
                if color[j] not in s:
                    s.append(color[j])  # agrega el color de j a s (si no estaba)
        k = 0
        while k in s:
            k += 1
        color.append(k)  # k es el primer color que no esta en s. Asigna el color k a i
        if k + 1 > colores:
            colores += 1

    return colores, color


G = [[2, 4, 5], [3, 5], [3, 4, 5], [1, 2, 4], [0, 2, 3, 5], [0, 1, 4]]
G = grafo(G)
print G

print caminata_euleriana(G)
print coloracion_vertices(G)


# def caminata_euleriana(G, v):
#     return True


# Algoritmo de Prim
# si G es un grafo una funcion de peso de las aristas es un lista de listas w tal que
# w[i][j] = peso de la arista de i a j (real >= 0), para 0 <= i, j <= n -1.
# Si ij arista, w[i][j] = w[j[i] > 0. Si ij no es arista w[i][j] = w[j][i] = 0.

def peso_max(w):
    # pre: w es una lista de pesos de las aristas de un grafo
    # post: devuelve el peso maximo
    resultado = 0
    for i in range(w):
        for j in  range(w[i]):
            resultado = max(resultado,w[i][j])
    return resultado

def peso_std(graph):
    # pre: graph es un grafo
    # post: devuelve w, funcion de peso, tal que a cada arista le asigna peso 1
    n = len(graph)
    w = []
    for i in range(n):
        w.append([])
        for i in range(n):
            w[i].append(0)
        for j in range(n):
            for j in range(n):
                if j in graph[i]:
                    w[i]



def prim(graph, w):
    #  pre: graph grafo con vertices 1,...,n y pesos w[i][j]. n >= 1.
    # (w[i][j] = infinito si ij no es arista de G)
    # post: devuelve tree un MST de graph
    n = len(graph)
    S = [0]  # lista de vertices utilizados en el MST (comienza con el primero)
    Q = range(1, n)  # lista de vertices aun no utilizados en el MST
    L = []
    for i in Q:
        L.append([i, 1, w(i, 1)])
    F = []
    for i in range(len(graph)):
        F.append([])
    # F  grafo con vertices 0,...,n-1 y sin aristas.
    while Q != []:
        uk = L[0][0]
        vk = L[0][1]
        pk = L[0][2]
        for u in L:
            if u[2] < pk:
                uk = u[0]
                vk = u[1]
                pk = u[2]
        # uk = vertice en Q tal que pk = w(uk,vk) es minimo
        F = agregar_arista(F, uk, vk)
        S.append(uk)
        Q.remove(uk)
        L.remove([uk, vk, pk])
        for i in range(len(L)):
            if w(L[i][0], uk) < L[i][2]:
                L[i][1] = uk
                L[i][2] = w(L[i][0], uk)
            # el for modifica L
    return F
