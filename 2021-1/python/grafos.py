import copy


# Un grafo se define con una lista de adyacencia G =[a0,a1,...] (los ai son listas)
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


def copiar_grafo(graph):
    # pre: graph es un  grafo
    # post:  devuelve una copia del grafo graph
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
    # pre: graph es un grafo, vert es un vertice de graph
    # post: devuelve los vertices adyacentes a vert
    hgraph = copiar_grafo(graph)
    return hgraph[vert]


def quitar_arista(lt, e):
    # pre: lt lista de adyacencia e= [x,y] arista
    # mod: modifica lt, quita arista [x,y] (si está)
    # post: -.
    lt[e[0]].remove(e[1]) 
    lt[e[1]].remove(e[0]) 


def agregar_arista(lt, e):
    # pre: lt lista de adyacencia e= [x,y] arista
    # mod: modifica lt, agrega arista [x,y] (si no está)
    # post: -.
    if e[1] not in lt[e[0]]:
        lt[e[0]].append(e[1]) 
        lt[e[1]].append(e[0]) 

def nro_aristas(G):
    # pre: G grafo
    # post: devuelve el  número de aristas de G
    k = 0
    for u in G:
        k = k + len(u)
    return k // 2    

# ALGORITMOS SOBRE GRAFOS


# Grafos de prueba

# Grafo 1 (el gran tour)
G = [[1,2,4,5],[0,2,4,5],[0,1,3,5],[2,4],[0,1,3,5],[0,1,2,4]]

# Grafo 2
# G = [[3,4,5,6], [2,4], [1,5], [0,4], [0,1,3,5], [0,2,4,6], [0,5]]

# Grafo 3 (cíclico)
# G = [[1,5],[0, 2],[1,3],[2,4],[3,5],[4,0]]

# Grafo 4 
# G = [[2, 4, 5], [3, 5], [3, 4, 5], [1, 2, 4], [0, 2, 3, 5], [0, 1, 4]]
# G = grafo(G)


## Inicio: Algoritmo de Hierholzer ##

def enclibr(lt, tc): # necesaria para circuitos eulerianos
    # pre: lt lista de adyacencia, tc = lista de vértices,  
    # post: devuelve j en tocados tq libres[j] no es vacío.  
    ret = -1
    for j in range(len(lt)):
        if len(lt[j]) > 0 and j in tc:
            ret = j
            break
    return ret

def inserta_circuito(cr, ct): # necesaria pa circuitos eulerianos
    # pre: cr, ct circuitos tq ct[0] en cr
    # mod: se modifica cr insertando ct en ct[0]
    # si cr = [...,c0,c1,c2,...] y ct = [c1,d,...,f,c1]
    # entonces se obtiene cr = [...,c0,c1,d,...,f,c1,c2,...] 
    j = cr.index(ct[0])
    k = j
    for t in range(len(ct)-1):
        cr.insert(k,ct[t])
        k = k + 1
        
def circuito_euleriano(G, v = 0): #Algoritmo de Hierholzer
    # pre: G grafo con todos los vértices de valencia par, v vértice.
    #      Si no se ingresa v toma el valor 0
    # post: devuelve 'circuito' una lista de vertices que forma un circuito
    #       euleriano. El  circuito empieza en 0.
    circuito = [v]  # inicio de la caminata
    libres = copiar_grafo(G) # aristas no utilizadas
    while  nro_aristas(libres) > 0:
        sub_cam = []   
        h = 0
        while libres[h] == [] or h not in circuito:
            h = h + 1
        # h = vértice en circuito donde libre[h] != [] (hay aristas libres)
        pos = circuito.index(h) # posición de la 1º ocurrencia de h
        p0 = h
        p1 = libres[h][0] 
        while p1 != h: # mientras no se vuelva al origen
            sub_cam.append(p1)  # agrega p1 a sub_cam 
            libres[p0].remove(p1)
            libres[p1].remove(p0) # quitar arista p0, p1 
            p0 = p1 
            p1 = libres[p0][0]
        libres[p0].remove(h)
        libres[h].remove(p0) # quitar arista p0, p1 
        # print( circuito[: pos +1], sub_cam, circuito[pos :]) 
        circuito = circuito[: pos + 1] +  sub_cam + circuito[pos :]
        # print('Circuito:',circuito) 
        # print('Libres;',libres)
    return circuito   

