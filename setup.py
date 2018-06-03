from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = "C:\\Python\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python\\tcl\\tk8.6"

base = None
executables = [Executable("main.py", base=base)]

packages = ["idna", "parse", "pathfinder", "time", "math", "pygame", "sys", "random"]
buildOptions = dict(include_files = ['effects/', 'enemy_pic/', 'powerup/', 'projectiles/', 'sounds/', 'ui/', 'weapons/', 'datafiles/', 'player.png']) #folder,relative path. Use tuple like in the single file to set a absolute path.


options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
         name = "appname",
         version = "1.0",
         description = "description",
         author = "your name",
         options = dict(build_exe = buildOptions),
         executables = executables)

