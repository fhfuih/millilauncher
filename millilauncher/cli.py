'''
A command-line interface
'''

import os

import click

import api
import prefs

CONTEXT_SETTINGS = {'help_option_names':['-h', '--help']}

launcher_prefs = None

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0')
def cli():
    '''
    Millilauncher

    This is a minecraft launcher so minimalistic that it's stripped of a graphic interafce.
    You can launch Minecraft in a few commands, everything else is done in the backend.
    Sounds cool, doesn't it? Now it's your turn, hacker!
    '''
    global launcher_prefs
    launcher_prefs = prefs.Prefs()
    if not os.path.exists('./millilauncher.json'):
        click.echo('First run, will execute setup wizard in a minute.')
        pass


@cli.command()
def wizard():
    '''Launcher setup wizard
    '''
    global launcher_prefs
    click.echo('Millilauncher setup wizard')

    info = api.systeminfo.default_java_directory
    if not info:
        while True:
            click.echo('Javaw.exe file not found. Please enter manually.')
            info = click.prompt('Path to Javaw.exe')
            if os.path.exists(info):
                break
    launcher_prefs.java_dir = info

    info = api.systeminfo.default_minecraft_directory
    if not info:
        while True:
            click.echo('.minecraft folder not found. Please enter manually.')
            info = click.prompt('Path to .minecraft folder')
            if os.path.exists(info):
                break
    launcher_prefs.mc_dir = info


@cli.command()
@click.argument('version')
def launch(version):
    '''
    Launch Minecraft of a certain version.
    '''
    print('launching', version, '...')

@cli.command()
@click.argument('version')
@click.option('--client', is_flag=True)
@click.option('--assets', is_flag=True)
@click.option('--libraries', is_flag=True)
@click.option('--forge', is_flag=True)
@click.option('--liteloader', is_flag=True)
@click.option('--external', is_flag=True, default=False, help='''Open the download link externally.
                                                                 Useful when you want to download files in another manner.
                                                                 Default is False.''')
def download(version, **components):
    '''
    Download Minecraft, components or mods.
    '''
    print(components)

@cli.command()
@click.option('--lang', help='Language of this command-line interface.')
@click.option('--mcDir', help='Path to \'.minecraft\' folder.')
@click.option('--javaDir', help='Path to \'javaw.exe\'.')
@click.option('--maxMem', help='Maximum memory allocated to Minecraft.')
@click.option('--fullScreen', is_flag=True, help='Whether to launch Minecraft in fullscreen')
@click.option('--loginMode', help='''Default login mode.
                                     Can be overrided by passing an argument to \'launch\' command.''')
@click.option('--username', help='''Username for the default Minecraft account.
                                    Can be overrided by passing an argument to \'launch\' command''')
@click.option('--password', help='''Password for the default Minecraft account.
                                    Can be overrided by passing an argument to \'launch\' command''')
@click.option('--downloadSource', help='Default source from which the launcher downloads resources.')
def config(**kw):
    '''
    Configure your launch preferences
    '''
    print(kw)

@cli.group('list')
def list_versions(low, high):
    '''
    List all valid Minecraft versions.
    '''
    pass

@list_versions.command()
def local():
    pass

@list_versions.command()
def remote():
    pass

if __name__ == '__main__':
    cli()