
//Throws errors about incomplete type gate, tried talking to lab assistant, he didnt have any idea either. I worked for several hours trying to fix it.
//Not quite sure why it happens or what is causing it to happen, ran out of time to turn it in.
#include "Wire.h"


using namespace std;


//Constructor
Wire::Wire(string wireName, vector<Gate *> wireGates, int value) {
    name = wireName;
    currValue = value;

    //Sets the gates array to the wireGates array without aliasing
    for(int i = 1; i < wireGates.size(); i++) {
      if(wireGates.at(i) != NULL){
        gates.at(i) = new Gate(wireGates.at(i)->getInput1(), wireGates.at(i)->getInput2(), wireGates.at(i)->getDrive(), wireGates.at(i)->getDelay(), wireGates.at(i)->getType());
        //*gates.at(i) = *wireGates.at(i);
      }
    }
}

//Destructor
Wire::~Wire(){

  for(int i = 0; i < gates.size(); i++) {
    delete gates.at(i);
  }
}

//Getters
string Wire::getName() const {
  return name;
}

vector<Gate*> Wire::getGates() const {
  return gates;
}

int Wire:: getCurrValue() const {
  return currValue;
}


//Mutators
void Wire::addGate(Gate *newGate) {
  gates.push_back(newGate);
}

void Wire::setCurrValue(int newValue) {
  currValue = newValue;
}

//Operator =
Wire& Wire::operator=(const Wire& rhs) {

     name = rhs.name;
     currValue = rhs.currValue;
    
    for(int i = 0; i < rhs.gates.size(); i++) {
        gates.at(i) = new Gate;
        *gates.at(i) = *rhs.gates.at(i);
    }

    return *this;

 }

