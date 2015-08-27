import click
import unicon.data as udata

@click.group()
def cli():
    pass

@cli.command('create')
@click.argument('name')
def create(name):
    """Creates a new cluster"""
    click.echo("%s cluster" % name)
    click.echo(udata.read_cluster(name))

@cli.command('list')
@click.argument('name', default='cluster')
def list(name):
    """Lists clusters or resources"""
    if name == "cluster":
        # list of clusters from yaml 
        dlist = list(enumerate(udata.clusters(), start=1))
    elif name == "resource":
        dlist = list(enumerate(udata.resources(), start=1))
    else:
        print ("Unexpected type")# %s" % name)
        dlist=None

    click.echo(dlist)

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
        udata.write_resource(rname, "cert", cert)

@cli.command('update')
@click.argument('name')
def update(name):
    """Updates clusters or resources"""
    if name == "cluster":
        # list of clusters from yaml 
        click.echo(udata.clusters())
    elif name == "resource":
        click.echo(udata.resources())


