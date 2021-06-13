import time

def mcd(a: int, b: int) -> int:
    # pre: a y b son números enteros, alguno de ellos no nulo
    # post: devuelve  mcd(a,b)     
    assert type(a) == type(b) == int and (a != 0 or b != 0 ), 'Los números deben ser enteros, alguno no nulo'
    a, b = abs(a), abs(b)
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

def gcd_r(x, y): # de Elements of Programming Interviews in Python The Insiders’ Guide by Adnan Aziz, Tsung-Hsien Lee, Amit Prakash p. 352
    # recursivo, no usa: *, //,  %. Solo operaciones bitwise.
    # x & y = el AND de los números binarios correspondientes => x & 1 == 0 sii x es par, x & 1 == 1 sii x es impar
    # x >> 1,  en binario tachar el último dígito =>  x >> 1 == x // 2
    # x << 1,  en binario agregar un 0  al final => x << 1 == 2 * x
    if x > y:
        return gcd_r(y, x)
    elif x == 0:
        return y
    elif not x & 1 and not y & 1: # x and y are even.
        return gcd_r(x >> 1, y >> 1) << 1
    elif not x & 1 and y & 1: # x is even, y is odd.
        return gcd_r(x >> 1, y)
    elif x & 1 and not y & 1: # x is odd, y is even.
        return gcd_r(x, y >> 1)
    return gcd_r(x, y - x) # Both x and y are odd.

def gcd(x, y): # de Elements of Programming Interviews in Python The Insiders’ Guide by Adnan Aziz, Tsung-Hsien Lee, Amit Prakash p. 352
    # pre: x >= 0, y >= 0,  alguno no nulo.
    # NO recursivo. No usa: *, //,  %. Solo operaciones bitwise.
    # x & y = el AND de los números binarios correspondientes => x & 1 == 0 sii x es par, x & 1 == 1 sii x es impar
    # x >> 1,  en binario tachar el último dígito =>  x >> 1 == x // 2
    # x << 1,  en binario agregar un 0  al final => x << 1 == 2 * x
    mcd  = 1
    k = 0
    while not x & 1 and not y & 1: # x and y are even.
        x, y, k = x >> 1, y >> 1, k + 1 
    # Ahora x, y = x // 2**k, y // 2**k, x o y impar y gcd = 2**k * gcd(x , y)
    while y != 0:
        if x == 0:
            for k in range(k): 
                y  = y << 1
            mcd, y = y, 0
            # el gcd es y * 2**k
        elif not x & 1 and y & 1: # x is even, y is odd.
            # print('x is even, y is odd',x,y,mcd)
            x = x >> 1
            # print(x, y, mcd)
        elif x & 1 and not y & 1: # x is odd, y is even.
            # print('x is odd, y is even',x,y,mcd)
            y = y >> 1
            # print(x, y, mcd)
        else: # both x and y are odd.
            # print('x is odd, y is odd',x,y,mcd)
            if y >= x:
                x, y = y - x, x
            else:
                x = x - y
            # print(x, y, mcd)
    return mcd

def gcd_2(x, y): # de Elements of Programming Interviews in Python The Insiders’ Guide by Adnan Aziz, Tsung-Hsien Lee, Amit Prakash p. 352
    # pre: x >= 0, y >= 0,  alguno no nulo.
    # NO recursivo. No usa: *, //,  %. Solo operaciones bitwise.
    # x & y = el AND de los números binarios correspondientes => x & 1 == 0 sii x es par, x & 1 == 1 sii x es impar
    # x >> 1,  en binario tachar el último dígito =>  x >> 1 == x // 2
    # x << 1,  en binario agregar un 0  al final => x << 1 == 2 * x
    mcd  = 1
    pot2 = 0
    while y != 0:
        if x == 0:
            for k in range(pot2): 
                y  = y << 1
            mcd, y = y, 0
        elif not x & 1 and not y & 1: # x and y are even.
            # print('x and y are even',x,y,mcd)
            x, y, pot2 = x >> 1, y >> 1, pot2 + 1 
            # print(x, y, mcd)
        elif not x & 1 and y & 1: # x is even, y is odd.
            # print('x is even, y is odd',x,y,mcd)
            x = x >> 1
            # print(x, y, mcd)
        elif x & 1 and not y & 1: # x is odd, y is even.
            # print('x is odd, y is even',x,y,mcd)
            y = y >> 1
            # print(x, y, mcd)
        else: # both x and y are odd.
            # print('x is odd, y is odd',x,y,mcd)
            if y >= x:
                x, y = y - x, x
            else:
                x = x - y
            # print(x, y, mcd)
    return mcd



def main():
    # Ejemplos
    n, m = 10**100 + 10000057777452552451767467456784889556356356563563, 10**100+ 100000585575423542452457545234523534524567787856959060021
    n, m = 2**3 *7*5,  2**2 *7*3
    t0 = time.time()
    x = mcd(n, m)
    print('mcd',x)
    t1 = time.time()
    print('mcd:',n,m,'  ',t1-t0)

    t0 = time.time()
    x = gcd(n, m)
    print('gcd',x)
    t1 = time.time()
    print('gcd:',n,m,'  ',t1-t0)
    return 0

# RUN
 
if __name__ == '__main__':
    main()