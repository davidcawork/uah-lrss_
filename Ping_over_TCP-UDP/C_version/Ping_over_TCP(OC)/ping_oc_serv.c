/*
 * Copyright (C) 2018 David Carrascal(1);
 * 
 *                    (1) University of Alcala, Spain.
 *                    
 *  
 *  Ping tool over tcp (Client) 
 *    
 *  Usage : ./ping_oc.out <IP/destination> <Port>
 *   
 *  For more information you can check: github.com/davidcawork/uah-lrss_/tree/master/Ping_over_TCP-UDP/C_version
 * 
 * 
 */



#include <stdio.h>      /*  for printf() ... */
#include <stdlib.h>     /*  for atoi(), exit(), malloc(), free()*/
#include <sys/socket.h> /*  for socket(), bind()  and connect()  */
#include <sys/types.h>  /*  for socket(), bind()  and connect()  */
#include <string.h>     /*  for memset()    */
#include <netinet/in.h> /*  for sockaddr_in and in_addr_t   */
#include <arpa/inet.h>  /*  for htonl, htons, ntohl and ntohs*/
#include <stdbool.h>    /*  for use true/false and type bool */
#include <unistd.h>     /*  for close()     */


#define MAX_CONNECTIONS 7
#define BUFFER_SIZE 256
#define REPLY "Ping : Reply (0)\n"

int main(int argc, char * argv []){

    /*  Var.aux */
    in_port_t serv_port;
    int socket_serv, socket_cl;
    struct sockaddr_in server,client;
    socklen_t client_addr_len = sizeof(client);
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
        serv_port = atoi(argv[1]);

        /*  Create a stream socket - TCP */
        if((socket_serv = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0){
            printf("Error: cannot create a socket() :L \n");
            exit(1);
        }

        /*Lenar de ceros*/
        memset(&server, 0 , sizeof(struct sockaddr_in)); /* Explicado en la memoria*/
        server.sin_family = AF_INET;
        server.sin_port = htons(serv_port); /* To big Endian   */
        server.sin_addr.s_addr = htonl(INADDR_ANY);

        if(bind(socket_serv, (struct sockaddr *)&server,sizeof(struct sockaddr_in))){
            printf("Error: cannot bind to the local addr\n");
            exit(1);
        }

        if(listen(socket_serv, MAX_CONNECTIONS ) < 0){
            printf("Error: listen()\n");
            exit(1);
        }

        while(true){
            socket_cl = accept(socket_serv,(struct sockaddr *)&client, &client_addr_len);
            if(socket_cl < 0){
                printf("Error: accept()\n");
            }

            if(inet_ntop(AF_INET,&client.sin_addr.s_addr, client_name, sizeof(client_name)) != NULL){
                printf("Client: %s | Port: %d\n",client_name,ntohs(client.sin_port));
            }else{
             printf("Error: cannot to get client addr\n");   
            }

            n_data_rcv = recv(socket_cl, buffer,BUFFER_SIZE,0);
            if(n_data_rcv < 0){
                printf("Error: recv()\n");
                exit(1);       
            }

            while(n_data_rcv > 0 ){
                n_data_sent = send(socket_cl, reply, strlen(reply), 0);
                if(n_data_sent < 0 ){
                    printf("Error: send()\n");
                    exit(1);
                }

                n_data_rcv = recv(socket_cl, buffer,BUFFER_SIZE,0);
                if(n_data_rcv < 0){
                    printf("Error: recv()\n");
                    exit(1);       
                }
            }

            close(socket_cl);
        }
    }

    return 0;
}