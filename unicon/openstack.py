import re
import time
import unicon.data as udata
import unicon.keypair as ukey
import unicon.util as uutil
from novaclient import client
from novaclient import exceptions as nova_exceptions
#import urllib3
#urllib3.disable_warnings()

def buy(cred, count, name, user_cmds=None):
    nova = client.Client(cred['VERSION'], cred['USERNAME'],
            cred['PASSWORD'], cred['PROJECT_ID'], cred['AUTH_URL'],
            cacert=cred['CACERT'])

    conf = udata.get_conf()
    vm_size = nova.flavors.find(name=conf['size'])
    vm_image = nova.images.find(name=conf['os'])
    userdata = udata.read_userdata(vm_image.name)

    # SSH KEY 
    dkey = ukey.get_default()
    userdata = inject_cmds(name=vm_image.name, cmds=user_cmds,
            userdata=userdata, ssh_pub_key=dkey['public'])
    print userdata
    try:
        vm_key = nova.keypairs.find(fingerprint=dkey['fingerprint'])
    except nova_exceptions.NotFound, e:
        vm_key = nova.keypairs.create(dkey['name'], dkey['public'])
    #USER DATA
    ret = nova.servers.create(name = name, image = vm_image, flavor =
    vm_size, min_count = count, userdata = userdata, key_name=vm_key.name, meta=
    {"client": "unicon CLI"})
    #ADD PUBLIC IP
    ip_info = add_public_ip(nova, ret)
    instance = nova.servers.find(id=ret.id)
    res = { 'network': ip_info, 'instance': instance }
    return res

def add_public_ip(nova, server):
    """Creates a floating ip from the pool, and associates with server"""
    pools = nova.floating_ip_pools.list()
    pool = pools[0]
    fip = nova.floating_ips.create(pool.name)
    # novaclient.exceptions.BadRequest: No nw_info cache associated with
    # instance (HTTP 400) 
    # https://bugs.launchpad.net/nova/+bug/1249065
    # Fix released, Kilo, Liberty
    time.sleep(1.5)
    server.add_floating_ip(fip.ip)
    return fip

def inject_cmds(**kargs):
    """Injects commands to runcmd unit in cloud-config"""
    # if re.match(r"^#cloud-config[\n]*coreos", userdata):
        # THIS IS ABOUT COREOS
        # https://coreos.com/os/docs/latest/cloud-config.html

    discovery_token = uutil.discovery_etcd()
    runcmd_string = "".join(kargs['cmds'])
    ssh_pub_key = kargs['ssh_pub_key']
    userdata = kargs['userdata'] % vars()
    return userdata

