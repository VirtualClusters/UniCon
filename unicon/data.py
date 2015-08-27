import os
from glob import glob
import yaml

BASE_DIR=os.path.expanduser("~") + "/.unicon"

def clusters():
    return list_clusters()

def list_clusters():
    return get_list_of_files(BASE_DIR + "/cluster/*.yaml")

def resources():
    return list_resources()

def list_resources():
    return get_list_of_files(BASE_DIR + "/resource/*")

def get_list_of_files(path):
    res = glob(path)
    return [os.path.splitext(os.path.basename(i))[0] for i in res]

def read(name):
    stream = file(name, 'r')
    return yaml.load(stream)
    # READ FROM TEXT

def read_cluster(name):
    return read(BASE_DIR + "/cluster/" + name + ".yaml")

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
        filename = name + ".pem"
    else:
        print ("Unexpected type")
        raise

    # From BASE_DIR
    filepath = (BASE_DIR + "/resource/" + name + "/" + filename)
    write(filepath, text)
    os.chmod(filepath, 0600)
