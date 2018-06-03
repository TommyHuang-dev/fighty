from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = "C:\\Python\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python\\tcl\\tk8.6"

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna", "parse", "pathfinder", "time", "math", "pygame", "sys", "random"]
includefiles = ['enemies', 'weapons']
includes = []
excludes = []
buildOptions = dict(include_files = ['your_folder/'])

options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "shooty",
    options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}},
    version = "1.1",
    description = 'hallos',
    executables = executables
)