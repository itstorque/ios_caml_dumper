#!/usr/local/bin/python3
"""
    This program is meant to be run on the output of
    `ls -laR` on the directory /System/Library on iOS.
"""

import sys, getopt
from random import sample

def main(argv):
   inputfile  = ''
   outputfile = ''
   extension  = ''
   port = ''
   user_and_host = ''
   script_file = ''

   try:
      opts, args = getopt.getopt(argv,"hi:o:e:p:u:",["input=","output=","extension=","port=","user_and_host="])

   except getopt.GetoptError:
      print ('extract_files.py -i <inputfile> -o <outputfile> -e <extension> -s <script_file> -p <port> -u <user_and_host>')
      sys.exit(2)

   for opt, arg in opts:

        if opt == '-h':
            print ('extract_files.py -i <inputfile> -o <outputfile> -e <extension> -s <script_file> -p <port> -u <user_and_host>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-e", "--ext", "--extension"):
            extension = arg.split(".")[-1]
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-u", "--user_and_host", "-h", "--host"):
            user_and_host = arg
        elif opt in ("-s", "--script_file", "--script"):
            script_file = arg

   return inputfile, outputfile, extension, port, user_and_host

if __name__ == "__main__":

    inputfile, outputfile, extension, port, user_and_host = main(sys.argv[1:])

    extension = '.caml' if extension=="" else "."+extension

    filename = 'ls_System_Library.txt' if inputfile == '' else inputfile

    file = open(filename, 'r')
    count = 0

    contains_caml = False
    directory = None
    directories = set()
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
                directories.add(directory[2:-2])
                output = output + directory[:-2] + "/ -> " + str(files) + "\n"
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

    file = open("scp_command.sh" if script_file == '' else script_file, "w")

	# add a check to see if directory is empty
    scp_command = """if [ "$(ls -A ./)" ]; then \n
		echo "This directory is not empty..."
	else
		"""

	# use this block if the length of the command is too long to send
	# over, however it should be fine in most cases...

    # while len(directories) > 0:
	#
    #     dir_subset = set(sample(directories, min(40, len(directories))))
	#
    #     directories -= dir_subset
	#
    #     scp_command += "scp -r -P " + \
	# 		str(port if port else 2022) + " " + \
	# 		str(user_and_host if user_and_host else "root@localhost") + \
	# 		":/System/Library/\{"
	#
    #     # triple escape in command line because it is being sent to the remote and
	# 	# needs to be escaped there, double that to escape in python string i.e.
	# 	# 6 backslashes in total :)
    #     scp_command += '/*.caml,'.join(dir_subset).replace(" ", "\\\\\\ ")
	#
    #     scp_command += "/*.caml\} ./\n"

    scp_command += "scp -r -P " + \
        str(port if port else 2022) + " " + \
        str(user_and_host if user_and_host else "root@localhost") + \
        ":/System/Library/\{"

    scp_command += ','.join(directories).replace(" ", "\\\\\\ ")

    scp_command += "\} ./\n"

    scp_command += "find ./ -maxdepth 10 -type f ! -name \"*.caml\" -delete \n"

    scp_command += "find ./ -type d -empty -delete \n"

    scp_command += "\nfi"

    file.write("#!/bin/bash\n\n"+scp_command)
    file.close()
