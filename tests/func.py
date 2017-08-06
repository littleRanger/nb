#coding:UTF-8
#invalid
from app import BSConfig
import socket,struct

def BSConfigSentToBS(localaddress, remoteaddress, SendingStr):
    s=socket.socket(socket.AF_INET, SOCKET_DGRAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    s.bind(localaddress)
    str_temp = ""
    str_temp += struct.pack('B',SendingStr)
    
    while True:
        s.sendto(str_temp, remoteaddress)


