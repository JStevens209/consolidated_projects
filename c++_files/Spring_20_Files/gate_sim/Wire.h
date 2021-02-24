#ifndef WIRE_H
#define  WIRE_H

#include <iostream>
#include <vector>


class Gate;

using namespace std;

class Wire {
public:
//constructor

  Wire(string wireName = "", vector<Gate *> wireGate = {NULL}, int value = -1);
//destructor
  ~Wire();

//Getters
  string getName() const;
  vector<Gate*> getGates() const;
  int  getCurrValue() const;

//Setters
  void addGate(Gate *newGate);
  void setCurrValue(int newValue);

//Operator =
  Wire& operator=(const Wire& rhs);

private:
  string name;
  vector<Gate *> gates;
  int currValue;
  const int X = -1;
};

#endif