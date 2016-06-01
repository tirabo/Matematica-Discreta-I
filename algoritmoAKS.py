
import math
from polynomial import Polynomial as poly
import time

def mcd(a, b):
    # pre: a,b enteros.
    # post: mcd divisor de a,b usando Algoritmo de Euclides. Si ambos son nulos devuelve 0.
    if b < 0:
        b = -b
    while b > 0:
        a, b = b, a % b
    return a


def cambiodebase(m, b):
    # pre: m> 0, 1<b
    # post: devuelve una lista que es la expresion de m en base b
    ret = []
    cociente = m
    while cociente > 0:
        resto = cociente % b
        cociente = cociente/b
        ret.insert(0, resto)  # inserta por delante en la lista
    return ret


def phi(natural):
    # pre: natural  entero positivo
    # post: devuelve la phi de Euler
    result = 0
    for k in range(1, natural + 1):
        if mcd(natural, k) == 1:
            result += 1
    return result

"""
Metodo binario para exponencicion modular
Ver: 'Right-to-left binary method' en https://en.wikipedia.org/wiki/Modular_exponentiation
Se desea calular b**e % m
1) Se calcula la expresion binaria de e
Si e en base 2 es a_{n}...a_0, entonces
e = \sum_{i=0}^{n} a_i 2^i
2) Entonces b**e = (b**(2**n))**a_n * ...*(b**(2**0))*a_0
luego se calcula primero
c = (b**(2**0))*a_0 % m y luego se hace
c = c*(b**(2**1))*a_1 % m
y asi sucesivamente
"""


def pot_modulo(base, exponente, modulo):
    # pre: base, exponente, modulo enteros no negativos
    # post: devuelve b**e % m usando el metodo binario
    result = 0
    if modulo > 1:
        bine = cambiodebase(exponente, 2)
        result = 1
        pot2 = base % modulo
        while len(bine) > 0:
            # print bine
            result = result*(pot2**int(bine[-1])) % modulo
            pot2 = pot2**2 % modulo
            bine = bine[:-1]
    return result

def pot_modulo_poly_0(base, exponente, modulo):
    # pre: base polinomio; exponente, modulo enteros no negativos
    # post: devuelve b**e donde cada coeficiente se hace % m. Se usa el metodo binario
    result = poly([0])
    if modulo > 1:
        bine = cambiodebase(exponente, 2)
        result = poly([1])
        pot2 = base.mod(modulo)
        while len(bine) > 0:
            # print bine
            result = (result*(pot2**int(bine[-1]))).mod(modulo)
            pot2 = (pot2**2).mod(modulo)
            bine = bine[:-1]
    return result

def pot_modulo_poly(base, exponente, modulo):
    # pre: base y modulo son polinomios con modulo monico. exponente un entero no negativo
    # post: devuelve base**exponente % mmodulo usando el metodo binario
    result = 0
    if modulo.grado() >= 1:
        bine = cambiodebase(exponente, 2)
        result = poly([1])
        pot2 = base % modulo
        while len(bine) > 0:
            #print 'bb', bine
            #print len(bine)
            result = result*(pot2**int(bine[-1])) % modulo
            #print result
            pot2 = pot2**2 % modulo
            bine = bine[:-1]
    return result

"""
bb = poly([0, 1])**1 + poly([2])
mm = poly([0, 1])**2 + 1
ee = 56043
print bb, ' : ', mm, ' : ', ee
res =  pot_modulo_poly(bb, ee, mm)
print res
"""


def pot_monomio_modulo(ngrande, rtest, a):
    # post: devuelve true si  (x + a) ** ngrande % (x ** rtest - 1, ngrande) = x ** ngrande + a
    #       es decir si (x + a) ** ngrande - x ** ngrande + a = (x ** rtest - 1)*g + ngrande * f donde g,f in Z[x]
    #       Procedimiento: cada vez que hace una cuenta en polinomios, se hace % ngrande de los coeficientes de
    #       los polinomios (es como trabajar en Z_n)
    result = 0
    base,  exponente, modulo = poly([a, 1]), ngrande, poly([0,1])**rtest
    print  base, ':', exponente, ':',  modulo
    if modulo.grado() >= 1:
        bine = cambiodebase(exponente, 2)
        result = poly([1])
        pot2 = base % modulo
        while len(bine) > 0:
            # print 'bb', bine
            print len(bine)
            result = (result * (pot2 ** int(bine[-1])) % modulo).mod(ngrande)
            # print result
            pot2 = (pot2 ** 2 % modulo).mod(ngrande)
            print pot2
            bine = bine[:-1]
    return result

