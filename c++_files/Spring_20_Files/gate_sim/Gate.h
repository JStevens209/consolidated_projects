#ifndef GATE_H
#define GATE_H


#include <iostream>
#include <vector>
#include "Wire.cpp"

using namespace std;

class Wire;

class Gate {
public:

  Gate(Wire *input1 = NULL, Wire *input2 = NULL, Wire *newDrive = NULL, int gateDelay = -1, string gateType = "");
  ~Gate();

  void setInput1(Wire *input);
  void setInput2(Wire *input);

  Wire *getDrive() const;
  Wire *getInput1() const;
  Wire *getInput2() const;
  int getDelay() const;
  string getType() const;

//Logic Functions
  void AND();
  void OR();
  void XOR();
  void NOT();
  void NAND();
  void NOR();
  void XNOR();

//Operator =
  Gate& operator=(const Gate& rhs);


private:
  Wire *in1, *in2;
  Wire *drive;
  int delay;
  string type;


};

#endif