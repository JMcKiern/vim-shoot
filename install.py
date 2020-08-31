#!/bin/python3
import subprocess
import sys

dependencies = ['selenium', 'requests']

print('Installing dependencies (', *dependencies, ') with pip')
subprocess.check_call([sys.executable, *(' '.join(['-m pip install', *dependencies, '--ignore-installed -t 3rdparty/']).split(' '))])
