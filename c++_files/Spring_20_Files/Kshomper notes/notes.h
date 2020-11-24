using namespace std;

//scope resolution in a .cpp file looks like TemplateClass<T>::TemplateClass(...){...}
template <typename T>
class TemplateClass {
public:

    TemplateClass(T t1, T t2, T t3);

    void swap(T &a, T &b);
    void print();

private:
    T test1; 
    T test2; 
    T test3;  

};