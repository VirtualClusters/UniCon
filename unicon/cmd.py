import click

@click.group()
def cli():
    pass

@cli.command('create')
@click.argument('name')
def create(name):
    """Creates a new cluster"""
    click.echo("%s cluster" % name)

@cli.command('list')
@click.argument('name')
def list(name):
    """Lists clusters"""
    click.echo("mesos")
    # list of clusters from yaml 


