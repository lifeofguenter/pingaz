'''
PingAZ
'''

import logging

import boto3
import click

from pingaz import cloudwatcher
from pingaz import pinger


boto3.set_stream_logger('', logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('hosts', nargs=-1)
def target(hosts):
    '''check latency of given hosts'''

    results = pinger.ping(hosts)
    cloudwatcher.put(results)


@cli.command()
def asg():
    print('nada')


if __name__ == '__main__':
    cli()
