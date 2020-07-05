# CAML filedump from iOS 13.5

**NOTE**: None of the files in the directory [ios-13.5-glyphs](ios-13.5-glyphs)
are created/owned by the author of this repo, they are simply a copy of some
files found in iOS's `/System/Library/` directory.

[extract_files.py](extract_files.py) is a script that extracts certain file types
from a directory, specifically `.caml` files by default. It then generates two
files:

* [output.txt](output.txt) contains the list of CAML files in /System/Library on
an iOS 13.5 device, this should help locate CAML resources for glyphs.

* [scp_command.sh](scp_command.sh) contains an scp command that can be run to dump
the files from your iOS device. More information on running scp_command.sh can be
found in the [Running The Output Script](#Running-The-Output-Script) section.

## Usage

`extract_files.py -i <inputfile> -o <outputfile> -s <script_file> -e <extension> -p <port> -u <user_and_host>`

The default values are:

`inputfile  = 'ls_System_Library.txt'`

`outputfile = 'output.txt'`

`extension  = 'caml'`

`script_file = 'scp_command.sh'`

`port = 2022`

`user_and_host  = 'root@localhost'`

## Running The Output Script

The output script file is meant to be run in an empty target directory, if the directory isn't empty, the script won't run.

Give the file execution permission and run it in the target directory to populate it with the output CAML files.

```bash
chmod +x [$path_to_script_file]
[$path_to_script_file]
```
