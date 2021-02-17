import os
import yaml
import subprocess

default_config = [
    {
        'folders': {
            'build': 'build',
            'source': 'src'
        }
    },
    {
        'scripts': {
            'start': 'echo "Hello World!"'
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
        print('No script was found with the mathcing name.')