# print(circuito_euleriano(G,3))

    
def caminata_euleriana_desde_a(G, v, w): 
    # pre: graph grafo donde v y w son vértices impares y todos demás pares
    # post: devuelve  la lista de vertices de la caminata euleriana
    #       La caminata empieza en v y termmina en w.
    caminata = []
    H = copiar_grafo(G) # hace una copia de G
    if w in G[v]: # si [v,w] es arista en G
        quitar_arista(H, [v, w]) # quita la arista [v, w]
        cmnt = circuito_euleriano(H, v)
        caminata = cmnt.append(w)
    else: # si [v,w] no es arista en G
        agregar_arista(H, [v, w]) # agrega la arista [v, w]
        cmnt = circuito_euleriano(H, w)
        k = -1
        for i in range(1,len(cmnt)):
            if cmnt[i - 1] == w and cmnt[i] == v:
                k = i
            if k > 0:
                caminata.append(cmnt[i])
        for i in range(1,k):
            caminata.append(cmnt[i])
    return caminata

def caminata_euleriana(G): 
    # pre: G grafo.
    # post: devuelve un par. La primera coordenada es True si hay camina euleriana y False en otro caso.
    #       La segunda coordenada es [] si no hay c e y es la lista de vertices de la caminata si existe  c e
    #       La caminata empieza desde un vertice arbitrario (0 en el caso par).
    existe, caminata = False, []
    impares = []
    for i in range(len(G)):
        if len(G[i]) % 2 == 1: # si la valencia es impar
            impares.append(i)
    if len(impares) == 0: # todas las valencias pares
        existe = True
        caminata = circuito_euleriano(G)
    elif len(impares) == 2: # dos valencias impares
        existe = True
        vini, vfin = impares[0], impares[1]
        caminata = caminata_euleriana_desde_a(G, vini, vfin)
    return existe, caminata

# print(caminata_euleriana(G))

## FIN: Algoritmo de Hierholzer ##


## INICIO: algoritmo greedy para coloración de vértices

def coloracion_vertices(G):
    # pre: G grafo
    # post: devuelve la cantidad de colores usados  y  una lista de i:c donde i es vertice y
    #       c es color (c in N); de tal forma que si i:c,  k:c' y ij arista, entonces c != c'.
    color = []  # si  j < len(color), color[j] = c dice que el color de j es c.
    # si j <= len(color), todavia no esta asignado el color a j
    colores = 0  # cantidad de colores utilizados
    for i in range(len(G)):
        S = []  # conjunto de colores asignados a los vertices j (1 <= j < i) que son
        # adyacentes a vi (comienza vacio)
        for j in range(i):  # recorre todos los vertices j < i
            if j in graph[i]:  # si j es adyacente a i
                if color[j] not in S:
                    S.append(color[j])  # agrega el color de j a s (si no estaba)
        k = 0
        while k in S:
            k += 1
        color.append(k)  # k es el primer color que no esta en s. Asigna el color k a i
        if k + 1 > colores:
            colores += 1

    return colores, color

# print(coloracion_vertices(G))

## FIN: algoritmo greedy para coloración de vértices



## INICIO: Algoritmo de Prim ##

# Datos: G, w
# G es un grafo. 
# w es una funcion de peso de las aristas. Es un lista de listas, tal que
# w[i][j] = peso de la arista de i a j (real >= 0), para 0 <= i, j <= n - 1.
# Si ij arista, w[i][j] = w[j[i] > 0. Si ij no es arista w[i][j] = w[j][i] = 0.

def peso_max(w):
    # pre: w es una lista de pesos de las aristas de un grafo
    # post: devuelve el peso maximo
    resultado = 0
    for i in range(len(w)):
        for j in  range(len(w[i])):
            resultado = max(resultado,w[i][j])
    return resultado


