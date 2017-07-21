#coding:UTF-8
#invalid
from app import BSConfig


def BSConfigSentToBS(address,):
    s=socket.socket(socket.AF_INET, SOCKET_DGRAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    s.bind(address)



