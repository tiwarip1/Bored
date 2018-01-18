from cx_Freeze import setup, Executable

buildOptions = dict(packages = [], excludes = [])
 
import sys
base = 'Win32GUI' if sys.platform='win32' else  None
 
executables = [
    Executable('rubiks.py', base=base)
]
 
setup(
    name='Tetris',
    version = '0.1',
    description = 'A PyQt Tetris Program',
    options = dict(build_exe = buildOptions),
    executables = executables
)