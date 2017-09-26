#coding:utf-8
from UDPSendRecv import UDPSendtoBS
import struct
import binascii
import IPy
a=0x08
b=0x09
c=0x01
aa=u'192.168.1.1'
d=aa.encode('ascii')
value=(0x0908,)
s=struct.Struct('!H')
p=s.pack(*value)
print 'packed data:',binascii.hexlify(p)
UDPSendtoBS(('127.0.0.1',6000),('127.0.0.1',9000),p)
