#!/usr/bin/env python2
# =============================================================================
# @file   deploy.py
# @author Albert Puig (albert.puig@epfl.ch)
# @date   03.02.2014
# =============================================================================
"""Install things needed for python."""

import os

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

packages = [ 'Fabric',
             'beautifulsoup4',
             'fitbit',
             'fonttools',
             'fuzzywuzzy',
             'ipython',
             #'line_profiler',
             'memory_profiler',
             'numpy',
             'matplotlib',
             'progressbar',
             'psutil',
             'pyflakes',
             'pylint',
             'radon',
             'scipy',
             'sh',
             'subliminal',
             'paramiko',
             'nose',
             'PyYAML',
             'pycolors',
             'oauth2',
             'pathfinder'
           ]

if __name__ == '__main__':
    if which('pip2'):
        os.system('pip2 install -U %s' % (' '.join(packages)))
    else:
        print "First run brew and afterwards install the pip packages"

# EOF
