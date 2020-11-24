//
#include "notes.h"
#include <iostream>


using namespace std;

template <typename T>
TemplateClass<T>::TemplateClass(T t1, T t2, T t3) { 
    test1 = t1;
    test2 = t2;
    test3 = t3;
}

template <typename T>
void TemplateClass<T>::swap(T &a, T &b) {
        T t = a;
        a = b;
        b = t;
    }

template <typename T>
void TemplateClass<T>::print() {
        cout << test1 << " " << test2 << " " << test3 << endl;
    }