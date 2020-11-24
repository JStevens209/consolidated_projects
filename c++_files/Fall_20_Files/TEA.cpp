#include <iostream>
#include <vector>
#include <fstream>
#include <bitset>
#include <iomanip>
#include <sstream>
#include <vector>
#include <stdint.h>

using namespace std;


string strr;

//INPUT FUNCTIONS

// Takes in 2 int32 values and a filename, changes the 2 int32 values to represent the first 16 hex chars in the file
void readHexFile( ifstream &fin, uint32_t &left, uint32_t &right ){

    string hexString;
    string temp;
    
    // Gets 16 Hex Characters from the file, if there are none left, use zeros instead
    for( int i = 0; i < 16; i++ ){
        if( !fin.eof() ){
            temp = fin.get();
            hexString.append( temp );
        }
        else if( fin.eof() ){
            hexString.append( "0" );
        }
    }


    // Splits the hexString into a left and right half, and convert it to decimal
    stringstream ss;
    ss << std::hex << hexString.substr( 0, 8 );
    ss >> left;

    stringstream sss;
    sss << std::hex << hexString.substr( 8, 8 );
    sss >> right;    

    // Returns two 32 bit integers
    return;
}


// Takes in two int32 values and a filename, changes the int32 values to represent the first 8 ACSII chars of the file
void readStringFile( ifstream &fin, uint32_t &left, uint32_t &right){

    string fileString;
    string temp;

    // Reads in 32-bits of the file, if no bits are left, read in spaces
    for( int i = 0; i < 8; i++ ){
        if( !fin.eof() ){
            temp = fin.get();
            fileString.append( temp );
        }
        else if( fin.eof() ){
            fileString.append( " " );
        }
    }


    //Converts the ACSII characters to binary, then to a string
    string leftBinaryVal;
    string rightBinaryVal;
    for( int i = 0; i < fileString.length() / 2; i++ ){

        // Using bitset was the only way I could think of creating a reversible 32 bit integer out of ACSII characters
        leftBinaryVal  += bitset<8>( fileString.substr(0, 4)[i] ).to_string();
        rightBinaryVal += bitset<8>( fileString.substr(4, 4)[i] ).to_string();
    }

    // Converts the binary strings to uint32_t
    left  = bitset<32>(leftBinaryVal).to_ulong();
    right = bitset<32>(rightBinaryVal).to_ulong();

    return;
}

// Reads the key into a uint32_t vector and returns the uint32_t vector
vector<uint32_t> getKeyArray( ifstream &fin, bool isIV = false ) {

    vector<uint32_t> decKeyArr;
    string keyString;

    // Gets the key as a string
    getline( fin, keyString );

    // Splits the string into 4 substrings and calls string to long on each substr
    decKeyArr.push_back( (uint32_t)stoll( keyString.substr( 0, 8 ), nullptr, 16 ) );
    decKeyArr.push_back( (uint32_t)stoll( keyString.substr( 8, 8 ), nullptr, 16 ) );
    // If the function is parsing an IV file, just get 64 bits
    if( !isIV ){
        decKeyArr.push_back( (uint32_t)stoll( keyString.substr( 16, 8 ), nullptr, 16 ) );
        decKeyArr.push_back( (uint32_t)stoll( keyString.substr( 24, 8 ), nullptr, 16 ) );
    }

    return decKeyArr;
}



// OUTPUT FUNCTIONS //
void outputHexText( const uint32_t left, const uint32_t right ){
    ofstream fout;
    fout.open( "/Users/joshua/Documents/output.txt" );

    cout << hex << (uint32_t)left << (uint32_t)right << dec;

    fout.close();
    return;
}

void outputStringText( const uint32_t left, const uint32_t right ){

    // Turns the integers back into binary strings
    string binaryString = bitset<32>( (uint32_t)left ).to_string(); 
    binaryString += bitset<32>( (uint32_t)right ).to_string();

    stringstream sstream( binaryString );

    // Converts the binary to ACSII text and prints it
    while( !sstream.eof() ){
        bitset<8> bits;
        sstream >> bits;

        strr += char( bits.to_ulong() );
    }

    return;
}


/*
 Description: encrypts the left and right variable with the TEA algorithm

 @param key, ALWAYS 128 bit key, vector size 4
 @param l  plaintext left  --> ciphertext left  , passed by reference
 @param r plaintext right --> ciphertext right , passed by reference
 */
vector<uint32_t> teaEncrypt(const vector<uint32_t> KEY, uint32_t l, uint32_t r) {
    vector<uint32_t> text;
    uint32_t left = l;
    uint32_t right = r;
    uint32_t const DELTA = 0x9e3779b9;
    uint32_t sum = 0;
    for (int i = 0; i < 32; i++) {
        sum += DELTA;
        left  = left  + (((right << 4) + KEY[0]) ^ (right + sum) ^ ((right >> 5) + KEY[1]));
        right = right + (((left  << 4) + KEY[2]) ^ (left  + sum) ^ ((left  >> 5) + KEY[3]));
    }
    text.push_back(left);
    text.push_back(right);
    return text;

}

