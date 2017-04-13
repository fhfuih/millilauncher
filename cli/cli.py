'''
A command-line interface
'''

import click

CONTEXT_SETTINGS = {'help_option_names':['-h', '--help']}

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0')
def cli():
    '''
    Minecraft Linecher

    This is a minecraft launcher so minimalistic that it's stripped of a graphic interafce.
    Now you can launch Minecraft in a few commands, everything else is done in the backend.
    Sounds cool, doesn't it? Now it's your turn, hacker!
    '''

@cli.command()
@click.argument('version')
def launch(version):
    '''
    Launch Minecraft of a certain version.
    '''
    print('launching', version)

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

@cli.command('list')
@click.option('--low')
@click.option('--high')
def list_(low, high):
    '''
    List all valid Minecraft versions within the range.
    '''
    pass

if __name__ == '__main__':
    cli()