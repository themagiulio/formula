import argparse
import urllib.request
from urllib.error import HTTPError
import wget
import io
import requests
import json
import os
import shutil
import tarfile
import yaml
import sys
import pkg_resources
import subprocess


def displayVersion():
    print(f"Formula v{pkg_resources.get_distribution('formula').version}")
    print("Developer by: Giulio De Matteis <giuliodematteis@icloud.com>")

default_config = [
    {
        'folders': {
            'build': 'build',
            'source': 'src'
        }
    },
    {
        'scripts': {
            'start': 'formula --compile && ./build/program.out'
        }
    },
    {
        'packages': []
    }
]

def openConfig():
    try:
        with open('config.yaml') as file:
            return yaml.full_load(file)
    except IOError:
        print("No config.yaml file found.")
        return False

def projectInit(name):
    os.mkdir(name)
    os.mkdir(os.path.join(name, 'fortran_modules'))
    os.mkdir(os.path.join(name, 'src'))
    with open(os.path.join(os.getcwd(), name, 'config.yaml'), 'w') as file:
        document = yaml.dump(default_config, file)
    
def projectCompile():
    try:
        document = openConfig()
        src = list(document[0].values())[0]['source']
        bld = list(document[0].values())[0]['build']
        mod = list(document[0].values())[0]['modules']
        if not os.path.exists(src):
            print('The source folder does not exist.')
            return
        if not os.path.exists(bld):
            os.mkdir(bld)
        process = subprocess.run(f'gfortran {src}/* -o {bld}/program.out', shell=True)
    except KeyError:
        print('Source and/or Build folders are not properly set.')

def runScript(name):
    try:
        document = openConfig()
        process = subprocess.run(list(document[1].values())[0][name], shell=True)
    except KeyError:
        print('No script was found with the provided name.')

repo = 'https://pastebin.com/raw/E9aiX0NA'

def packageAdd(name):
    try:
            with urllib.request.urlopen(repo) as url:
                data = json.loads(url.read().decode())
            if '@' not in name:
                download_url = list(data[name].values())[0]
                version = list(data[name].keys())[0]
            else:
                name, version = name.split('@', 1)
                download_url = data[name][version]
                   
            document = openConfig()
            if document == False:
                return

            pkglist = list(document[2].values())[0]
            if f"{name}@{version}" in pkglist:
                print(f"{name}@{version} is already installed.")
                return


            pkg = f"{name}-{download_url.rsplit('/', 1)[-1]}"
            pkg_archive_path = os.path.join('fortran_modules', pkg)
            pkg_path = os.path.join('fortran_modules', f"{name}@{version}")
            wget.download(download_url, out=pkg_archive_path)
            print()
            if pkg.endswith('tar.gz') or pkg.endswith('tgz'):
                tar = tarfile.open(pkg_archive_path, "r:gz")
                tar.extractall(pkg_path)
                tar.close()

            elif pkg.endswith('tar'):
                tar = tarfile.open(pkg_archive_path, "r:")
                tar.extractall(pkg_path)
                tar.close()

            os.unlink(pkg_archive_path)

            if document == False:
                return
            pkglist.append(f"{name}@{version}")
            with open('config.yaml', 'w') as file:
                yaml.dump(document, file)

    except HTTPError as e:
        if e.code == 404:
            print('The provided repository does not work.')
    except KeyError:
        print('The provided module does not exists.')

def packageRemove(name):
    document = openConfig()
    pkglist = list(document[2].values())[0]
    pkgs = [pkg for pkg in pkglist if name in pkg]
    pkgs_len = len(pkgs)

    if pkgs_len == 0:
        print('No module was found.')
    elif pkgs_len == 1:
        pkg_path = os.path.join('fortran_modules', pkgs[0])
        if os.path.exists(pkg_path):
            shutil.rmtree(pkg_path)

        document = openConfig()
        pkglist = list(document[2].values())[0]
        pkglist.remove(pkgs[0])
        with open('config.yaml', 'w') as file:
            yaml.dump(document, file)
        print(f"{pkgs[0]} was succesfully removed.")
    elif pkgs_len > 1:
        print(f"{pkgs_len} modules were found. Type the name and the version of the one you want to remove.")
        for pkg in pkgs:
            print(f"- {pkg}")

def packageList():
    document = openConfig()
    if document == False:
        return
    pkglist = list(document[2].values())[0]
    for pkg in pkglist:
        print(f"- {pkg}")

def cli():
        parser = argparse.ArgumentParser(description='Fortran Package Manager.')

        parser.add_argument('--init', '-i',
                            dest='projectName',
                            help='Start a Fortran project in the current folder')

        parser.add_argument('--add', '-a',
                            dest='packageName',
                            nargs='+',
                            help='Add a module')

        parser.add_argument('--remove', '-R',
                            dest='packageNameToRemove',
                            nargs='+',
                            help='Remove a module')

        parser.add_argument('--list', '-l',
                            dest='packageList',
                            action='store_const',
                            const=True,
                            help='Display installed packages')

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
            elif args.packageList:
                packageList()
        elif nargs == 3:
            if args.projectName:
                projectInit(args.projectName)
            elif args.scriptName:
                runScript(args.scriptName)
        if args.packageName:
            for pkg in args.packageName:
                packageAdd(pkg)
        if args.packageNameToRemove:
            for pkg in args.packageNameToRemove:
                packageRemove(pkg)