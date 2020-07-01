# List CAML files in directory
This is a script that extracts certain file types from a directory.

[output.txt](output.txt) contains the list of CAML files in /System/Library on an iOS 13.5 device, this should help locate CAML resources for glyphs.

## Usage

`extract_files.py -i <inputfile> -o <outputfile> -e <extension>`

The default values are:

`inputfile  = 'ls_System_Library.txt'`

`outputfile = 'output.txt'`

`extension  = 'caml'`
