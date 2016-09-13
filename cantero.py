import copy

conf1 = []
for i in range(4):
	conf1.append([i])


conf2 = []
for i in range(4):
	for u in conf1:
		v = u[:]
		v.append(i)
		conf2.append(v)

		
conf3 = []
for i in range(4):
	for u in conf2:
		v = u[:]
		v.append(i)
		conf3.append(v)
		
conf4 = []
for i in range(4):
	for u in conf3:
		v = u[:]
		v.append(i)
		conf4.append(v)
		
conf5 = []
for i in range(4):
	for u in conf4:
		v = u[:]
		v.append(i)
		conf5.append(v)

conf = []
for i in range(4):
	for u in conf5:
		v = u[:]
		v.append(i)
		conf.append(v)
conf.sort()
	
for u in conf:
	print u
	
exit(0)

r1 = []

for u in conf:
	sirve = True
	for i in range(5):
		if u[i] == u[i+1]:
			sirve = False
	if u[5] == u[0]:
		sirve = False
	if sirve == True:
		r1.append(u)
"""		
print len(r1)
for u in r1:
	print u
"""

r2 = []
raux = []
for u in r1:
	sirve = True
	if u  in raux:
		sirve = False
	else:
		for i  in range(6):
			x = []
			for j in range(6):
				x.append(u[(i+j)%6])
			if  x not  in raux:
				raux.append(x)
	if sirve == True:
		r2.append(u)
		
print len(r2)
for u in r2:
	print u
	
