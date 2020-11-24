#include <iostream>
#include <math.h>

#define PI 3.14159265


using namespace std;

int main(){

  double answer;
  double n = 100.0;

  for(double i = 0; i < (PI/2.0); i += ((PI/2.0) * (1.0/n))) {
    answer += sin(i);

    //cout << i << " " << answer << endl;
  }

  answer += sin(PI/2.0);
  answer *= ((PI/2.0) * (1.0/n));

  cout << answer << endl;

}
