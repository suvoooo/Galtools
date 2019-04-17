#!/usr/bin/python

import os, sys, time, math, glob

try:
   import cPickle as pickle
except:
   import pickle

mDMmin=1490.0
mDMmax=1510.0
#Emin=1.0
#Emax=4000.0
xMax = 1
xMin = 10e-7
pli=-2.3
PM="MIN"

BR={}
#BR["LKP"]={"e":0.2,"Mu":0.2,"Tau":0.2,"q":0.11,"c":0.11,"t":0.11,"h":0.02}
#BR["Hino"]={"b":0.85,"Tau":0.15}
#BR["Gino"]={"Z":0.5,"W":0.5}
#BR["el"]={"e":1.0}
#BR["mu"]={"Mu":1.0}
BR["tau"]={"Tau":1.0}
#BR["W"]={"W":1.0}
#BR["b"]={"b":1.0}

def main():
	flxatp = []
	fd=readCirelli()
	print "done reading"
	for mDM,ed in fd.iteritems():
#		print mDM
		E=sorted(ed.keys())
		F={}
		for DMp in BR.keys():
			F[DMp]={}
#				print e , totflx
		for e in E:
#			print "Energy "+str(e)
			for DMp,br in BR.iteritems():			
				totflx=0.0
				for c,b in br.iteritems():
					totflx=totflx+(b*ed[e][c])
					flxatp.append(totflx)
				#print len(flxatp)
				F[DMp][e]=totflx/mDM/mDM/e/2.303
#		for DMp,flx in F.iteritems():
#			fpicklef='/nfs/RAID/home/suvob/dmfluxes/mc%ssmflxs/smflx-%s-%3.2f.dat'%(PM,DMp,mDM)
#			normflx=norm(flx,mDM)
#			saveresults(fpicklef,normflx)
#			loadresults(fpicklef,normflx)

def readCirelli():
	d_file = open('/home/suvo/Downloads/dmfluxes_atproduction/MuatproPPPC4%iGeVdlogx.d' %(mDMmin+10),'w')
	MCfile=open("/home/suvo/Downloads/AtProduction_all.dat/AtProduction_positrons.dat",'r')
	header = MCfile.readline()
	print header
	flxdct={}
	while True:
		stringline = MCfile.readline()
      		if stringline=='':
			break
		stringlist=stringline.split()
		mDM=float(stringlist.pop(0))
		if mDM>mDMmax or mDM<mDMmin:
			continue
		if not mDM in flxdct.keys():
			flxdct[mDM]={}
#		halo=stringlist.pop(0)  
#		if not halo in ["NFW"]:
#			continue 
#		prop=stringlist.pop(0)   
#		if not prop==PM:
#			continue   
		logx=float(stringlist.pop(0))
		#print logx
		x=pow(10,logx)
#		print x
		E = x * mDM   
		if x>xMax or x<xMin:
			continue
		eL=float(stringlist.pop(0))     
		eR=float(stringlist.pop(0))
		e=float(stringlist.pop(0))           
		MuL=float(stringlist.pop(0))    
		MuR=float(stringlist.pop(0))  
		Mu=float(stringlist.pop(0))     
		TauL=float(stringlist.pop(0))      
		TauR=float(stringlist.pop(0))         
		Tau=(float(stringlist.pop(0)))         
		q=float(stringlist.pop(0))        
		c=float(stringlist.pop(0))              
		b=float(stringlist.pop(0))             
		t=float(stringlist.pop(0))                 
		WL=float(stringlist.pop(0))       
		WT=float(stringlist.pop(0))      
		W=float(stringlist.pop(0))               
		ZL=float(stringlist.pop(0))            
		ZT=float(stringlist.pop(0))          
		Z=float(stringlist.pop(0))           
		g=float(stringlist.pop(0))               
		Gamma=float(stringlist.pop(0))       
		h=float(stringlist.pop(0))           
		Nue=float(stringlist.pop(0))      
		NuMu=float(stringlist.pop(0))    
		NuTau=float(stringlist.pop(0))     
		Ve=float(stringlist.pop(0))            
		VMu=float(stringlist.pop(0))     
		VTau=float(stringlist.pop(0))  
		flxdct[mDM][E]={"e":e,"Mu":Mu,"Tau":Tau,"W":W,"Z":Z,"q":q,"c":c,"b":b,"t":t,"h":h}
		print "%f %2.5e %2.5e %2.5e"%(logx,x,E,(Mu))
		d_file.write('{0:2} {1:3}'.format(x,(Mu)) + '\n')
	MCfile.close()
	return flxdct

def norm(flx,mass):
	e=[]
	normflx=[]
        print "norm - mDM: "+  str(mass)
	for i in range(4000):
		e=10**(i*0.001)
		if e>mass:
			normflx.append(0)
			continue
		edr=sorted(flx.keys())
		p=0.0
		for j in range(len(edr)):
			if edr[j]>e:
				x1=edr[j-1]
				x2=edr[j]
				y1=flx[edr[j-1]]
				y2=flx[edr[j]]
				p=y1+(y2-y1)*(e**pli-x1**pli)/(x2**pli-x1**pli)
				break
		normflx.append(p*3.0) # (should be multiplied by 6 in order to get the total flux)
		# flux is given for 10^-26 (or not?), output norm sigv = 3*10^-26
		#! output is electron + positron flux !!! (input also?)
		#print normflx[i]
	print len(normflx)
	return normflx

def saveresults(rfn,results):
	sfile=open(rfn,'w')   
	pickle.dump(results, sfile,protocol=-1)
	sfile.close 

def loadresults(rfn,results):
	sfile = open (rfn,'r')
	loadthing = pickle.load(sfile)
	sfile.close 
  	return loadthing
	


if __name__ == '__main__':
	sys.exit(main())	

