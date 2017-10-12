#-*- coding:utf-8 -*-
import socket
import struct
def UDPSendtoBS(LocalAddr, DesAddr,data):
    udpsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udpsock.bind(LocalAddr)
    udpsock.setblocking(0)
    while True:
        if(udpsock.sendto(data,DesAddr)):
            print("already sended msg to BS!")
        udpsock.close()
        break
    return 0 #success

def UDPRecvfromBS(ListenAddr):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #从指定的端口，从任何发送者，接收UDP数据
    s.setblocking(0)
    s.settimeout(5)
    s.bind(ListenAddr)
    print('waiting for connet..')
    while True:
        #接收一个数据
        data,addr=s.recvfrom(1024)
        return data
if __name__  == "__main__":
    #UDPSendtoBS(('127.0.0.1',8000),('127.0.0.1',2000),'data')
    UDPRecvfromBS(('127.0.0.1',2000))    
