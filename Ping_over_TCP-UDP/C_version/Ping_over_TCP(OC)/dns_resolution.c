/*
 * Copyright (C) 2018 David Carrascal(1);

 *                    (1) GIST, University of Alcala, Spain.
 *                    
 *  To get Ip from host using netdb.h utilities 
 */

#include <stdio.h>      /*  for printf() ... */
#include <stdlib.h>     /*  for atoi(), exit(), malloc(), free()*/
#include <netdb.h>      /*  for gethostby...() and getnet...() and getserver...()   */
#include <sys/socket.h> /*  for socket(), bind()  and connect()  */
#include <sys/types.h>  /*  for socket(), bind()  and connect()  */
#include <netinet/in.h> /*  for sockaddr_in and in_addr_t   */
#include <arpa/inet.h>  /*  for htonl, htons, ntohl and ntohs*/


int main(int argc, char * argv []){

    /*  Var aux */
    struct hostent * aux_host;


    if(argc < 2 || argc >3){        /*Check arg's */
        printf("Bad usage, try: ./%s host_name\n", argv[0]);
        exit(1);
    }else{

        /*  Let's check our host  */;
        aux_host = gethostbyname(argv[1]);
        if((aux_host) == NULL){

           printf("Cannot find Ip\n"); 
           exit(1);

        }else{

            printf("\tHost name: %s\n", aux_host->h_name);
            printf("\tHost alias: %s\n", aux_host->h_aliases[0]);
            printf("\tHost IP: %s\n", inet_ntoa(*((struct in_addr *) aux_host->h_addr_list[0])));  
        }
    }

}