/*
 Description: decrypts the left and right variable with the TEA algorithm

 @param key, ALWAYS 128 bit key, vector size 4
 @param l ciphertext left --> plaintext left
 @param r ciphertext right --> plaintext right
 */
vector<uint32_t> teaDecrypt(const vector<uint32_t> KEY, uint32_t l, uint32_t r) {
    vector<uint32_t> text;
    uint32_t left = l;
    uint32_t right = r;
    int const DELTA = 0x9e3779b9;
    int sum = DELTA << 5;
    for (int i = 0; i < 32; i++) {
        right = right - (((left  << 4) + KEY[2]) ^ (left  + sum) ^ ((left  >> 5) + KEY[3]));
        left  = left  - (((right << 4) + KEY[0]) ^ (right + sum) ^ ((right >> 5) + KEY[1]));
        sum -= DELTA;
    }
    text.push_back(left);
    text.push_back(right);
    return text;
}

/*
Description: CBC mode encryption
Blocks are chained together
Random initialization vector, IV, is required, but not secret, 64 bits of hex, vector contains L @ index 0 and R @ index 1
@param plaintext vector of (left , right)'s 
@return the Ciphertext in a vector of (left, right)'s
*/
vector<vector<uint32_t> > CBCEncrypt(const vector<uint32_t> KEY, vector<vector<uint32_t> > plaintext, const vector<uint32_t> IV) {
    vector<vector<uint32_t> > Ciphertext;
    
    // take care of index 0 because it uses IV
    Ciphertext.push_back(teaEncrypt(KEY, ( IV[0] ^ plaintext[0][0] ), ( IV[1] ^ plaintext[0][1] )));

    //take care of the rest
    for (int i = 1; i < plaintext.size(); i++) {
        Ciphertext.push_back(teaEncrypt(KEY, ( Ciphertext[i - 1][0] ^ plaintext[i][0] ), ( Ciphertext[i - 1][1] ^ plaintext[i][1] )));
    }

    return Ciphertext;
}


/*
Description: CBC mode decryption
Blocks are chained together
Random initialization vector, IV, is required, but not secret, 64 bits of hex, vector contains L @ index 0 and R @ index 1
@param ciphertext in a vector of (left, right)'s
@return the Plaintext vector of (left , right)'s
*/
vector<vector<uint32_t> > CBCDecrypt(const vector<uint32_t> KEY, vector<vector<uint32_t> > ciphertext, const vector<uint32_t> IV) {
    vector<vector<uint32_t> > Plaintext;

    // take care of index 0 because it uses IV
    {
        vector<uint32_t> temp = teaDecrypt(KEY, ciphertext[0][0], ciphertext[0][1]);
        vector<uint32_t> ttemp;
        ttemp.push_back(IV[0] ^ temp[0]);
        ttemp.push_back(IV[1] ^ temp[1]);
        Plaintext.push_back(ttemp);
    }

    //take care of the rest
    for (int i = 1; i < ciphertext.size(); i++) {

        vector<uint32_t> temp = teaDecrypt(KEY, ciphertext[i][0], ciphertext[i][1]);
        vector<uint32_t> ttemp;
        ttemp.push_back(ciphertext[i - 1 ][0] ^ temp[0]);
        ttemp.push_back(ciphertext[i - 1 ][1] ^ temp[1]);
        Plaintext.push_back(ttemp);
    }

    return Plaintext;
}

/*
Description: CTR mode decryption
Use a block cipher like a stream cipher
Random initialization vector, IV, is required, but not secret, 64 bits of hex, vector contains L @ index 0 and R @ index 1
@param ciphertext vector of (left , right)'s
@return the Plaintext in a vector of (left, right)'s
*/
vector<vector<uint32_t> > CTREncrypt(const vector<uint32_t> KEY, vector<vector<uint32_t> > ciphertext, const vector<uint32_t> IV) {
    vector<vector<uint32_t> > Plaintext;

    // IVRight Overflow Counter
    int OCntr = 0; 

    //set to smallest uint32_t value
    uint32_t temp = UINT32_MAX + 1; 

    for (int i = 0; i < ciphertext.size(); i++) {
        uint32_t IVLeft = IV[0];
        uint32_t IVRight = IV[1];
        uint32_t IVRightCheck = IVRight + i;

        // if IVRightCheck's previous value is less than IVRightCheck (meaning it overflowed during this current loop)
        if (temp > IVRightCheck) {
            // increment Overflow Counter
            OCntr++; 
        }

        // update temp
        temp = IVRightCheck; 
        
        vector<uint32_t> temp = teaEncrypt(KEY, IVLeft + OCntr, IVRightCheck);  // E(K, IV + i)
        vector<uint32_t> ttemp;
        ttemp.push_back(ciphertext[i][0] ^ temp[0]);  // C[i][0] ^ E[0]      -- Left
        ttemp.push_back(ciphertext[i][1] ^ temp[1]);  // C[i][1] ^ E[1]      -- Right
        Plaintext.push_back(ttemp); //(L,R) goes to index i of Plaintext
    }

    return Plaintext;
}

