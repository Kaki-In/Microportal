#!/usr/bin/python3

from main_platform import *
import sys

def printHelp():
    print("""usage : {PATH} [--server|--help|-h]

Options : 
    	--server : starts the local server
    	--help|-h : displays this help

""".format(PATH = sys.argv[0]))

def main(args):
    if not args[1 : ]:
        return printHelp()
    command = args[1]
    if  command in ("--server",):
        platform = Platform()
        return platform.server.main()
    elif command in ("--help","-h"):
        return printHelp()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
