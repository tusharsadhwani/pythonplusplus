#!/usr/bin/env python3
import argparse
import os.path
import sys

from ppp_compiler import compile_ppp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PPP Compiler (Transpiler)")
    parser.add_argument('filepath', help="path to .pp file")
    parser.add_argument('-o', help="name of the output file")
    if len(sys.argv) == 1:
        # parser.print_help(sys.stderr)
        # sys.exit(1)
        class args:
            filepath = 'test.pp'
            o = None
    else:
        args = parser.parse_args()

    if not os.path.exists(args.filepath):
        msg = "File {} doesn't exist"
        raise ValueError(msg.format(args.filepath))
    
    with open(args.filepath) as f:
        outfile_name = compile_ppp(f, args.o)
    print(outfile_name, "created successfully")