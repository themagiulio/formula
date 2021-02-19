# Formula

Formula is a package manager built for the Fortran Language.

## Installation

You can install the latest version through pip: `pip install formulapm`

## Commands

### Initialize Project

`formula --init <Project Name>` or `formula -i <Project Name>`

### Add Package

`formula --add <Package Name>` or `formula -a <Package Name>`

### Remove Package

`formula --remove <Package Name>` or `formula -R <Package Name>`

### Package List

`formula --list` or `formula -l`

### Compile Project

`formula --compile` or `formula -c`

*gfortran is required to compile Fortan projects.*

### Run Script

`formula --run <Script Name>` or `formula -r <Script Name>`

### Run Start Script

`formula --start` (alias for `formula --run start`)

### Display Formula Version

`formula --version` or `formula -v`

## Configure Project

The project is configurable by editing the `config.yaml` file, which is automatically created when a project is initialized.

### Configure repositories

Repositories can be linked to Formula with a json file which contains all the information about the inserted packages and their versions.

Each projects come with a default repository. Multiple repositories can be added. If they have packages with the same name the latter repository will be priviged.

**Example**

```
- repositories:
  - https://pastebin.com/raw/E9aiX0NA
```

### Configure Project Folders

Project Folders like `build` and `src` are configurable through the `folders` section.

**Example**

```
- folders:
    build: build
    source: src
```

### Configure Scripts

Scripts can be added through the `scripts` section.

**Example**

```
- scripts:
    start: echo "Hello World!"
```

```
$ formula --run start
Hello World!
```