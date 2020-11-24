This program was created by Joshua Stevens.

Use:
    steg.exe -e <input filepath> <output filepath> [input text filepath]
    steg.exe -d <input filepath> [output text filepath]

    Flags:
        -e: Encrypt using input filepath, output png to output filepath
        -d: Decrypt using input filepath, does not use output filepath

    input filepath: A filepath to a valid png/bmp file.
    output filepath: The filepath to where the encrypted png/bmp file should be created.
    input/output text file: If this file path is provided the program will either read data from it for encryption, or write data to it for decryption
                            if this file is not specified for encryption, program will expect user input after running command.


Example:

    steg.exe -e ./examples/test.png ./output.png ./examples/test_input.txt
    steg.exe -d ./output.png


This program should not need any external dependencies, if it does, I gave you the wrong .exe on accident.