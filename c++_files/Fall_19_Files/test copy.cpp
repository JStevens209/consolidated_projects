#include <iostream>

using namespace std;

class ThreeDPoint{
public:
  ThreeDPoint(double x = 0, double y = 0, double z = 0);
/*  ThreeDPoint(double xx, double yy, double zz) {
    x = xx;
    y = yy;
    z = zz;
  }*/

private:
  double x,y,z;

};

int main(){

  double x,y,z;
  ThreeDPoint orderedPair(x,y,z);



  return 0;
}
