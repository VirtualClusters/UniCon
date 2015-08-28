import os
import tempfile
from os import chmod
from Crypto.PublicKey import RSA
from unicon import data as udata

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
    with open(public, 'w') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))

def get_new_keyname():
    directory = udata.KEY_DIR
    if not os.path.exists(directory):
        os.makedirs(directory)

    tf = tempfile.NamedTemporaryFile(dir=directory)
    pub = tf.name
    pri = pub + ".pk"
    return (pub, pri)

def list_keys():
    pass

def add_key(name, key):
    pass

def delete_key(name, key):
    pass
