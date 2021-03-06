
#include <string>
#include <regex>
#include <iostream>

int main() {
    std::string equation = "x^2+2x-330";
    std::smatch m;

    // Find every match of the 
    while ( std::regex_search( equation, m, std::regex( "[xyz0-9]+" )) ) {
        for ( auto x : m ) 
            std::cout << x << " ";

        std::cout << std::endl;

        equation = m.suffix().str();
    }

    return 0;
}
/*/
// match_results constructor
// - using cmatch, a standard alias of match_results<const char*>
#include <iostream>
#include <regex>
#include <string>

int main ()
{

  std::string test = "subject";
  std::cmatch m;          // default constructor

  std::regex_match ( test.c_str(), m, std::regex("sub(.*)") );

  for (unsigned i=0; i<m.size(); ++i)
    std::cout << "match " << i+1 << ": " << m[i] << std::endl;

  return 0;
}
/**/