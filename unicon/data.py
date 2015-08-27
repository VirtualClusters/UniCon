from os.path import expanduser, basename, splitext
from glob import glob

BASE_DIR=expanduser("~") + "/.unicon"

def clusters():
    res = glob(BASE_DIR + "/cluster/*.yaml")
    return [splitext(basename(i))[0] for i in res]

