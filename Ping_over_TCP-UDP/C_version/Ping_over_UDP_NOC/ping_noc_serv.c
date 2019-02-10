/*
 * Copyright (C) 2018 David Carrascal(1);
 * 
 *                    (1) University of Alcala, Spain.
 *                    
 *  
 *  Ping tool over tcp (Server) 
 *    
 *  Usage : ./ping_oc_server <Port>
 *   
 *  For more information you can check: github.com/davidcawork/uah-lrss_/tree/master/Ping_over_TCP-UDP/C_version
 * 
 * 
 */



#include <stdio.h>      /*  for printf() ... */
#include <stdlib.h>     /*  for atoi(), exit(), malloc(), free()*/
#include <sys/socket.h> /*  for socket(), bind()  and connect()  */
#include <sys/types.h>  /*  for socket(), bind()  and connect()  */
#include <string.h>     /*  for memset() +  strlen() */
#include <netinet/in.h> /*  for sockaddr_in and in_addr_t   */
#include <arpa/inet.h>  /*  for htonl, htons, ntohl and ntohs*/
#include <stdbool.h>    /*  for use true/false and type bool */
#include <unistd.h>     /*  for close()     */


#define BUFFER_SIZE 100
#define REPLY "Ping : Reply (0)_______________________________________________\n"



int main(int argc, char * argv []){

    /*  Var.aux */
    in_port_t serv_port;
    int socket_serv, socket_cl;
    struct sockaddr_in server,client;
    socklen_t client_addr_len = sizeof(client);
    struct hostent * resolv;
    char client_name[INET_ADDRSTRLEN];
    char buffer[BUFFER_SIZE];
    ssize_t n_data_rcv, n_data_sent;
    char reply[] = {REPLY};

    /*  ----    Here starts our program     ----  */

    /*  Check arg's   */
    if(argc != 2){
        printf("Error: Usage: %s <port>\n",argv[0]);
        exit(1);
    }else{
        

        /*  Create a stream socket - UDP */
        if((socket_serv = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0){
            printf("Error: cannot create a socket() :L \n");
            exit(1);
        }

        /*     
         *  Let's fill our socket addr with 0, for compatibility (struct sockaddr_in) - (struct sockaddr)
         * 
         *  It'll be better explained in the readme or in the memory, still I don't know what I will do :s
         *
         */

        memset(&server, 0 , sizeof(struct sockaddr_in));
        serv_port = atoi(argv[1]);
        server.sin_family = AF_INET;
        server.sin_port = htons(serv_port); /* To big Endian   */
        server.sin_addr.s_addr = htonl(INADDR_ANY);

        if(bind(socket_serv, (struct sockaddr *)&server,sizeof(struct sockaddr_in))){
            printf("Error: cannot bind to the local addr\n");
            exit(1);
        }

       
        /*  Infinite loop   */
        while(true){

           /*
            * recvfrom: receive a UDP datagram from a client
            */

            bzero(buffer, BUFFER_SIZE);
            n_data_rcv = recvfrom(socket_serv, buffer, BUFFER_SIZE, 0,(struct sockaddr *) &client, &client_addr_len);
            if (n_data_rcv < 0){
                printf("Error: cannot recv data\n");
                exit(1);
            }
            /*
            resolv = gethostbyaddr((const char *)&client.sin_addr.s_addr, sizeof(client.sin_addr.s_addr), AF_INET);
            if (resolv == NULL){
                printf("Error: cannot to get client addr\n");
                exit(1);
            }*/        

            if(inet_ntop(AF_INET,&client.sin_addr.s_addr, client_name, sizeof(client_name)) != NULL){
                printf("Client: %s | Port: %d\n",client_name,ntohs(client.sin_port));
            }else{
                printf("Error: cannot to get client addr\n");
                exit(1);   
            }
            
            /* 
             * sendto: echo the input back to the client 
             */

            n_data_sent = sendto(socket_serv, reply, strlen(reply), 0, (struct sockaddr *) &client, client_addr_len);
            if (n_data_sent < 0){
                printf("Error: cannot recv data\n");
                exit(1);
            }

            //close(socket_cl);
        }
    }

    return 0;
}