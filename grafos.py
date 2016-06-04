

# Un grafo se define con una lista de adyacencia G =[a0,a1,...]
#  1) los vertices son 0,1,...,len(G)-1
#  2) ai non los vertices adyacentes a i. ai es una lista ordenada de vertices != i.
#  3) j in ai sii i in aj
#  4) cada ai no tiene elementos repetidos

def grafo(G):
    # pre: G es un lista. Cada componente es una lista de enteros j, con 0 <= j < len(G)
    # post: devuelve una lista de adyacencia (cumple 2), 3) y 4) de arriba)
    for i in range(len(G)):
        #print G[i]
        j = 0
        while j  < len(G[i]):
            k = G[i][j]
            if i not in G[k]:
                G[k].append(i)
            if G[i][j] == i or G[i][j] >= len(G) :
                del G[i][j]
            else:
                j = j +1
    for i in range(len(G)):
        G[i].sort()
        j = 1
        while j < len(G[i]):
            if G[i][j] == G[i][j-1]:
                del G[i][j]
                pass
            else:
                j = j+1
    return G


def valencia(G):
    # pre: G es un grafo
    # post: devuelve la lista de valencias. La valencia(G)[i] = valencia del vertice i
    G = grafo(G)  # por las dudas chequea el grafo
    val = []
    for i in range(len(G)):
        val.append(len(G[i]))
    return val


def aristas(G):
    # pre: G grafo
    # post:  devuelve una lista de aristas [a,b]. Para simplificar tambien se pone [b,a]
    G = grafo(G)  # por las dudas chequea el grafo
    aristas = []
    for i in range(len(G)):
        aristas.append([i,G[i]])
    return aristas

def adyacentes(v, G):
    # pre: G grafo, v vertice
    # post: devuelve los vertices adyacentes a v
    return G[v]

def sacar_arista(G,i,j):
    # pre: G grafo, i, j vertices
    # post: elimina la arista ij (si existe)
    k = 0
    while k < len(G[i]):
        if G[i][k] == j:
            del G[i][k]
            break
        k += 1
    k = 0
    while k < len(G[j]):
        if G[j][k] == i:
            del G[j][k]
            break
        k += 1
    return G


def agregar_arista(G,i,j):
    # pre: G grafo, i, j vertices
    # post: agrega la arista ij (si no existe)
    G[i].append(j)
    G[j].append(i)
    G = grafo(G)
    return G



def caminata_euleriana(G):
    # pre: G grafo
    # post: devuelve un par. La primera coordenada es True si hay camina euleriana y False en otro caso.
    #       La segunda coordenada es vacia si no hay c e y es la lista de vertices de la caminata si existe  c e
    #       La caminata empieza desde un vertice arbitrorio.
    result = []
    val = valencia(G)
    caminata = True
    extremos = []
    for i in range(len(val)):
        if val[i] % 2 == 1:
            extremos.append(i)
    if len(extremos) == 0 or len(extremos) == 2:
        vini, vfin = 0, 0
        if len(extremos) == 2:
            vini, vfin = extremos[0], extremos[1]
        recorrido = [vini]
        libres = G # en cada vertice nos dira que arista no hemos usado
        usados = []
        for u in G:
            usados.append([])
        pos = extremos[0]
        while len(libres[pos]) > 0:
            prox = libres[pos][0]
            print pos, libres[pos], prox
            recorrido.append(prox)
            libres = sacar_arista(libres, pos, prox)
            usados = agregar_arista(usados, pos, prox)
            print libres
            print usados
            pos = prox
        return (True,recorrido)
    else:
        return (False,[])

G = [[2, 4, 5],[3, 5],[3, 4, 5],[1, 2, 4], [0, 2, 3, 5], [0, 1, 2, 4]]
G = grafo(G)
print G

print caminata_euleriana(G)

# def caminata_euleriana(G, v):
#     return True
