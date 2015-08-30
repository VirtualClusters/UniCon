import os
import unicon.data as udata
import unicon.openstack as uos

def buy(count, name, resource=None):
    """Allocate resources (VMs)"""
    res = udata.get_resource()
    # Identify type of resources: AWS, openstack, etc
    cred = _helper_to_convert(res)
    if cred['TYPE'] == 'openstack':
        res = uos.buy(cred, count, name)
    elif cred['TYPE'] == 'AWS':
        print ("TBD")
    else:
        print ("Unexpected type")

def _helper_to_convert(resource):

    res = {}
    rtype = None
    res_name = resource.keys()[0]

    for k, v in resource[res_name].iteritems():
        if k == "os_username":
            res['USERNAME'] = v
            rtype = "openstack"
        elif k == "os_password":
            res['PASSWORD'] = v
            rtype = "openstack"
        elif k == "os_tenant_name":
            res['PROJECT_ID'] = v
            rtype = "openstack"
        elif k == "os_auth_url":
            res['AUTH_URL'] = v
            rtype = "openstack"
        elif k == "os_cacert":
            res['CACERT'] = os.path.expanduser(v)
            rtype = "openstack"

    if rtype == "openstack":
        res['VERSION'] = 2 # DEFAULT, need to support 1.1
    if not 'CACERT' in res:
        res['CACERT'] = udata.get_cacert_path(res_name)
    res['TYPE'] = rtype
    return res

"""Alias"""
allocate = buy
launch = buy
