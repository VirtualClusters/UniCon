import os
from glob import glob
import yaml

BASE_DIR = os.path.expanduser("~") + "/.unicon"
RES_DIR = BASE_DIR + "/resource/"
CLS_DIR = BASE_DIR + "/cluster/"

def list_clusters():
    return get_list_of_files(CLS_DIR + "/*.yaml")

def list_resources():
    return get_list_of_files(RES_DIR + "/*")

def get_list_of_files(path):
    res = glob(path)
    return [os.path.splitext(os.path.basename(i))[0] for i in res]

def read(name):
    stream = file(name, 'r')
    return yaml.load(stream)
    # READ FROM TEXT

def read_cluster(name):
    return read(CLS_DIR + name + ".yaml")

def write(filepath, data):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(filepath, 'w')
    f.write(data)
    f.write('\n')
    f.close()

def write_resource(name, ftype, text):
    if ftype == "cred":
        filename = ".cred"
    elif ftype == "cert":
        filename = ".pem"
    else:
        print ("Unexpected type")
        raise

    # From BASE_DIR
    filepath = (RES_DIR + name + "/" + filename)
    write(filepath, text)
    os.chmod(filepath, 0600)

def read_resource(name=None):
    if not name:
        res = get_def_resource()

def get_def_resource():
    lres = list_resources()
    conf = read_conf()

def get_conf():
    try:
        return read(BASE_DIR + "/conf.yaml")
    except IOError, e:
        print ("No conf.yaml")

def get_filepath(name, rtype):
    if rtype == "cluster":
        filepath = CLS_DIR + name + ".yaml"
    elif rtype == "resource":
        filepath = RES_DIR + name + "/.cred" 
    return filepath

"""Alias"""
clusters = list_clusters
resources = list_resources
read_conf = get_conf
conf = get_conf

