#include <vector>
#include <iostream>

using namespace std;


int main(){

  const int SIZE = 3;
  vector<int> va(SIZE),vb;



  va.at(0)= 1;
  va.at(1) = 2;
  va.at(2) = 3;

  vb = va;
  vb.push_back(4);
  //cout << vb.back();
  vb.pop_back();
  //cout << vb.back();

  //ranged based for loop, to edit the vector itself, pass it by reference through
  //the variable; ex. for(int &testVar:testVector)
  for(auto test:vb){
    cout << test << endl;
  }

/*  cout << vb.at(0); //makes certain the requested value is in the range.
  cout << vb[1]; //does not do that ^
  cout << vb.at(2);
  cout << vb.at(3);*/

}
