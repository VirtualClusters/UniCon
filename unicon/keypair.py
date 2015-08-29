import os
import tempfile
import base64
import hashlib
from os import chmod
from Crypto.PublicKey import RSA
from unicon import data as udata
from unicon import util as uutil

# Thanks to http://stackoverflow.com/a/22449476
def create_new_keypair(name=None):
    if not name:
        public, private = get_new_keyname()
    else:
        public = udata.KEY_DIR + name
        private = udata.KEY_DIR + name + ".pk"

    key = RSA.generate(2048)
    with open(private, 'w') as content_file:
        chmod(private, 0600)
        content_file.write(key.exportKey('PEM'))
    pubkey = key.publickey()
    pubkey_str = pubkey.exportKey('OpenSSH')
    with open(public, 'w') as content_file:
        content_file.write(pubkey_str)

    # ADD KEY TO CONF
    if not add_key(name, pubkey.exportKey('OpenSSH')):
        os.remove(public)
        os.remove(private)
        return False
    print ("New key [{0}]: {1}".format(name, pubkey_str))

def get_new_keyname():
    directory = udata.KEY_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    tf = tempfile.NamedTemporaryFile(prefix="unicon-",dir=directory)
    pub = tf.name
    pri = pub + ".pk"
    return (pub, pri)

def list_keys(return_type="str"):
    kconf = get_conf()
    kdict = kconf['keys']
    dkey = kconf['default']
    result_str = []
    for kname, kvar in kdict.iteritems():
        if kname == dkey:
            isdefault = " (default)"
        else:
            isdefault = ""
        key_print = fingerprint(kvar['public'])
        created = kvar['created']
        result_str.append("{0}{1}: {2} ({3})".format(kname, isdefault, key_print, created))
        kdict[kname]['fingerprint'] = key_print 

    if return_type == "str":
        return result_str
    return kdict

def get_conf():
    #kflist = udata.list_keys() # Key File List
    kconf = udata.read_key_conf()
    return kconf

def add_key(name, keystring):
    """Adds a key, returns updated key configuration"""
    kconf = get_conf()
    if name in kconf['keys']:
        print ("Key {0} exists, try other name".format(name))
        return False
    name = str(name)
    kconf['keys'][name] = {}
    kconf['keys'][name]['public'] = keystring
    kconf['keys'][name]['created'] = uutil.current_time()
    if not kconf['default']:
        kconf['default'] = name

    udata.write_key_conf(kconf)
    return True

def delete_key(name):
    """Delete a key"""
    kconf = get_conf()
    if not name in kconf['keys']:
        print ("{0} not found".format(name))
        return False

    public = udata.KEY_DIR + name
    private = udata.KEY_DIR + name + ".pk"

    os.remove(public)
    os.remove(private)
 
    del kconf['keys'][name]
    if kconf['default'] == name:
        if len(kconf['keys']) == 0:
            kconf['default'] = ""
        else:
            kconf['default'] = kconf['keys'].keys()[0]

    udata.write_key_conf(kconf)
    return True

def set_default(name):
    print ("TBD")

def get_default():
    print ("TBD")

# Thanks to http://stackoverflow.com/a/6682934
def fingerprint(keystr):
    key = base64.b64decode(keystr.strip().split()[1].encode('ascii'))
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))

# ALIAS 
default = get_default
add = add_key
delete = delete_key
create = create_new_keypair
thumbprint = fingerprint
