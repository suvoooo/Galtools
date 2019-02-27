#!/usr/bin/python
import sys, pyfits, string, math
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

files=[]
headers=[]
datas=[]

nt={}
nt[(0,1)]="neutron"
nt[(1,1)]="proton"
nt[(-1,1)]="anti-proton"
nt[(1,0)]="positron"
nt[(-1,0)]="electron"
nt[(0,0)]="neutrino"
nt[(1,2)]="deuteron"
nt[(-1,2)]="anti-deuteron"

el={}
el[2]="He"
el[3]="Li"
el[4]="Be"
el[5]="B"
el[6]="C"
el[7]="N"
el[8]="O"
el[9]="F"
el[10]="NE"
el[11]="Na"
el[12]="Mg"
el[13]="Al"
el[14]="Si"
el[15]="P"
el[16]="S"
el[17]="Cl"
el[18]="Ar"
el[19]="K"
el[20]="Ca"
el[21]="Sc"
el[22]="Ti"
el[23]="V"
el[24]="Cr"
el[25]="Mn"
el[26]="Fe"



def nucltype(z,a):
	if z<2:
		return nt[(z,a)]
	else:
		return el[z]+"-"+str(a)

def selecteind(a):
	if a >1:
		return 2.7
	else:
		return 3.0

filenames = sys.argv[1:]

for f in filenames:
	files.append(pyfits.open(f))
	#print hl.info()
	headers.append(str(files[-1][0].header).splitlines(False))
	datas.append(files[-1][0].data)

hls=[]
for h in headers:
	hls.append(len(h))
if len(set(hls))>1:
	print "headers do not have same length"
	print hls
	for h in headers:
		print "====================================================="
		print "HEADER:"
		for l in h:
			print l
	sys.exit(1)

Estart=False
Edelta=False
headerlist=[]
for h in zip(*headers):
	if not len(set(h))<=1:
		print "Difference found:"
		for i in list(h):		
			print i
		sys.exit(1)
	else:
		entry=tuple(set(h))[0]
		if entry.partition(' ')[0]=="CRVAL3":
			Estart=float(entry.replace(" ","").partition("=")[2].partition("/")[0])
			print Estart
		if entry.partition(' ')[0]=="CDELT3":
			Edelta=float(entry.replace(" ","").partition("=")[2].partition("/")[0])
			print Edelta
		headerlist.append(entry)
		
if not Estart:
	print "No value for Energy start found"
	sys.exit(1)

if not Edelta:
	print "No value for Energy increment found"
	sys.exit(1)

dls=[]
for d in datas:
	dls.append(len(d))	
if len(set(dls))>1:
	print "datasets do not have same length"
	print dls
	sys.exit(1)

headerlist=headerlist[-dls[0]*3:] 
dnlist=zip(headerlist[0::3] , headerlist[1::3] , headerlist[2::3] )

for dn in dnlist:
	continue

fig=plt.figure()
fig.patch.set_facecolor('white')
dni=-1
for d in zip(*datas):
	dni=dni+1
	plothead=(dnlist[dni][0]+dnlist[dni][1]+dnlist[dni][2]).replace(" ","").replace("electrons","").replace("ofnucleus","").replace('/',"").replace('NUC',"")
	ni=int(plothead.rpartition('-')[2])
	zak=plothead.split('=')[1:]
	z=int(zak[0].partition('Z')[0])
	a=int(zak[1].partition('A')[0])
	k=int(zak[2].partition('K')[0])
	plothead="n%dZ%dA%dK%d"%(ni,z,a,k)
	print "nuleus no. %d - %s "%(ni,plothead)
	title="nucl %d - %s"%(ni,nucltype(z,a))
	if dni<3:
		
		els=[]
	for i in d:
		els.append(len(i))
	if len(set(els))>1:
		print "energy axes do not have same length"
		print els
		sys.exit(1)
	e=[]			
	fvals=[]
	for i in d:
		fvals.append([])
		for ex in i:
			fvals[-1].append(ex[0][8])
	for ne in range(len(d[0])):
		e.append(math.pow(10,Estart+Edelta*ne))
	
		
	ax=fig.add_subplot(211)
	for i in range(len(d)):	
		fvalsmod=[]
		eind=selecteind(a)
		print "multiplied with energy index:"
		print eind
		for ei,fi in zip(e,fvals[i]):
			fvalsmod.append(fi*ei**-2*ei**eind)		
		plt.plot(e,fvalsmod)
	
	ax.set_xscale('log')
	ax.set_yscale('log')
	ax.set_ylabel('flux x E^%2.1f'%eind)
	ax=fig.add_subplot(212)
	fvalsdiff=[]
	for ei,fi1,fi2 in zip(e,fvals[0],fvals[1]):
		raw1=fi1*ei**-2
		raw2=fi2*ei**-2
		fvalsdiff.append((raw1-raw2)/(0.5*raw1+0.5*raw2))
	plt.plot(e,fvalsdiff)
	ax.set_xscale('log')
	ax.set_yscale('linear')
	ax.set_xlabel('E [MeV]')
	ax.set_ylabel('(f1 - f2) x average')
	fig.suptitle(title)
	plt.savefig("./compareplots/"+plothead+".png")
	plt.clf()	
	


sys.exit(0)

print len(dnlist)
print len(zip(*datas))
