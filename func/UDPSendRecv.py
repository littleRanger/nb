#coding:utf-8
import socket
import struct
import binascii
def UDPSendtoBS(LocalAddr, DesAddr,data):
    udpsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udpsock.bind(LocalAddr)
    #str = "88010101"
    origindata = data
    temp =""
    sendingdata =""
    while origindata:
        temp = origindata[0:2]
        s = int(temp,16)
        sendingdata += struct.pack('B',s)
        origindata = origindata[2:]
    print 'origindata:',data
    print 'sendingdata',binascii.hexlify(sendingdata)
    while True:
        if(udpsock.sendto(sendingdata,DesAddr)):
            pass
        udpsock.close()
        break

def UDPRecvfromBS(ListenAddr):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #从指定的端口，从任何发送者，接收UDP数据
    s.setblocking(0)
    s.bind((ListenAddr))
    print('正在等待接入...')
    while True:
        #接收一个数据
        data,addr=s.recvfrom(1024)       
        print('Received:',binascii.hexlify(data),'from',addr)
    return data
if __name__  == "__main__":
    UDPSendtoBS(('192.168.31.31',8000),('192.168.31.168',2000),"a12")
