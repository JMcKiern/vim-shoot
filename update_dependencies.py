#!/bin/python3
import subprocess
import sys

subprocess.check_call([sys.executable, *('-m pip install selenium requests --ignore-installed -t 3rdparty/'.split(' '))])
