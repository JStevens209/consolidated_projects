#include <curses.h>
#include <stdlib.h>
#include <math.h>
#include <vector>

#include <string>

//#include "vector_math.cpp"

int main() {

    initscr();
    cbreak();
    noecho();

    clear();

    double x = 0;
    double y = 0;
    double z = 0;

    double cam_x = 10;
    double cam_y = 10;
    double cam_z = 10;

    int camera_plane_x = 0;
    int camera_plane_y = 0;
/*
    int camera_origin_x = COLS / 2;
    int camera_origin_y = LINES / 2;

    int maxlines = LINES - 1;
    int maxcols = COLS - 1;

    int maxsize = std::min( maxlines, maxcols );

    std::vector<double> camera_vector = { cam_x, cam_y, cam_z };

    for( int i = 0; i < COLS; i++ ) {
        for( int k = 0; k < LINES; k++ ) {
            camera_plane_x = k - camera_origin_x;
            camera_plane_y = i - camera_origin_y;

            if( camera_plane_y < 1 ) {
                mvaddch( i, k, '-' );

            }

        }
    } 
*/
    
    mvaddstr( 100, 10, std::to_string(COLS).c_str() );

    refresh();

    getch();
    endwin();
    
    exit(0);
}