def w_infty(w):
    # pre: w es una lista de pesos de las aristas de un grafo
    # post: devuelve w donde reemplaza el peso 0 por peso_max(w) +100 ('= infinito')
    u = copy.deepcopy(w)
    pinfty = peso_max(w) + 100
    for i in range(len(w)):
        for j in range(len(w[i])):
            if w[i][j] == 0:
                u[i][j] = pinfty
    return u


def peso_std(graph):
    # pre: graph es un grafo
    # post: devuelve w, funcion de peso, tal que a cada arista le asigna peso 1
    n = len(graph)
    w = []
    for i in range(n):
        w.append([])
        for j in range(n):
            w[i].append(0)
            if j in  graph[i]:
                w[i][j] = 1
    return w

def prim(graph, w):
    #  pre: graph grafo con vertices 0,...,n-1 y pesos w[i][j]. n >= 1.
    # (w[i][j] = infinito si ij no es arista de G)
    # post: devuelve un MST de graph
    n = len(graph)
    S = [0]  # lista de vertices utilizados en el MST (comienza con el primero)
    Q = []
    for i in range(1, n):
        Q.append(i)  
    # Q es la lista de vertices aun no utilizados en el MST
    # print(Q)
    L = []
    w = w_infty(w)
    for i in Q:
        L.append([i, 0, w[i][0]])
    # L = [[1, 0, p2], ..., [n-1, 0, p(n-1)]]]  con pi = w(i,0)
    # se ira modificando L de tal forma que si Q = [u0,...,ur],
    # L = [[u0,v0,p0],...,[ur,vr,pr]] donde  vi = vertice en S adyacente a ui tal que w(ui,vi) es minimo, pi = w(ui,vi)
    F = []
    for i in range(len(graph)):
        F.append([])
    # F  grafo con vertices 0,...,n-1 y sin aristas.
    wF = 0 # wF es la suma del peso de todas las aristas de F
    while Q != []:
        # print 'L :', L
        L.sort(key=lambda x: x[2]) # ordena L por pesos
        [uk,vk,pk] = L[0]
        # print uk,vk,pk
        # uk = vertice en Q tal que pk = w(uk,vk) es minimo
        agregar_arista(F, [uk, vk])
        wF = wF + w[uk][vk]
        S.append(uk)
        Q.remove(uk)
        L.remove([uk, vk, pk])
        for i in range(len(L)):
            if w[L[i][0]][uk] < L[i][2]:
                L[i][1] = uk
                L[i][2] = w[L[i][0]][uk]
            # el for modifica L
    return (F, wF)

# Pruebas 

G = [[1,2,3,4],[0,2,3,4],[0,1,3,4],[0,1,2,4],[0,1,2,3]]
G = grafo(G)
w = [[0, 6, 8, 6, 3],[6, 0, 2, 4, 5],[8, 2, 0, 5, 7],[6, 4, 5, 0, 7],[3, 5, 7, 7, 0]]

G = [[1, 2, 3], [0, 2, 4], [0, 1, 3, 4, 5, 6], [0, 2, 6], [1, 2, 5, 7, 8], [2, 4, 6, 8], [2, 3, 5, 8, 9],
     [4, 8, 10], [4, 5, 6, 7, 9, 10], [6, 8, 10], [7, 8, 9]]
G = grafo(G)
w = [[0, 2, 8, 1, 0, 0, 0, 0, 0, 0, 0], [2, 0, 6, 0, 1, 0, 0, 0, 0, 0, 0], [8, 6, 0, 7, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 7, 0, 0, 0, 9, 0, 0, 0, 0], [0, 1, 5, 0, 0, 3, 0, 2, 9, 0, 0], [0, 0, 1, 0, 3, 0, 4, 0, 6, 0, 0],
     [0, 0, 2, 9, 0, 4, 0, 0, 3, 1, 0], [0, 0, 0, 0, 2, 0, 0, 0, 7, 0, 9], [0, 0, 0, 0, 9, 6, 3, 7, 0, 1, 2],
     [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 4], [0, 0, 0, 0, 0, 0, 0, 9, 2, 4, 0]]

# (F, wF) = prim(G,w)
# print(F)
# print(wF)

## FIN: Algoritmo de Prim ##
