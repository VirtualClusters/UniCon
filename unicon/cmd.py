import click
import unicon.data as ud

@click.group()
def cli():
    pass

@cli.command('create')
@click.argument('name')
def create(name):
    """Creates a new cluster"""
    click.echo("%s cluster" % name)
    click.echo(ud.read_cluster(name))

@cli.command('list')
def list():
    """Lists clusters"""
    click.echo(ud.clusters())
    # list of clusters from yaml 


