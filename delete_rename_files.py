#!/usr/bin/python

import math, glob
import os
direct=raw_input("write the folder inside include directory: ")



path = '/home/suvo/galprop-56/binary/binaryxerces/include/xercesc/framework/%s/'%(direct)
writewhat = '#include </home/suvo/galprop-56/binary/binaryxerces/include/xercesc/'

listof_files=glob.glob(path+'./*.hpp')

print listof_files


for filename in listof_files:
	os.remove(filename)


listof_filesnewname=glob.glob(path+'/*.out')

print listof_filesnewname


for newfilename in listof_filesnewname:
	new_newfilename=newfilename.replace('out','hpp')
	print new_newfilename
	os.rename(newfilename, new_newfilename)
#newfile.close()
