import aritmetica as md1
import math

"""
Test deterministico  de primalidad de  Miller Rabin (asume la Hipotesis de Riemman)

https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

Input: ng > 1, es un entero impar el cual veremos si es primo.
Output: False si ng is compuesto, True si ng es primo

escribir  ng - 1 = 2**s * d con mcd(2,d) = 1.
for a in  [2,min(ng - 1,2 * ln(ng)**2)]:
   Si para todo r in [0,s - 1]  -> a**d \not \equiv 1 (mod ng) and a**(2**r * d)\not \equiv - 1 (mod ng)
         return False
return True
"""


def mrd(ng):
    d = (ng - 1) / 2
    s = 1
    while d % 2 == 0:
        d = d / 2
        s = s + 1
    # ng - 1 = 2**s * d  con mcd(2, d) = 1
    vr = int(min(ng - 1, 2 * math.log(ng)**2)) + 1
    print 'Chequeos: ',vr
    for a in range(2, vr):
        # print 'a', a
        if a % 1000 == 0:
            print 'chequeo: ',a
        compuesto = True # True si es composite, False si no se sabe
        for r in range(s):
            chk1 = md1.pot_modulo(a, d, ng)  # a**d % ng calculado en forma eficiente
            chk2 = md1.pot_modulo(chk1, 2**r, ng)  # a**(2**r * d) % ng calculado en forma eficiente
            # print r, chk1, chk2
            compuesto = compuesto and (chk1 != 1 and chk2 != ng - 1)
        if compuesto:
            return False
    return True


#n1 = 10**10+79
n1 = 10**15+37
#n1 = 43
#n1 = 45

n1 = 2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077
n2 = 2367495770217142995264827948666809233066409497699870112003149352380375124855230068487109373226251983
print mrd(n1)




# 43 - 1 = 42 = 2**1 * 21
# s = 1, d = 21
# vr = 29
# a = 2, r = 1
# chk1 = 2**9 % 37 =
# 2**9 % 37 = 31


