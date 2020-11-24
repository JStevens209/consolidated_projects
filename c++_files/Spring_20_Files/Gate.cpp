#include "Gate.h"


Gate::Gate(Wire *input1, Wire *input2, Wire *newDrive, int gateDelay, string gateType) {
  in1 = new Wire(input1->getName(), input1->getGates(), input1->getCurrValue());
  in2 = new Wire(input2->getName(), input2->getGates(), input2->getCurrValue());
  drive = new Wire(newDrive->getName(), newDrive->getGates(), newDrive->getCurrValue());

  delay = gateDelay;
  type  = gateType;
}

Gate::~Gate() {
  //Deletes the space allocated to the pointers
  delete in1;
  delete in2;
  delete drive;
}

//Mutators
void Gate::setInput1(Wire *input) {
    in1 = input;
}

void Gate::setInput2(Wire *input) {
    in2 = input;
}

//Getters
 Wire* Gate::getDrive() const {
    return drive;
}
Wire* Gate::getInput1() const {
    return in1;
}
Wire* Gate::getInput2() const {
    return in2;
}
int Gate::getDelay() const {
    return delay;
}
string Gate::getType() const {
    return type;
}


/*LOGIC GATES*/

void Gate::AND() {
    if((in1->getCurrValue() == 1) && (in2->getCurrValue() == 1)){
        drive->setCurrValue(1);
    }
    else {
        drive->setCurrValue(0);
    }
}
  void Gate::OR() {
      if((in1->getCurrValue() == 1) || (in2->getCurrValue() == 1)) {
          drive->setCurrValue(1);
      }
      else {
          drive->setCurrValue(0);
      }
  }

  //unsure of what behavior should be when one input == X
  void Gate::XOR() {
      //Handles undefined behavior by setting output to undefined if either input is undefined
      if((in1->getCurrValue() == -1) || (in2->getCurrValue() == -1)) {
          drive->setCurrValue(-1);
          return;
      }
      //if input 1 is on XOR input 2 is on, set drive to on
      if((in1->getCurrValue() == 1) != (in2->getCurrValue() == 1)) {
          drive->setCurrValue(1);
      }
      else {
          drive->setCurrValue(0);
      }
  }

  void Gate::NOT() {
      //if input is on, turn it off, and reverse
      if(in1->getCurrValue() == 1) {
          drive->setCurrValue(0);
      }
      else if(in1->getCurrValue() == 0) {
          drive->setCurrValue(1);
      }
  }
  //ANDS, then NOTS
  void Gate::NAND() {
      AND();
      NOT();
  }
  void Gate::NOR() {
      OR();
      NOT();

  }
  void Gate::XNOR(){
      XOR();
      NOT();
  }

//Operator =
 Gate::Gate& Gate::operator=(const Gate& rhs) {
     delay = rhs.delay;
     type = rhs.type;

    in1 = new Wire;
    in2 = new Wire;
    drive = new Wire;
    *in1 = *rhs.in1;
    *in2 = *rhs.in2;
    *drive = *rhs.drive;

    return *this;
 }