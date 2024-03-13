"""
pycx2 Compilation Module

This module provides functions for compiling Python version 2
source files using Cython.

Copyright (c) 2024 Rangga Fajar Oktariansyah.
All rights reserved.

Note:
  This module is designed to work with Python 2.7.

For more information and updates, visit: https://github.com/FajarKim/pycx2
"""

import os
import sysconfig
import subprocess
from Cython.Build import cythonize
from Cython.Compiler import Options

def compile(source_file, verbose=False):
    """
    Compile Python2 source file to executable using Cython.

    Args:
        source_file (str): Path to the Python source file.
        verbose (bool): If True, print detailed compilation information.

    Returns:
        tuple: A tuple containing the return code from the compilation process and the executable path.
    """
    basename = os.path.splitext(source_file)[0]
    c_file = basename + ".c"
    executable = "a.out"

    # Generate c file
    Options.embed = "main"
    compiler_directives = {"language_level": "2"}  # Python 2
    cythonize(source_file, compiler_directives=compiler_directives,
              force=True, quiet=not verbose)

    # Compile c file to executable
    cvars = sysconfig.get_config_vars()
    CC = cvars["CC"]  # Compiler
    INCLUDEPY = cvars["INCLUDEPY"]  # Python2 include directory
    BLDLIBRARY = cvars["BLDLIBRARY"]  # Python2 library
    BINLIBDEST = cvars["BINLIBDEST"]  # Python2 lib directory
    cmd = "{} -O2 {} -I{} -L{} {} -o {}".format(CC, c_file, INCLUDEPY, BINLIBDEST, BLDLIBRARY, executable)
    if verbose:
        print(cmd)
    return_code = subprocess.check_call(cmd.split(" "))
    if return_code != 0:
        print("Compilation failed.")
    return return_code, executable
