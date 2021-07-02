import itertools

"""
Se colocan 6 plantines en un cantero circular
1) Hay 4 clases de plantines (0, 1, 2, 3)
2) No puede haber 2 plantines consecutivos de la misma clase
De cuantas formas se puede hacer? (las rotaciones son equivalentes)
"""

cls = [0, 1, 2, 3]
plt1 = list(itertools.product(cls, cls, cls, cls, cls, cls))
r0 = []
for u in plt1:
    r0.append(list(u))
# r0 son todos los canteros posibles, sin restricciones, sin equivalencia de rotaciones (es cls**6)


r1 = []
for u in r0:
    sirve = True
    for i in range(5):
        if u[i] == u[i + 1]:
            sirve = False
    if u[5] == u[0]:
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
        for i in range(6):  # agrega todas las rotaciones de u a raux
            x = []
            for j in range(6):
                x.append(u[(i + j) % 6])
            if x not in raux:
                raux.append(x)
    if sirve:
        r2.append(u)
# r2 son todos los canteros circulares posibles donde no puede haber dos clases iguales contiguas.
# Hay equivalencia por rotaciones
print(len(r2))
# for u in r2:
#     print u
