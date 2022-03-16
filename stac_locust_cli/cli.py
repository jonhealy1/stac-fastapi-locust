import click

def hello_world():
    click.echo("HELLO WORLD!")

@click.option(
    "-h", "--hello", is_flag=True, help="Print hello world."
)
@click.command()
# @click.argument('file')
@click.version_option(version="0.1.4")
def main(hello):
    if hello:
        hello_world()