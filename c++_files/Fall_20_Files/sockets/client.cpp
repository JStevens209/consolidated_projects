// Name: Joshua Stevens
// Date: Sept 29, 2020
// Purpose: This code was mostly copied from a guide given by the instructor, the purpose is to
// run a client that sends data to the server, then print the data that it recieves back.

#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
 
int main( int argc, char **argv )
{
    // Error Checking for cases of no command line arguments passed
    // If there is only 1 argument, then no data was provided.
    if( argc < 2 ) {
        std::cout << "ERROR: Not enough arguments." << std::endl;
        return 1;
    }
    
    int sockfd, n;
    char recvline[100];
    struct sockaddr_in servaddr;
 
    sockfd = socket( AF_INET,SOCK_STREAM, 0 );
    bzero( &servaddr, sizeof servaddr) ;
 
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons( 10313 );
 
    inet_pton(AF_INET,"127.0.0.1",&( servaddr.sin_addr ));
    connect( sockfd, ( struct sockaddr *) &servaddr, sizeof( servaddr ));
 
    // Sets both and recvline to all zeroes
    bzero( recvline, 100 );
    // Writes the data to the server
    write( sockfd, argv[1], strlen( argv[1] ) + 1 );
    // Reads the data sent from the server into recvline
    read( sockfd, recvline, 100 );
    printf( "%s", recvline );
    
}