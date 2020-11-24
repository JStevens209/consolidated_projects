#include <iostream>
#include <math.h>

#define PI 3.14159265


using namespace std;

int main(){

  double answer;
  double n = 10000.0;
  int count = 0;

  for(double i = 0; i < (PI/2.0); i += ((PI/2.0) * (1.0/n))) {

    if(((count % 2) == 0) && (count != 0)) {
      answer += (2 * sin(i));
    }
    else {
      answer += (4 * sin(i));
    }

    count++;
    //cout << i << " " << answer << endl;
  }

  answer += sin(PI/2.0);
  answer *= (((PI/2.0) * (1.0/n)) / 3);

  cout << answer << endl;

}
