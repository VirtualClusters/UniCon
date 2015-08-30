import unicon.data as udata
import unicon.keypair as ukey
from novaclient import client
from novaclient import exceptions as nova_exceptions

def buy(cred, count, name):
    nova = client.Client(cred['VERSION'], cred['USERNAME'],
            cred['PASSWORD'], cred['PROJECT_ID'], cred['AUTH_URL'],
            cacert=cred['CACERT'])

    conf = udata.get_conf()
    vm_size = nova.flavors.find(name=conf['size'])
    vm_image = nova.images.find(name=conf['os'])
    userdata = udata.read_init(vm_image.name)
    # SSH KEY 
    dkey = ukey.get_default()
    try:
        vm_key = nova.keypairs.find(fingerprint=dkey['fingerprint'])
    except nova_exceptions.NotFound, e:
        vm_key = nova.keypairs.create(dkey['name'], dkey['public'])
    #USER DATA
    ret = nova.servers.create(name = name, image = vm_image, flavor =
    vm_size, min_count = count, userdata = userdata, key_name=vm_key.name, meta=
    {"client": "unicon CLI"})
    return ret

