// Name: Joshua Stevens
// Date: Sept 29, 2020
// Purpose: This code was mostly copied from a guide given by the instructor, the purpose is to
// start a server that listens for a client, then once a client sends it data, it modifies the 
// data and echoes it back to the client.

/*Required Headers*/
#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <bitset>
 
int main() {
 
    char str[100];
    int listen_fd, comm_fd;

    struct sockaddr_in servaddr;
    bzero( &servaddr, sizeof( servaddr ));

    listen_fd = socket( AF_INET, SOCK_STREAM, 0 );
 
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htons( INADDR_ANY );
    servaddr.sin_port = htons( 10313 );
 
    bind( listen_fd, ( struct sockaddr * ) &servaddr, sizeof( servaddr ));
    listen( listen_fd, 10 );
 
    while( true ) {
        std::string output;
        std::string input;

        // Accept the next socket connection
        comm_fd = accept( listen_fd, ( struct sockaddr* ) NULL, NULL );

        // Read in input
        bzero( str, 100);
        read( comm_fd, str, 100 );

        // Converts the initial input from ACSII characters to binary
        input = str;
        for( int i = 0; i < input.length(); i++ ){
           output += std::bitset<8>( input[i] ).to_string();
        }
        
        // Log echo to server console
        std::cout << "Echo back - " << output << std::endl;
 
        // Send binary to client
        write( comm_fd, output.c_str(), strlen( output.c_str() ) + 1 );
 
    }
}