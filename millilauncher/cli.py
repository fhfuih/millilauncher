"""
A command-line interface
"""

import os

import click

import api
from config import config
from __init__ import __version__ as version

CONTEXT_SETTINGS = {'help_option_names':['-h', '--help']}

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=version)
def main():
    """
    Millilauncher

    This is a minecraft launcher so minimalistic that it's stripped of a graphic interafce.
    You can launch Minecraft in a few commands, everything else is done in the backend.
    Sounds cool, doesn't it? Now it's your turn, hacker!
    """


@main.command('launch')
@click.argument('version')
@click.option('-r', '--raw', is_flag=True, default=False)
def _launch(version, raw):
    """
    Launch Minecraft of a certain version
    """
    launcher = api.LauncherCore(config.mc_dir, config.javaw_dir)
    if raw:
        click.echo(launcher.launch_raw(version, config.username, config.max_mem))
    else:
        launcher.launch(version, config.username, config.max_mem)


@main.command('download')
@click.argument('version')
@click.option('-c', '--client', is_flag=True)
@click.option('-a', '--assets', is_flag=True)
@click.option('-l', '--libraries', is_flag=True)
@click.option('-F', '--forge', is_flag=True)
@click.option('-L', '--liteloader', is_flag=True)
@click.option('-E', '--external', is_flag=True, default=False, help='Open the download link externally.\
    Useful when you want to download files in another manner. Default is False')
def _download(version, **components):
    """
    Download Minecraft, components or mods
    """
    pass

@main.group('config')
def _config():
    """
    Configure your millilauncher and launch preferences
    """
    pass

@_config.command('set')
@click.option('--lang', help='Language of this command-line interface')
@click.option('--mcDir', help='Path to \'.minecraft\' folder')
@click.option('--javaDir', help='Path to \'javaw.exe\'')
@click.option('--maxMem', help='Maximum memory allocated to Minecraft')
@click.option('--fullScreen', is_flag=True, help='Whether to launch Minecraft in fullscreen')
@click.option('--loginMode', help='Default login mode.\
    Can be overrided by passing an argument to \'launch\' command')
@click.option('--username', help='Username for the default Minecraft account.\
    Can be overrided by passing an argument to \'launch\' command')
@click.option('--password', help='Password for the default Minecraft account.\
    Can be overrided by passing an argument to \'launch\' command')
@click.option('--downloadSource', help='Default source from which the launcher downloads resources')
def _set(**kw):
    pass

@_config.command('reset')
def _reset():
    """
    Reset your configuration file to default
    """
    config.reset()

@_config.command('wizard')
def _wizard():
    """
    Run the setup wizard
    """
    pass


@main.group('list')
def _list():
    """
    List all valid Minecraft versions
    """
    pass

@_list.command('local')
def _local():
    """
    List valid Minecraft versions stored locally
    """
    pass

@_list.command('remote')
@click.option('-l', '--low')
@click.option('-h', '--high')
def _remote(low, high):
    """
    Fetch valid Minecraft versions list from Mojang in the range (if provided).
    """
    pass

if __name__ == '__main__':
    main()
