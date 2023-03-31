from itertools import product


"""
Se colocan 6 plantines en un cantero circular
1) Hay 4 clases de plantines (0, 1, 2, 3)
2) No puede haber 2 plantines consecutivos de la misma clase
¿De cuantas formas se puede hacer? (las rotaciones son equivalentes)
"""



def acomodar_plantines(cantero = 6, cls_plantines= 4):
    # cantero : cantidad de plantines en el cantero
    # cls_plantines : cantidad de clases de plantines
    cls = list(range(cls_plantines))
    cls_repetidos = [cls]*cantero
    plt1 = list(product(*cls_repetidos))
    r0 = [list(w) for w in plt1]
    # r0 son todos los canteros posibles, sin restricciones, sin equivalencia de rotaciones (es cls**cantero)
    r1 = []
    for u in r0:
        sirve = True
        for i in range(cantero - 1):
            if u[i] == u[i + 1]:
                sirve = False
        if u[cantero - 1] == u[0]:
            sirve = False
        if sirve:
            r1.append(u)
    # r1 son todos los canteros circulares posibles donde no puede haber dos clases iguales contiguas.
    # No hay equivalencia por rotaciones
    r2 = []
    raux = []
    for u in r1:
        sirve = True
        if u in raux:
            sirve = False
        else:
            for i in range(cantero):  # agrega todas las rotaciones de u a raux
                x = []
                for j in range(cantero):
                    x.append(u[(i + j) % cantero])
                if x not in raux:
                    raux.append(x)
        if sirve:
            r2.append(u)
    # r2 son todos los canteros circulares posibles donde no puede haber dos clases iguales contiguas.
    # Hay equivalencia por rotaciones
    # for u in r2:
    #     print u
    return len(r2)

cantero = 6
for cls_plantines in range(1, cantero ):
    print(cls_plantines,acomodar_plantines(cantero, cls_plantines))