pp = poly([3, 1])**300
qq = poly([5, 1])**1000
print 'pp:', pp
# print 'qq:', qq
# print pp*qq
print (pp*qq).mod(100000)

# print pot_monomio_modulo(100000, 333, 3)

def orden_admisible(rtest, ngrande):
    # pre: rtest, ngrande enteros positivos
    # post: devuelve True si ngrande**k % rtest != 1 para for all  k tal 1 <= k <= log_2(ngrande)**2.
    #       es decir si el orden multiplicativo de ngrande en Z_rtest es > log_2(ngrande)**2
    result = True
    u = int(math.log(ngrande, 2)**2)+1
    for k in range(1, u):
        a = pot_modulo(ngrande, k, rtest)
        if a == 1:
            # print  k
            result = False
            break
    return result


def paso2(ngrande):
    # pre: entero > 0
    # post: devuelve un entero rtest > log_2(ngrande)**2 tal que orden_admisible(rtest, ngrande) == True.
    #      Es decir devuelve rtest > log_2(ngrande)**2 tal  ngrande**k % rtest != 1
    #      for all  k tal 1 <= k <= log_2(ngrande)**2
    rtest = int(math.log(ngrande, 2)**2)+1
    while not orden_admisible(rtest, ngrande):
        # print rtest
        rtest = rtest +1
    return rtest


def paso3(ngrande, rtest):
    # post: si para algun a <= rtest, mcd(a,ngrande) > 1, devuelve False (en ese caso ngrande es compuesto),
    # sino devuelve True  (en ese caso sigue el test)
    result = True
    for a in range(1, rtest+1):
        if mcd(a, ngrande) > 1:
            result = False
            break
    return result


def paso4(ngrande, rtest):
    # post: si ngrande <= rtest devuelve True (en ese caso ngrande es primo), en el otro caso devuelve False
    #       (y sigue el test)
    return ngrande <= rtest


def pot_monomio_modulo(ngrande, rtest, a):
    # post: devuelve true si  (x + a) ** ngrande % (x ** rtest - 1, ngrande) = x ** ngrande + a
    #       es decir si (x + a) ** ngrande - x ** ngrande + a = (x ** rtest - 1)*g + ngrande * f donde g,f in Z[x]
    result = True
    return result


def paso5(ngrande, rtest):
    # post: sea u = int(phi(rtest)**0.5*math.log(ngrande,2)). Entonces si for all a <= u  se cumple
    #       (x+a)**ngrande % (x**rtest-1,ngrande) = x**ngrande +a entonces devuelve True (en ese caso ngrande  es primo)
    #       en caso contrario devuelve False (y ngrande es compuesto)
    #       Aqui x es una variable independiente y congruencia se hace en polinomios.
    result = False
    u = int(phi(rtest) ** 0.5 * math.log(ngrande, 2))
    print 'u', u
    for a in range(1, u+1):
        pass
        # pot_monomio_modulo(ngrande, rtest, a)
    return result

# n = 10**100+37
# print paso2(n)
# r = 110431
# print paso3(n,r)
# print len(cambiodebase(n, 2))

# n = 10**25+37
# print paso2(n)
# r = 6899
# print paso3(n,r)
# print len(cambiodebase(n, 2))



# n = 10**25+37
# r = 6899
# r = 7000
# f = poly([1,1])

"""
n = 10**10+37
r = 1103
r = 1100
f = poly([1,1])

t0 = time.clock()
xr1 = poly([0, 1])**r + 1
print 'xr1', xr1
t1 = time.clock()
print 'Tiempo 0', t1-t0



t0 = time.clock()
h = f**100
h = h.mod(n)
nh = poly([1])
for i in range(r/100):
    nh = nh * h
    nh = nh.mod(n)
    #print i
t1 = time.clock()
print nh.grado()
print 'Tiempo 0', t1-t0


t0 = time.clock()
for i in range(r/100):
    nh = nh * h
    nh = nh.mod(n)
    nh = nh % xr1
    print i
t1 = time.clock()
print nh.grado()
print 'Tiempo', t1-t0
"""


