#include <curses.h>
#include <stdlib.h>
#include <math.h>
#include <vector>
#include <string>

#include "vector_math.cpp"

int main() {

    initscr();
    cbreak();
    noecho();

    clear();

    double x = 0;
    double y = 0;
    double z = 0;

    double cam_x = 20;
    double cam_y = 20;
    double cam_z = 20;

    int camera_plane_x = 0;
    int camera_plane_y = 0;

    int camera_origin_x = COLS / 2;
    int camera_origin_y = LINES / 2;

    int maxlines = LINES - 1;
    int maxcols = COLS - 1;

    int maxsize = std::min( maxlines, maxcols );

    std::vector<double> camera_vector = { cam_x, cam_y, cam_z };

    std::vector<double> test_vector = { x, y, z };

    for( int i = 0; i < COLS; i++ ) {
        for( int k = 0; k < LINES; k++ ) {

            camera_plane_x = i - camera_origin_x;
            camera_plane_y = k - camera_origin_y;

            if( camera_origin_x > 0 ) {
                mvaddch( camera_plane_y, camera_plane_x, '-' );
            }

        }
    } 

    refresh();

    getch();
    endwin();
    
    exit(0);
}