vector<vector<uint32_t> > EBCDecrypt( const vector<uint32_t> KEY, vector<vector<uint32_t> > ciphertext ) {
    vector<vector<uint32_t> > Plaintext;

    for( int i = 0; i < ciphertext.size(); i++ ){
        Plaintext.push_back( teaDecrypt( KEY, ciphertext[i][0], ciphertext[i][1] ));
    }

    return Plaintext;
}


vector<vector<uint32_t> > EBCEncrypt( const vector<uint32_t> KEY, vector<vector<uint32_t> > ciphertext ) {
    vector<vector<uint32_t> > Plaintext;

    for( int i = 0; i < ciphertext.size(); i++ ){
        Plaintext.push_back( teaEncrypt( KEY, ciphertext[i][0], ciphertext[i][1] ));
    }

    return Plaintext;
}


int main( int argc, char **argv ) {

    if( argc < 3 ){
        cout << "ERROR: Too few command line arguments" << endl;
        return 1;
    }

    string filePath = argv[1];
    ifstream plainFin;
    plainFin.open( filePath );

    // Check if file exists
    if( !plainFin.is_open() ){
        cout << "ERROR: file " <<  filePath << " does not Exist" << endl;
        return 1;
    }

    int periodIndex = filePath.find_last_of( '.' );
    int dashIndex = filePath.find_last_of( '-');

    bool isHex = true;
    bool isEncrypting = true;
    int mode = 0;

    // Sets wether or not the file is written in Hex
    if( filePath[ periodIndex - 1 ] == 'S' ){
        isHex = false;
    }

    // Sets wether the file is going to be decrypted, or encrypted
    if( filePath[ periodIndex + 1 ] == 'c' ){
        isEncrypting = false;
    }

    // Sets the mode, default is EBC, or mode 0
    if( filePath.substr((dashIndex - 3), 3) == "CBC" ) {
        mode = 1;
    }
    else if( filePath.substr((dashIndex - 3), 3) == "CTR" ) {
        mode = 2;
    }

    // Opens the key file
    string keyPath = argv[2];
    ifstream keyFin;
    keyFin.open( keyPath );

    if( !keyFin.is_open() ){
        cout << "ERROR: The file " << keyPath << " does not exist" << endl;
        return 1;
    }

    if( ( mode == 1 || mode == 2 ) && ( argc < 4 )){
        cout << "ERROR: Not enough command line arguments" << endl;
        return 1;
    }

    string IVPath = argv[3];
    ifstream IVFin;
    IVFin.open( IVPath );

    if( !IVFin.is_open() ){
        cout << "ERROR: The file " << IVPath << " does not exist." << endl;
        return 1;
    }

    uint32_t left, right;
    vector<uint32_t> key = getKeyArray( keyFin );
    vector<uint32_t> IV = getKeyArray( IVFin, true );
    vector<vector<uint32_t> > leftAndRight;

    // Read File loop
    while( !plainFin.eof() ){

        if( isHex ){
            readHexFile( plainFin, left, right );
        }
        else {
            readStringFile( plainFin, left, right );
        }

        vector<uint32_t> temp;
        temp.push_back( left );
        temp.push_back( right );
        leftAndRight.push_back( temp );
    }
    if( isEncrypting && mode == 0 ){
        leftAndRight = EBCEncrypt( key, leftAndRight );
    }
    else if( mode == 0 ){
        leftAndRight = EBCDecrypt( key, leftAndRight );
    }
    
    if( isEncrypting && mode == 1 ){
        leftAndRight = CBCEncrypt( key, leftAndRight, IV );
    }
    else if( mode == 1 ){
        leftAndRight = CBCDecrypt( key, leftAndRight, IV );
    }

    if( mode == 2 ){
        leftAndRight = CTREncrypt( key, leftAndRight, IV);
    }

    for( int i = 0; i < leftAndRight.size(); i++ ){
        if( isHex ){
            outputHexText( leftAndRight[i][0], leftAndRight[i][1] );
        }

        if( !isHex ){
            outputStringText( leftAndRight[i][0], leftAndRight[i][1] );
        }
    }

    ofstream fout( "/Users/joshua/Documents/output.txt" );
    fout << strr;
    fout.close();

    cout << strr;

}

//CMD Line ARGS, prob gonna forget to delete this
// "/Users/joshua/Documents/mystery1_ECB-H.p"  "/Users/joshua/Documents/teacher-H.key" "/Users/joshua/Documents/teacher-H.iv"
// "/Users/joshua/Documents/mystery2_ECB-S.crypt"  "/Users/joshua/Documents/teacher-H.key" "/Users/joshua/Documents/teacher-H.iv"
// "/Users/joshua/Documents/mystery3_CBC-S.plain" "/Users/joshua/Documents/teacher-H.key" "/Users/joshua/Documents/teacher-H.iv"
// "/Users/joshua/Documents/mystery4_CTR-S.crypt" "/Users/joshua/Documents/teacher-H.key" "/Users/joshua/Documents/teacher-H.iv"


// /Users/joshua/Documents/practice_ECB-S.plain "/Users/joshua/Documents/theme-H.key" "/Users/joshua/Documents/theme-H.iv"   

