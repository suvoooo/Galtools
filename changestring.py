#!/usr/bin/python

import math, glob

direct=raw_input("write the folder inside include directory: ")



path = '/home/suvo/galprop-56/binary/binaryxerces/include/xercesc/framework/%s/'%(direct)
writewhat = '#include </home/suvo/galprop-56/binary/binaryxerces/include/xercesc/'

listof_files=glob.glob(path+'/*.hpp')

print listof_files


for filename in listof_files:
	FI = open(filename,'r')
	Fout = open(filename.replace('hpp', 'out'),'w')
	for line in FI:
		Fout.write(line.replace('#include <xercesc/', writewhat))
	FI.close()
	Fout.close()
