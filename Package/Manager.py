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

repo = 'https://pastebin.com/raw/E9aiX0NA'

def openConfig():
    try:
        with open('config.yaml') as file:
            return yaml.full_load(file)
    except IOError:
        print("No config.yaml file found.")

def packageAlreadyInstalled(pkgName, pkgVersion):
    with open('config.yaml') as file:
        document = yaml.full_load(file)
        pkglist = list(document[2].values())[0]
        if f"{pkgName}@{pkgVersion}" in pkglist:
            return True
        else:
            return False

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
                   
            if packageAlreadyInstalled(name, version):
                print(f"{name}@{version} is already installed.")
                return

            #data = requests.get(download_url, stream=True)
            pkg = f"{name}-{download_url.rsplit('/', 1)[-1]}"
            pkg_archive_path = os.path.join('fortran_modules', pkg)
            pkg_path = os.path.join('fortran_modules', f"{name}@{version}")
            #open(pkg_archive_path, 'wb').write(data.raw.read())
            wget.download(download_url, out=pkg_archive_path)
            print()
            if pkg.endswith('tar.gz'):
                tar = tarfile.open(pkg_archive_path, "r:gz")
                tar.extractall(pkg_path)
                tar.close()

            elif pkg.endswith('tar'):
                tar = tarfile.open(pkg_archive_path, "r:")
                tar.extractall(pkg_path)
                tar.close()

            os.unlink(pkg_archive_path)

            with open('config.yaml') as file:
                document = yaml.full_load(file)
                pkglist = list(document[2].values())[0]
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
        with open('config.yaml') as file:
            document = yaml.full_load(file)
            pkglist = list(document[2].values())[0]
            pkglist.remove(pkgs[0])
        with open('config.yaml', 'w') as file:
            yaml.dump(document, file)
    elif pkgs_len > 1:
        print(f"{pkgs_len} modules were found. Type the name and the version of the one you want to remove.")
        for pkg in pkgs:
            print(f"- {pkg}")