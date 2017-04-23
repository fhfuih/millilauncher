'''
A command-line interface
'''

import os

import click

import api
from config import config

CONTEXT_SETTINGS = {'help_option_names':['-h', '--help']}

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0')
def cli():
    '''
    Millilauncher

    This is a minecraft launcher so minimalistic that it's stripped of a graphic interafce.
    You can launch Minecraft in a few commands, everything else is done in the backend.
    Sounds cool, doesn't it? Now it's your turn, hacker!
    '''


@cli.command('launch')
@click.argument('version')
def _launch(version):
    '''
    Launch Minecraft of a certain version.
    '''
    print('launching', version, '...')

@cli.command('download')
@click.argument('version')
@click.option('--client', is_flag=True)
@click.option('--assets', is_flag=True)
@click.option('--libraries', is_flag=True)
@click.option('--forge', is_flag=True)
@click.option('--liteloader', is_flag=True)
@click.option('--external', is_flag=True, default=False, help='''Open the download link externally.\
    Useful when you want to download files in another manner. Default is False.''')
def _download(version, **components):
    '''
    Download Minecraft, components or mods.
    '''
    click.echo(version, components)

@cli.group('config')
def _config():
    pass

@_config.command('set')
@click.option('--lang', help='Language of this command-line interface.')
@click.option('--mcDir', help='Path to \'.minecraft\' folder.')
@click.option('--javaDir', help='Path to \'javaw.exe\'.')
@click.option('--maxMem', help='Maximum memory allocated to Minecraft.')
@click.option('--fullScreen', is_flag=True, help='Whether to launch Minecraft in fullscreen')
@click.option('--loginMode', help='''Default login mode.\
    Can be overrided by passing an argument to \'launch\' command.''')
@click.option('--username', help='''Username for the default Minecraft account.\
    Can be overrided by passing an argument to \'launch\' command''')
@click.option('--password', help='''Password for the default Minecraft account.\
    Can be overrided by passing an argument to \'launch\' command''')
@click.option('--downloadSource', help='Default source from which the launcher downloads resources.')
def _set(**kw):
    pass

@_config.command('reset')
def _reset():
    config.reset()

@_config.command('wizard')
def _wizard():
    info = config.minecraft_folder
    while True:
        info = click.prompt("Path to '.minecraft' folder",
                            default=info, show_default=True)
        if info and os.path.isdir(info):
            config.minecraft_folder = info
            break
        click.echo('Invalid input!')

    info = config.javaw_file
    while True:
        info = click.prompt("Path to 'javaw.exe' executable",
                            default=info, show_default=True)
        if info and os.path.isdir(info):
            config.javaw_file = info
            break
        click.echo('Invalid input!')



@cli.group('list')
def _list(low, high):
    '''
    List all valid Minecraft versions.
    '''
    pass

@_list.command('local')
def _local():
    pass

@_list.command('remote')
def _remote():
    pass

if __name__ == '__main__':
    cli()