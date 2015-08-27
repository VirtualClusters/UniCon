from os.path import expanduser, basename, splitext
from glob import glob
import yaml

BASE_DIR=expanduser("~") + "/.unicon"

def clusters():
    res = glob(BASE_DIR + "/cluster/*.yaml")
    return [splitext(basename(i))[0] for i in res]

def read(name):
    stream = file(BASE_DIR + name, 'r')
    return yaml.load(stream)

def read_cluster(name):
    return read("/cluster/" + name + ".yaml")

