#include <queue>
#include <string>

class Equation {

    private:
        double x = 0;
        double y = 0;
        double z = 0;

        std::queue<char> variables;
        std::queue<char> operations;

    public:
        Equation( std::string equation );

        void parseEquation( std::string equation );
        double *walkEquation();

        
};