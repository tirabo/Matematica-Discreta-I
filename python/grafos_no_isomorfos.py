import json
from itertools import chain, combinations, permutations
import math

# Aqui un grafo será un n = vertices de  0 a n-1 y un conjunto de aristas frozenset({a,b})

def dos_subconjuntos(n: int): 
    # devuelve la lista de 2-subconjuntos del conjunto {0,...,n-1}. Los devuelve como frozenset. 
    dos_tuplas = []
    for i in range(n):
        for j in range(i+1, n):
            dos_tuplas.append(frozenset({i,j}))
    return dos_tuplas


def powerset2(s):
    # https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    # Devuelve un iterable con los subconjuntos (es un iterable que se usa una sola vez,  generator en Python)
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]
    

def powerset(s):
    # https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
    # devuelve la lista de subconjuntos de s,  donde s es uin iterable con elementos inmutables 
    x = len(s)
    pow_set = []
    for i in range(1 << x):
        pow_set.append({s[j] for j in range(x) if (i & (1 << j))})
    return pow_set

# dos_sc = dos_subconjuntos(3)
# print(powerset(dos_sc))
# exit(0)


def lista_de_valencias(n, grafo):
    # n entero,  grafo es un grafo con n vértices
    # post: lista de valencias en orden ascendente 
    val = [0] * n
    for edge in grafo:
        for vertice in edge:
            val[vertice] += 1
    val.sort()
    return tuple(val)

def conectados_a_vertices(n, grafo, vertices):
    # devuelve los vértices conectados a vértices. Esta función se basa en que por la implementación las aristas está ordenadas. 
    for edge in grafo:
        edge_l = list(edge)
        if edge_l[0] in vertices:
            vertices.append(edge_l[1])
        if edge_l[1] in vertices:
            vertices.append(edge_l[0])
    return list(set(vertices))

def es_conexo(n, grafo):
    return len(conectados_a_vertices(n, grafo, [0])) == n
    
def permutaciones(n):
    # devuelve lista de listas de permutaciones de 0, ..., n-1. Cada permutación es una n-upla de números diferentes
    # usa la función permutations de itertools
    lst = [x for  x  in range(n) ]
    return list(permutations(lst))

def func_perm(permutacion):
    # devuelve una función fp tal que fp(i) = permutacion[i]
    def fp(x):
        return permutacion[x]
    return fp

def perm_grafo(permutacion, grafo):
    def perm_edge(permutacion, edge):
        # devuelve el edge  con los vértices permutados según permutación
        result = []
        for x in edge:
            result.append(permutacion[x])
        return  frozenset(result)
    return {perm_edge(permutacion, edge) for edge in grafo}


def grafos_conexos(n_vert):
    # Grafos conexos de n_vert vértices 
    dos_sc = dos_subconjuntos(n_vert)
    
    grafos_n = powerset(dos_sc) # lista de todos los grafos de n_vert vertices
    print('Grafos posibles:', len(grafos_n))

    dic_val = {} # diccionario tal dic_val[(1,1,2,2,4,4)] = lista de todos los grafos conexos con esas valencias
    for grafo in grafos_n:
        if es_conexo(n_vert, grafo):
            lista_val = lista_de_valencias(n_vert, grafo)
            if lista_val not in dic_val.keys():
                dic_val[lista_val] = [grafo]
            else:
                dic_val[lista_val].append(grafo)

    print('Listas de valencias posibles para '+str(n_vert)+'-grafos conexos:', len(dic_val))
    
    i = 0
    pm_n, factorial_n = permutaciones(n_vert), len(permutaciones(n_vert))
    no_iso = []
    for lista_val in dic_val:
        print(i, len(dic_val[lista_val]),  lista_val)
        n1  = len(dic_val[lista_val])
        while n1 > 0:
            grafo = dic_val[lista_val][0]
            no_iso.append(grafo)
            kp = 0
            while kp < factorial_n and len(dic_val[lista_val]) > 0:
                grafo_permutado = perm_grafo(pm_n[kp], grafo)
                if grafo_permutado in dic_val[lista_val]:
                    dic_val[lista_val].remove(grafo_permutado)
                kp = kp + 1 
            n1 = len(dic_val[lista_val])
        i = i + 1 
        if i > 1:
            pass
            # break
    print('Cantidad de '+str(n_vert)+'-grafos conexos no isomorfos:', len(no_iso))
    return no_iso


def guardar_lista_grafos(lista_grafos, nombre):
    with open('./2021/python/'+nombre+'.json', 'w') as file:
        grafos_no_iso_json = []
        for grafo in lista_grafos:
            l_grafo = []
            for edge in grafo:
                l_grafo.append(tuple(edge))
            grafos_no_iso_json.append(l_grafo)
        file.write(json.dumps(grafos_no_iso_json))

def importar_lista_grafos(nombre):
    # nombre es un .json don de hay una lista de grafos.
    # Cada grafo es una lista de aristas
    # cada arista es una lista de de dos enteros
    #  Devuelve la lista de grafos (lista de conjuntos de frozensets)
    with open(nombre, 'r') as file:
        file_json = json.loads(file.read())
    lista_grafos = []
    for grafo  in file_json:
        grafo_set = set()
        for edge in grafo:
            grafo_set.add(frozenset(edge))
        lista_grafos.append(grafo_set)
    lista_grafos.sort()
    return lista_grafos

def str_grafo(grafo):
    # reemplaza arista frozenset por 2-tuple (sirve para imprimir)
    ret = set()
    for  edge in grafo:
        ret.add(tuple(edge))
    return ret


def main():
    # grafos_no_iso = grafos_conexos(4)
    # grafos, n_vert = importar_lista_grafos('./2021/python/grafos-5.json'), 5
    # grafos, n_vert = importar_lista_grafos('./2021/python/grafos-6.json'), 6
    grafos, n_vert = importar_lista_grafos('./2021/python/grafos-7.json'), 7
    


    val_gr = []
    for grafo in grafos:
        val_gr.append([lista_de_valencias(n_vert, grafo), grafo])
    val_gr.sort()

    for w in val_gr:
        print(w[0], str_grafo(w[1]))


    





if __name__ == '__main__':
    main()
