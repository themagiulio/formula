import argparse
import sys
from Project.Manager import projectInit, projectCompile, runScript
from Package.Manager import packageAdd, packageRemove

def displayVersion():
    print('Formula v0.0.1')

parser = argparse.ArgumentParser(description='Fortran Package Manager.')

parser.add_argument('--init', '-i',
                    dest='projectName',
                    help='Start a Fortran project in the current folder')

parser.add_argument('--add', '-a',
                    dest='packageName',
                    help='Add a module')

parser.add_argument('--remove', '-R',
                    dest='packageNameToRemove',
                    help='Remove a module')

parser.add_argument('--version', '-v',
                    dest='displayVersion',
                    action='store_const',
                    const=True,
                    help='Display Formula version')
        
parser.add_argument('--run', '-r',
                    dest='scriptName',
                    help='Run scripts located in config.yaml')

parser.add_argument('--start',
                    dest='runStart',
                    action='store_const',
                    const=True,
                    help='An alias for --run start')

parser.add_argument('--compile', '-c',
                    dest='projectCompile',
                    action='store_const',
                    const=True,
                    help='Compile Fortran project')

args = parser.parse_args()
nargs = len(sys.argv)

if nargs == 1:
    parser.print_help()
    sys.exit(1)
elif nargs == 2:
    if args.displayVersion:
        displayVersion()
    elif args.projectCompile:
        projectCompile()
    elif args.runStart:
        runScript('start')
elif nargs == 3:
    if args.projectName:
        projectInit(args.projectName)
    elif args.scriptName:
        runScript(args.scriptName)
    elif args.packageName:
        packageAdd(args.packageName)
    elif args.packageNameToRemove:
        packageRemove(args.packageNameToRemove)