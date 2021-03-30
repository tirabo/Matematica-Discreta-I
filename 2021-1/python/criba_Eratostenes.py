
# criba de Eratóstenes

def criba(n: int) -> list[int]:
    # pre: n > 0
    criba = [2]*(n+1) # lista de 2's de longitud n + 1 
    for i in range(1, n + 1, 2):
        criba[i] = i # en los lugares impares se pone criba[i] = i
    i = 3
    while i*i < n + 1:
        if criba[i] == i:
            for j in range(i*i, n + 1, i):
                if criba[j] == j:
                    criba[j] = i
        i = i + 1
    return criba # post:  criba[i] = menor factor primo de i (i >0)

def primos_hasta(n: int) -> list[int]:
    # pre: n > 0
    # post: devuelve primos, una lista de primos  <= n
    criba_n = criba(n)
    primos = []
    for i in range(3, n + 1, 2):
        if criba_n[i] == i:
            primos.append(i)
    return primos

def desc_prima(n: int) -> list[int]:
    # pre: n > 0
    # post: devuelve descomposición prima de n como una lista de primos <= n
    primos = []
    k = n
    while k > 1:
        p = criba(k)[-1] # el menor primo que divide a k
        primos.append(p)
        k = k // p
        
    return primos


# print(len(criba(10**8))) # esto ya toma mucho tiempo 
# print(primos_hasta(101))
print(desc_prima(1024))

