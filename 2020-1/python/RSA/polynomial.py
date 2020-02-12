import collections
import itertools
import time


class Polynomial(object):
    def __init__(self, *args):
        """
        Create a polynomial in one of three ways:

        p = Polynomial(poly)           # copy constructor
        p = Polynomial([1,2,3 ...])    # from sequence
        p = Polynomial(1, 2, 3 ...)    # from scalars
        La division de polinomios se hace en Q[x]
        """
        super(Polynomial, self).__init__()
        if len(args) == 1:
            val = args[0]
            if isinstance(val, Polynomial):  # copy constructor
                self.coeffs = val.coeffs[:]
            elif isinstance(val, collections.Iterable):  # from sequence
                self.coeffs = list(val)
            else:  # from single scalar
                self.coeffs = [val + 0]
        else:  # multiple scalars
            self.coeffs = [i + 0 for i in args]
        self.trim()

    def __add__(self, val):
        "Return self+val"
        if isinstance(val, Polynomial):  # add Polynomial
            res = [a + b for a, b in itertools.izip_longest(self.coeffs, val.coeffs, fillvalue=0)]
        else:  # add scalar
            if self.coeffs:
                res = self.coeffs[:]
                res[0] += val
            else:
                res = val
        return self.__class__(res)

    def __call__(self, val):
        "Evaluate at X==val"
        res = 0
        pwr = 1
        for co in self.coeffs:
            res += co * pwr
            pwr *= val
        return res

    def __eq__(self, val):
        "Test self==val"
        if isinstance(val, Polynomial):
            return self.coeffs == val.coeffs
        else:
            return len(self.coeffs) == 1 and self.coeffs[0] == val

    def __mul__(self, val):
        "Return self*val"
        if isinstance(val, Polynomial):
            _s = self.coeffs
            _v = val.coeffs
            res = [0] * (len(_s) + len(_v) - 1)
            for selfpow, selfco in enumerate(_s):
                for valpow, valco in enumerate(_v):
                    res[selfpow + valpow] += selfco * valco
        else:
            res = [co * val for co in self.coeffs]
        return self.__class__(res)

    def __div__(self, val):
        "Return self/val, val debe ser monico"
        q, r = Polynomial(), self  # A cada paso el invariante es self = val * q + r
        x = Polynomial([0,1])
        while r != 0 and r.grado() >= val.grado():
            if val.lead() != 1:
                break
            g = r.grado() - val.grado()
            t = r.lead() * x**g # Divide los coeficientes principales
            q, r = q + t, r - (t * val)
        return q

    def __mod__(self, val):
        "Return self % val, val debe ser monico"
        q, r = Polynomial([0]), self  # A cada paso el invariante es self = val * q + r
        x = Polynomial([0, 1])
        while r != 0 and r.grado() >= val.grado():
            # print('rrrr', r.grado())
            if val.lead() != 1:
                break
            g = r.grado() - val.grado()
            t = r.lead() * x ** g  # Divide los coeficientes principales
            q, r = q + t, r - (t * val)
        return r

    def __neg__(self):
        "Return -self"
        return self.__class__([-co for co in self.coeffs])

    def __pow__(self, y, z=None):
        "Devuelve self**n"
        u = 1
        i = 1
        while y > 0:
            u = u * self
            y = y - 1
            i = i + 1
        return u

    def __radd__(self, val):
        "Return val+self"
        return self + val

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.coeffs)

    def __rmul__(self, val):
        "Return val*self"
        return self * val

    def __rsub__(self, val):
        "Return val-self"
        return -self + val

    def __str__(self):
        "Return string formatted as aX^3 + bX^2 + c^X + d"
        res = []
        for po, co in enumerate(self.coeffs):
            if co:
                if po == 0:
                    po = ''
                elif po == 1:
                    po = 'X'
                else:
                    po = 'X^' + str(po)
                res.append(str(co) + po)
        if res:
            res.reverse()
            return ' + '.join(res)
        else:
            return "0"

    def __sub__(self, val):
        "Return self-val"
        return self.__add__(-val)

    def trim(self):
        "Remove trailing 0-coefficients"
        _co = self.coeffs
        if _co:
            offs = len(_co) - 1
            if _co[offs] == 0:
                offs -= 1
                while offs >= 0 and _co[offs] == 0:
                    offs -= 1
                del _co[offs + 1:]

    def grado(self):
        "Devuelve el grado de un polinomio"
        _co = self.coeffs
        return len(_co) - 1

    def lead(self):
        "Devuelve el coeficiente principal del polinomio"
        _co = self.coeffs
        prin = len(_co)- 1
        return _co[prin]

    def coeff(self,n):
        "Devuelve el coeficiente de x**n"
        pass
    def mod(self,n):
        "Devuelve  el plolinomio con los coeficientes modulo n"
        _co = self.coeffs
        np = []
        for i in range(len(_co)):
            np.append(_co[i] % n)
        return Polynomial(np)



"""
f = Polynomial([1, 2, 1])
g = Polynomial([1, 2, 0, 3, 0, 1, 0 , 5])
h = Polynomial([1, 0, 0, 0, 5])

print g, '/', f
print g/f
print g % f

q = Polynomial([0, 31, -22, 16, -10, 5])
r = Polynomial([1, -29, -40])
print q*f + r

f = Polynomial([1, 2, 1])
print f % f
"""

"""
t0 = time.clock()
n = 10**100+37

f = Polynomial([1,1])
g = Polynomial([2, 3, 1])
r = 110431

h = f**100
h = h.mod(n)


nh = Polynomial([1])
for i in range(1000):
    nh = nh * h
    nh = nh.mod(n)
    print i

t1 = time.clock()

print 'Tiempo', t1-t0
"""

"""
nh = Polynomial([1])
t0 = time.clock()
for i in range(r):
    nh = nh * f
    nh = nh.mod(n)
    #print i
t1 = time.clock()
print 'Tiempo', t1-t0
"""

"""
h = f**200
t0 = time.clock()
h = h.mod(n)
nh = Polynomial([1])
for i in range(r/200):
    nh = nh * h
    nh = nh.mod(n)
    #print i
t1 = time.clock()
print nh.grado()
print 'Tiempo', t1-t0
"""

