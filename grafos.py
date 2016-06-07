import copy

# Un grafo se define con una lista de adyacencia G =[a0,a1,...]
#  1) los vertices son 0,1,...,len(G)-1
#  2) ai non los vertices adyacentes a i. ai es una lista ordenada de vertices != i.
#  3) j in ai sii i in aj
#  4) cada ai no tiene elementos repetidos


def grafo(graph):
    # pre: graph es un lista. Cada componente es una lista de enteros j, con 0 <= j < len(graph)
    # post: devuelve una lista de adyacencia (cumple 2), 3) y 4) de arriba)
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
            if graph[i][j] == graph[i][j-1]:
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
    # pre: graph grafo
    # post:  devuelve una lista de aristas, una copia del mismo grafo
    graph = grafo(graph)
    hgraph = copy.deepcopy(graph)
    return hgraph


def vertices(graph):
    # pre: graph grafo
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
    h[i].append(j)
    h[j].append(i)
    return h


def caminata_euleriana_from(graph, v):
    # pre: graph grafo que 1) todas los son pares o 2) solo hay 2 vertices impares
    #      v es un vertice tal que en 1) es arbitrario, en 2) es uno de los vertices de valencia impar.
    # post: devuelve  la lista de vertices de la caminata euleriana
    #       La caminata empieza desde v.
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
