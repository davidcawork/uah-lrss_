/*
 * Copyright (C) 2018 David Carrascal(1);

 *                    (1) GIST, University of Alcala, Spain.
 *                    
 *  Ping tool over tcp 
 */

#include <stdio.h>      /*  for printf() ... */
#include <stdlib.h>     /*  for atoi(), exit(), malloc(), free()*/
#include <netdb.h>      /*  for gethostby...() and getnet...() and getserver...()   */
#include <sys/socket.h> /*  for socket(), bind()  and connect()  */
#include <sys/types.h>  /*  for socket(), bind()  and connect()  */
#include <netinet/in.h> /*  for sockaddr_in and in_addr_t   */
#include <arpa/inet.h>  /*  for htonl, htons, ntohl and ntohs*/
#include <time.h>       /*  for clock() */
#include <signal.h>     /*  To  handle CTRL+C signal(sigint)    */
#include <stdbool.h>    /*  for use true/false and type bool */
#include <string.h>     /*  for memset()    */

#define BUFFER_SIZE 256
#define INTERVAL_REQUEST 2000 /* units: ms (2s) */

typedef struct ping{

    char * server_name;
    char * port;
    int socket;
    struct sockaddr_in server;
    char buffer[BUFFER_SIZE];
    int pings_sended;
    int data_send, data_recv; //Units : bytes
    struct hostent * resolv;
    
} ping_t;

volatile bool shouldKeep_pinging = true;

void CTRLDhandler(int a){
    shouldKeep_pinging = false;
}

/*  Usage : ./a.out IP/destination Port */

int main(int argc, char * argv []){

    /*  Var.aux */
    ping_t pet_ping;
    char ping_request[]= {"Ping : Request (8)"};
    int timer_ms = 0;

    /* Prepare CTRL+C exit */
    if(signal(SIGINT, &CTRLDhandler) == SIG_ERR){
        printf("Error: cannot set signal handler\n");
        exit(1);
    }

    /*  Check arg's   */
    if(argc < 3){
        printf("Error, usage: %s destination port\n",argv[0]);
        exit(1);
    }else{

        /*  DNS query */
        pet_ping.resolv = gethostbyname(argv[1]);
        if((pet_ping.resolv) == NULL){
           printf("Cannot find Ip\n"); 
           exit(1);
        }else{  

            pet_ping.pings_sended = 0;
            pet_ping.data_send = 0;
            pet_ping.data_recv = 0;
            pet_ping.server_name = pet_ping.resolv->h_addr_list[0];
            pet_ping.port = argv[2];

            /*Lenar de ceros*/
            memset(&pet_ping.server, 0 , sizeof(struct sockaddr_in)); /* Explicado en la memoria*/
            pet_ping.server.sin_family = AF_INET;
            pet_ping.server.sin_port = htons(atoi(pet_ping.port)); /* To big Endian   */

            if(inet_pton(AF_INET, pet_ping.server_name, &pet_ping.server.sin_addr.s_addr)){
                printf("Error: cannot convert Ip/destination into a 32-bit binary repr\n");
                exit(1);
            }

            /*  Create a stream socket - TCP */
            if((pet_ping.socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0){
                printf("Error: cannot create a socket() :L \n");
                exit(1);
            }

            /*  Connect to server   */
            if( connect(pet_ping.socket, (struct sockaddr *)&pet_ping.server,sizeof(struct sockaddr_in)) < 0){
                printf("Error: cannot Connect to server :L \n");
                exit(1);
            }

            while(shouldKeep_pinging){
                //Send_ping(&pet_ping, ping_request, );
            }

            printf("\n\n\nEstadisticas de ping\n");
        }

       
    }
}