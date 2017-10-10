#coding:utf-8
import struct

value1=(0x88, 0x88, 0x32)
strt1=struct.Struct('!3B')
d1=strt1.pack(*value1)
a= strt1.unpack(d1)
print(a)
x=u'1'
value2=(0x88, 0x88, 0x32,int(x))
strt2=struct.Struct('!3BH')
d2=strt2.pack(*value2)
a= strt2.unpack(d2)
print(a)
