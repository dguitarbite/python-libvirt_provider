# -*- coding: utf-8 -*-

import click


@click.group()
def cli():
    """Python libvirt provider."""


@cli.command('dummy', short_help="just a dummy example text")
def dummy():
    """Dummy stub ..."""


if __name__ == "__main__":
    cli()
