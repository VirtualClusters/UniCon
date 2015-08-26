import click

@click.group()
def cli():
    pass

@cli.command('create')
@click.argument('app')
def create(app):
    """Creates a new cluster"""
    click.echo("%s cluster" % app)



