from PIL import Image as img
import stepic as steg
import sys

class Steganography:

    def __init__( self ):
        self.arguments = sys.argv
        flag = self.arguments[1]

        # If user is trying to encrypt and has 5 or greater args, then assign imagePath and outputPath.
        if len( self.arguments ) >= 4 and flag == "-e":

            self.imagePath = self.arguments[2]
            self.outputPath = self.arguments[3]

        # If the user is trying to decrypt and has 4 args, then only assign the imagePath.
        elif len( self.arguments ) >= 3 and flag == "-d":    
            self.imagePath = self.arguments[2]

        # If none of the previous criteria were met, something is wrong with the format, exit and print error.
        else:
            sys.exit( "Error Missing Arguments: steg <-e/-d> <Input Filepath> <Output Filepath> [Input/Output Textfile]" )
        
        # If the user included an input text file for encrypting, get the text from it.
        if len( self.arguments ) == 5 and flag == "-e":

            fin = open( self.arguments[4], 'r')

            if fin.readable():
                self.text = fin.read()
            else:
                sys.exit( "Error: Unable to Open Text File." )

            fin.close()

        # If the user included a filepath to output decrypted text to, set the text flag to True
        # This is a questionable design choice most likely, but its what makes the most sense.
        # If the decrypt function is called, it assumes that either self.text was set to a boolean,
        # or that the user has not specified a text file to output to.
        elif len( self.arguments ) == 4 and flag == "-d":
            self.text = True

        # If none of the previous criteria were met, the user has not specified a text file for I/O.
        # The reason I just ignore this case and just dont declare self.text is because there needs to be a way
        # to tell if the program previously reached this state without having to test for it again, this is the
        # most elegant solution to this problem.
        else:
            self.text = ""

    def encrypt( self ):

        # If self.text is an empty string, read input from stdin
        if not self.text:
            self.text = input()

        # Converts the ACSII text to a decimal array
        decList = []
        for char in self.text:
            decList.append( ord( char ) )

        # Encodes the data in the image
        fin = img.open( self.imagePath )

        encoding = steg.encode( fin, decList )
        encoding.save( self.outputPath )

        fin.close()
        
    def decrypt( self ):

        fout = img.open( self.imagePath )

        decoding = steg.decode( fout )
        
        # Checks if self.flag is "equivalent to" the keyword True, if it is,
        # then output to the user given filepath. Otherwise, just print it to stdout
        if self.text is True:

            fin = open( self.arguments[3], 'a+' )
            fin.write( decoding )
            fin.close()

        else:
            print( decoding )
    
        fout.close()

    def start( self ):

        flag = self.arguments[1]
    
        if flag == "-e":
            self.encrypt()
        
        elif flag == "-d":
            self.decrypt()

        else:
            print( "Proper use of 'steg' is: steg <-e/-d> <Input Filepath> <Output Filepath> [Input/Output Textfile]" )

            
if __name__ == "__main__":

    stego = Steganography()
    stego.start()
