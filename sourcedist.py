#!/usr/bin/python 

import math 
import matplotlib.pyplot as plt

d_0  = 8.5 # kpc
sigma = 0.6 # kpc ; spiral arm thickness

sourceG = []
dist = []
sourceM =[]

def Gsource(r, r_0):
	return (math.sqrt(r/r_0) ) * math.exp(-((r-r_0)/ r_0 ))



for i in range(0,200, 1):
	ik = i*0.1
	q = Gsource(ik,d_0)
	sourceG.append(q)
	dist.append(ik)

print len(sourceG), len(dist)




dists = []
spiralarm = [2.5,6.5,10.5,14.5]


for k in range(0,200,1):
		l = k*0.1
		expterm1 = ((l-spiralarm[0])**2)/(2*(sigma**2))
		expterm2 = ((l-spiralarm[1])**2)/(2*(sigma**2))
		expterm3 = ((l-spiralarm[2])**2)/(2*(sigma**2))
		expterm4 = ((l-spiralarm[3])**2)/(2*(sigma**2))
		expterms = math.exp(-expterm1) + math.exp(-expterm2) + math.exp(-expterm3) + math.exp(-expterm4) 
		modsource = Gsource(l,d_0) * expterms 
		sourceM.append(modsource)
		dists.append(l)
	











fig = plt.figure(figsize=(11.,10.))
fig.patch.set_facecolor('white')

plt.xlabel('Distance (Kpc)', fontsize=15)
plt.ylabel ('Source Function (Not Normalized)', fontsize=15)

plt.xlim(0,17)
plt.ylim(0.01, 1.3)
plt.plot(dist, sourceG, linestyle='-', linewidth=2, color='red', label = 'GALPROP')
plt.plot(dists, sourceM, linestyle='-.', color='blue', label = 'Spiral Arm Thickness 0.6 kpc')
plt.legend(fontsize=13)
plt.show()







