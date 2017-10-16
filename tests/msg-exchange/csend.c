#include <stdio.h>  
#include <stdlib.h>
#include <sys/types.h>  
#include <string.h>
#include <sys/socket.h>  
#include <netinet/in.h>  
#include <arpa/inet.h>  
#include <unistd.h>      
#pragma pack(1)
//struct trxmsg{
//	unsigned char flag1;
//	unsigned char flag2;
//	unsigned char flag3;
//	unsigned short bsid;
//	unsigned int trxid;
//	unsigned short ssid;
//    	char trxname[10];
//	char trxip[8];
//	unsigned short trxport;
//	unsigned short trxtxpower;
//	unsigned short trxdatarate;
//	unsigned short trxfreq;
//};
struct bsmsg{
    unsigned char flag1;
    unsigned char flag2;
    unsigned char flag3;
    unsigned short bsid;
    unsigned int trxid;
    unsigned short ssid;

    char bsname[10];
    char bsip1[8];
    char bsip2[8];
    unsigned short load1;
    unsigned short load2;
    unsigned short load3;
    unsigned short load4;
    unsigned short load5;
    unsigned short load6;
    unsigned short load7;
    unsigned short load8;
};
#pragma pack()
int main(int argc, char *argv[])  
    {  
        int client_sockfd;  
        int len;  
        struct sockaddr_in remote_addr; //服务器端网络地址结构体  
        int sin_size;

//        struct trxmsg p;
//		p.flag1=0x88;
//		p.flag2=0x88;
//		p.flag3=0x22;
//		p.bsid=1;
//		p.trxid=1;
//		p.ssid=0;
//		strcpy(&(p.trxname),"trx111");
//		strcpy(&(p.trxip),"C0A80105");
//		p.trxport=6;
//		p.trxtxpower=7;
//		p.trxdatarate=8;
//		p.trxfreq=9;
//
//		struct bsmsg p;
//		p.flag1=0x88;
//		p.flag2=0x88;
//		p.flag3=0x21;
//		p.bsid=1;
//		p.trxid=0;
//		p.ssid=0;
//		strcpy(&(p.bsname),"bs00001");
//		strcpy(&(p.bsip1),"C0A80202");
//		strcpy(&(p.bsip2),"C0A802FF");
//	    p.load1=99;
//	    p.load2=81;
//	    p.load3=17;
//	    p.load4=62;
//	    p.load5=51;
//	    p.load6=41;
//	    p.load7=31;
//	    p.load8=12;
//

char p[4]="Base";

		char buf[BUFSIZ];  //数据传送的缓冲区
        //printf("%x,%x,%x,%d,%d,");        
		memset(&remote_addr,0,sizeof(remote_addr)); //数据初始化--清零  
        remote_addr.sin_family=AF_INET; //设置为IP通信  
        remote_addr.sin_addr.s_addr=inet_addr("127.0.0.1");//服务器IP地址  
        remote_addr.sin_port=htons(8080); //服务器端口号  
      
             /*创建客户端套接字--IPv4协议，面向无连接通信，UDP协议*/  
        if((client_sockfd=socket(PF_INET,SOCK_DGRAM,0))<0)  
        {    
            perror("socket");  
            return 1;  
        }  
        //memcpy(buf,"Base");
        memcpy(buf,&p,sizeof(p));  
        printf("sending: '%s'/n",buf);  
        sin_size=sizeof(struct sockaddr_in);  
          
        /*向服务器发送数据包*/  
        if((len=sendto(client_sockfd,buf,sizeof(p),0,(struct sockaddr *)&remote_addr,sizeof(struct sockaddr)))<0)
        {  
            perror("recvfrom");   
            return 1;  
        }  
        close(client_sockfd);  
        return 0;  
    }  

