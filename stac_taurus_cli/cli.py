import click
import os

@click.option("-l", "--locust", is_flag=True, help="Run Locust outside of the Taurus wrapper.")
@click.option("-t", "--taurus", is_flag=True, help="Run the Taurus wrapper.")
@click.command()
# @click.argument('file')
@click.version_option(version="0.1.4")
def main(locust, taurus):
    if locust:
        os.system('locust')
    if taurus:
        os.system('bzt taurus_locust.yml')