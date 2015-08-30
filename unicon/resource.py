import os
import unicon.data as udata
import unicon.openstack as uos

class Resource(object):

    def __init__(self):
        res = udata.get_resource_access_info()
        self.cred = self._helper_to_convert(res)
        self.user_data = None
        self.cluster_info = None
        self.count = 1
        self.name = None

    def number_of_nodes(self, count):
        self.count = count

    def cluster_name(self, name):
        self.name = name

    def allocate(self, name, count=1, resource=None):
        """Allocate resources (VMs)"""

        # Identify type of resources: AWS, openstack, etc
        if self.count > count:
            count = self.count
        cred = self.cred
        if cred['TYPE'] == 'openstack':
            res = uos.buy(cred, count, name, self.cluster_info['commands'])
        elif cred['TYPE'] == 'AWS':
            print ("TBD")
        else:
            print ("Unexpected type")

    def set_user_data(self, udata):
        self.user_data = udata

    def set_cluster_info(self, cinfo):
        self.cluster_info = cinfo

    def runcmd(self, cmd=None):
        # TBD
        # Level of runcmd
        # - [Before boot] Operating system (custom image with builtin software)
        #   e.g. biolinux - In cloud, download and register ISO image for future
        #   use
        #   - Baremetal, PXE Boot selects OS to install
        # - [After boot] Bootstrap (boot script)
        #   - systemd, cloud-init, cloud-config
        # - [On runtime] SSH
        # - ansible, chef, puppet

        pass

    def _helper_to_convert(self, resource):

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
    buy = allocate
    launch = allocate
