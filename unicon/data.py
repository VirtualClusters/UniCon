import os
from glob import glob
import yaml
from unicon import util as uutil

BASE_DIR = os.path.expanduser("~") + "/.unicon"
RES_DIR = BASE_DIR + "/resource/"
CLS_DIR = BASE_DIR + "/cluster/"
KEY_DIR = BASE_DIR + "/key/"
INI_DIR = BASE_DIR + "/init/"

MAIN_CONF = BASE_DIR + "/conf.yaml"
KEY_CONF = KEY_DIR + "keys.yaml"

def list_clusters():
    return get_list_of_files(CLS_DIR + "/*.yaml")

def read_cluster(name):
    return read(CLS_DIR + name + ".yaml")

def list_resources():
    return get_list_of_files(RES_DIR + "/*")

def get_list_of_files(path):
    res = glob(path)
    return [os.path.splitext(os.path.basename(i))[0] for i in res]

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
    res = None
    if name:
        lres = list_resources()
        if name in lres:
            res = uutil.load_cred(RES_DIR + name + "/.cred")
    if not res:
        name = get_def_resource_name()
        res = uutil.load_cred(RES_DIR + name + "/.cred")
    return {name: res}

def get_def_resource_name():
    lres = list_resources()
    conf = read_conf()
    if conf['resource'] in lres:
        return conf['resource']
    else:
        print ("no default resource, first available resource will be used %s "\
                % lres[0])
    return lres[0]

def set_def_resource(name):
    print ("TBD")
 
def list_key_files():
    # Remove duplications
    return list(set(get_list_of_files(KEY_DIR + "/*")) -
            set(get_list_of_files(KEY_DIR + "/*.yaml")))

def read_key_conf():
    return read(KEY_CONF)

def write_key_conf(content):
    write(KEY_CONF, yaml.dump(content, default_flow_style=False))

def get_conf():
    try:
        return read(MAIN_CONF)
    except IOError, e:
        print ("No conf.yaml")
        raise

def list_inits():
    return get_list_of_files(INI_DIR + "/*")

def read_init(name):
    return read(INI_DIR + name)

def read(name):
    stream = file(name, 'r')
    ext = os.path.splitext(os.path.basename(name))[1] 
    if ext in [ ".yaml", ".yml" ]:
        return yaml.load(stream)
    else:
        return stream.read()

def write(filepath, data):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(filepath, 'w')
    f.write(data)
    f.write('\n')
    f.close()
   
def get_filepath(name, rtype, fname=None):
    if rtype == "cluster":
        filepath = CLS_DIR + name + (fname or ".yaml")
    elif rtype == "resource":
        filepath = RES_DIR + name + (fname or "/.cred")
    return filepath

def get_cacert_path(name):
    return get_filepath(name, "resource", ".pem")

"""Alias"""
clusters = list_clusters
resources = list_resources
read_conf = get_conf
conf = get_conf
get_resource_access_info = read_resource
read_userdata = read_init
