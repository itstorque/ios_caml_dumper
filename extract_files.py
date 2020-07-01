#!/usr/local/bin/python3

"""
    This program is meant to be run on the output of
    `ls -laR` on the directory /System/Library on iOS.
"""

import sys, getopt

def main(argv):
   inputfile  = ''
   outputfile = ''
   extension  = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:e:",["input=","output=","extension="])
   except getopt.GetoptError:
      print ('extract_files.py -i <inputfile> -o <outputfile> -e <extension>')
      sys.exit(2)
   for opt, arg in opts:
        if opt == '-h':
            print ('extract_files.py -i <inputfile> -o <outputfile> -e <extension>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-e", "--ext", "--extension"):
            extension = arg.split(".")[-1]

   return inputfile, outputfile, extension

if __name__ == "__main__":

    inputfile, outputfile, extension = main(sys.argv[1:])

    extension = '.caml' if extension=="" else "."+extension

    filename = 'ls_System_Library.txt' if inputfile == '' else inputfile

    file = open(filename, 'r')
    count = 0

    contains_caml = False
    directory = None
    files = set()

    output = ""

    while True:
        count += 1
        line = file.readline()

        if directory == None:
            directory = line
        else:
            if extension in line:
                files.add(line.split(" ")[-1])
                contains_caml = True

        if len(line) == 1:
            if contains_caml:
                print(directory[:-1], "->", files)
                output = output + directory[:-1] + " -> " + str(files) + "\n"
            directory = None
            files = set()
            contains_caml = False

        if not line: # EOF on empty line
            break

        # print("Line {}: {}".format(count, line.strip()))

    file.close()

    file = open("output.txt" if outputfile == '' else outputfile, "w")
    file.write("List of .caml files\n\n" + output)
    file.close()
