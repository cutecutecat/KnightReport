from os.path import abspath, dirname
import sys

def fetch_cwd():
    if getattr(sys, 'frozen', False):
        return abspath(dirname(sys.executable))
    else:
        return abspath(dirname(dirname(__file__)))