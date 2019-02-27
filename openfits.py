#!/usr/bin/python
import pyfits

hl=pyfits.open('/home/suvo/Downloads/tarfiles/galprop-54.1.984_nbysource/FITS/nuclei_54_firstvelatrial.gz')
print hl.info()
print hl[0].header
x = hl[0].header
print x[0]
print hl[0].data
y = hl[0].data
#print y[]
hl.close()
