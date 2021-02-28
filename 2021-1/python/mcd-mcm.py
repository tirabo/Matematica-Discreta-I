def mcd(a: int, b: int) -> int:
    # pre: a y b son números positivos
    # post: devuelve  mcd(a,b) o 0 si a == b ==0
    a = abs(a)
    b = abs(b)
    if a == 0 and b == 0:
        print('alguno de los dos números debe ser distinto de cero')
        return 0
    i, j = a, b
    while j != 0:
        # invariante: mcd(a, b) = mcd(i, j)
        resto = i % j  # i = q * j + resto
        i = j
        j = resto
    return i
    
def mcm(a: int,b: int) -> int:
    # pre: a y b son números positivos
    # post: obtenemos  mcm(a,b) o 0 si a==0==b
    if a == 0 and b == 0:
        return 0
    else: 
        return a*b // mcd(a,b)
    
def mcd2(a: int, b: int):
    # pre: a y b son números positivos
    # post: Obtenemos s y t tal que mcd(a,b) = a*s + b*t
    r0, r1 = a, b
    s0, t0 = 1, 0
    s1, t1 = 0, 1
    i = 1 
    while r1 != 0:
        # invariante: r0 = a * s0 + b * t0
        #             y  mcd(a, b) = mcd(r0, r1)
        resto = r0 % r1
        q, r0, r1 = r0 // r1, r1, resto
        s1p, t1p = s1, t1
        s1, s0 = s0 - s1 * q, s1p
        t1, t0 = t0 - t1 * q, t1p
        i = i+1
    return s0, t0
# Demostración: por  algoritmo de Euclides tenemos
# r[i-1] =  r[i] * q + r[i+1], con q =  r[i-1] // r[i] (*)
# Si tenemos
#  r[i] = a * s[i] + b * t[i]
#  r[i-1] = a * s[i-1] + b * t[i-1]
# Por (*)
# r[i+1] = r[i-1] - r[i] * q
#          = a * s[i-1] + b * t[i-1] - (a * s[i] + b * t[i]) * q
#          = a * (s[i-1] - q * s[i]) + b * (t[i-1] - q * t[i])
# Luego, s[i+1] = s[i-1] - q * s[i], t[i+1] = t[i-1] - q * t[i]


def main():
    # Ejemplos
    print(mcd2(15,21))
    print(mcd(-15,21))
    print(mcm(15,21))
    return 0

# RUN
 
if __name__ == '__main__':
    main()