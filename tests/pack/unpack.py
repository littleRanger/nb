import struct
from UDPSendRecv import *

rowdata = UDPRecvfromBS(('127.0.0.1', 8080))
print type(rowdata)
print rowdata
print len(rowdata)
structx = struct.Struct('=HIH')
data = structx.unpack(rowdata)
print data[0], data[1], data[2]
