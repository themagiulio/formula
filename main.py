import argparse
import sys
from Project.Manager import initProject

def displayVersion():
    print('Formula v0.0.1')

parser = argparse.ArgumentParser(description='Fortran Package Manager.')

parser.add_argument('--init', '-i',
                    dest='initProject',
                    help='Start a Fortran project in the current folder')

parser.add_argument('--version', '-v',
                    dest='displayVersion',
                    action='store_const',
                    const=True,
                    help='Display Formula version')

args = parser.parse_args()
nargs = len(sys.argv)

if nargs == 1:
    parser.print_help()
    sys.exit(1)
elif nargs == 2:
    if args.displayVersion:
        displayVersion()
elif nargs == 3:
    if args.initProject:
        initProject(args.initProject)