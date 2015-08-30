import click
import unicon.data as udata
import unicon.resource as uresource
import unicon.keypair as ukey
from subprocess import call

@click.group()
def cli():
    pass

@cli.command('create')
@click.argument('name')
@click.option('--count', default=1, help='Number of nodes')
def create(name, count):
    """Creates a new cluster"""
    click.echo("%s cluster" % name)
    cinfo = udata.read_cluster(name)
    ures = uresource.Resource()
    ures.number_of_nodes(count)
    ures.cluster_name(name)
    ures.set_cluster_info(cinfo)
    ures.allocate(name) # Allocate, launch, boot 
    ures.runcmd() # make it mine, configure, run scripts
    # Provide acccess info
    click.echo(res)

@cli.command('ssh')
def ssh():
    """SSH into a machine (TBD)"""
    pass

@cli.command('list')
@click.argument('name', default='cluster')
def lists(name):
    """Lists clusters or resources"""
    if name == "cluster":
        # list of clusters from yaml 
        ddict = dict(enumerate(udata.clusters(), start=1))
    elif name == "resource":
        ddict = dict(enumerate(udata.resources(), start=1))
    elif name == "key":
        ddict = dict(enumerate(ukey.list_keys(), start=1))
    else:
        print ("Unexpected type: {0}".format(name))# %s" % name)
        ddict = {}

    for num, val in ddict.iteritems():
        print ("{0}) {1}".format(num, val))

@cli.command('register')
@click.argument('name')
def register(name):
    """Registers clusters or resources"""
    if name == "cluster":
        click.echo("hello registering cluster")
    elif name == "resource":
        register_resource(name)
    else:
        click.echo("not supported")

def register_resource(name):
    rtype = click.prompt("1) bare metal, 2) IaaS", type=int)
    cert = None
    if rtype == 1:
        click.echo("Cobbler or PXE Boot will be configured (TBD)")
    elif rtype == 2:
        click.echo("Provide IaaS Credentials (End with 'EOF')")
        #credential = click.get_text_stream('stdin')
        sentinel = 'EOF'
        cred = '\n'.join(iter(raw_input, sentinel))
        #click.echo(creds)
        if click.confirm("Cert file?"):
            cert = '\n'.join(iter(raw_input, sentinel))
        rname = click.prompt("Resource name? (e.g. futuresystems," \
                + "chameleon, AWS", type=str)
        udata.write_resource(rname, "cred", cred)
        if cert:
            udata.write_resource(rname, "cert", cert)

@cli.command('update')
@click.argument('rtype')
def update(rtype):
    """Updates clusters or resources"""
    if rtype == "cluster":
        # list of clusters from yaml 
        ddict = dict(enumerate(udata.clusters(), start=1))
    elif rtype == "resource":
        ddict = dict(enumerate(udata.resources(), start=1))
    else:
        print ("Unexpected type")# %s" % name)
        ddict = None

    for num, val in ddict.iteritems():
        print ("{0}) {1}".format(num, val))

    num = click.prompt("Choose to update", type=int)
    click.edit(filename=udata.get_filepath(name=ddict[num], rtype=rtype)) 

@cli.command('keygen')
@click.argument('name', default=None)
def keygen(name):
    """Creates a new ssh key"""
    ukey.create_new_keypair(name)

@cli.command('keydel')
@click.argument('name')
def keydel(name):
    """Deletes a keypair"""
    ukey.delete_key(name)
    
# HELPER FUNCTIONS FOR SYSTEM COMMANDS
#
@cli.command('ls')
@click.argument('path', default="")
def ls(path):
    """ls .unicon directory"""
    call(['ls', "-al", (udata.BASE_DIR + "/" + path)])

@cli.command('nano')
@click.argument('path')
def nano(path):
    """nano .unicon directory"""
    call(["nano", (udata.BASE_DIR + "/" + path)])

@cli.command('cat')
@click.argument('path')
def cat(path):
    """cat .unicon directory"""
    call(["cat", (udata.BASE_DIR + "/" + path)])

