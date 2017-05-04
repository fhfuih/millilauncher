"""
A command-line interface
"""
import logging
import click

from . import api
from .config import config

from .version import __version__ as version

logging.basicConfig(filename='millilauncher.log', filemode='w', level=logging.DEBUG)

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
    if config.first_run:
        click.echo('This seems the first run. Running setup wizard.')
        _wizard()

@main.command()
@click.argument('version')
@click.option('-r', '--raw', is_flag=True, default=False)
def launch(version, raw):
    """
    Launch Minecraft of the given version
    """
    launcher = api.LauncherCore(config.mc_dir, config.java_dir)
    if raw:
        click.echo(launcher.launch_raw(version, config.username, config.max_mem))
    else:
        launcher.launch(version, config.username, config.max_mem)

# @main.command('download')
# @click.argument('version')
# @click.option('-c', '--client', is_flag=True)
# @click.option('-a', '--assets', is_flag=True)
# @click.option('-l', '--libraries', is_flag=True)
# @click.option('-F', '--forge', is_flag=True)
# @click.option('-L', '--liteloader', is_flag=True)
# @click.option('-E', '--external', is_flag=True, default=False, help='Open the download link externally.\
#     Useful when you want to download files in another manner. Default is False')
# def _download(version, **components):
#     """
#     Download Minecraft, components or mods
#     """
#     pass

@main.command('config')
@click.argument('action', type=click.Choice(['reset', 'wizard']), required=False)
# @click.option('-l', '--lang', help='Language of this command-line interface')
@click.option('-e', '--exit-on-launch', is_flag=True, help='Whether to terminate the launcher once the game is launched')
@click.option('-M', '--mc-dir', help='Path to \'.minecraft\' folder')
@click.option('-J', '--java-dir', help='Path to \'javaw.exe\'')
@click.option('-m', '--max-mem', type=int, help='Maximum memory allocated to Minecraft')
@click.option('-f', '--fullscreen', is_flag=True, help='Whether to launch Minecraft in fullscreen')
# @click.option('-L', '--login-mode', help='Default login mode.\
#     Can be overrided by passing an argument to \'launch\' command')
@click.option('-U', '--username', help='Username for the default Minecraft account.')
# @click.option('-P', '--password', help='Password for the default Minecraft account.')
# @click.option('-s', '--download-source', help='Default source from which the launcher downloads resources')
def config_(action, **kw):
    """
    Configure your launcher and game preferences.
    The 'action' argument is optional, and can be 'reset' or 'wizard'. 
    If it's left blank, only given options will be set.
    Else, given options will be set AFTER the corresponding action is executed.
    """
    if action == 'reset':
        ok = click.prompt('Are you sure you want to reset you settings?', confirmation_prompt=True)
        if ok:
            config.reset()
    elif action == 'wizard':
        _wizard()

    for k, v in kw.items():
        if v is None:
            break
        if isinstance(v, str) and v[0] == '=':
            v = v[1:]
        config[k.replace('-', '_')] = v
    config.save()

def _wizard():
    click.echo('Running the setup wizard. On each line, a default value is shown in the brackets if valid.\
        Leave blank to use it, or enter a new value.')
    config.mc_dir = click.prompt('Your \'.minecraft\' folder path', show_default=True, default=config.mc_dir, type=click.Path(exists=True))
    config.java_dir = click.prompt('Your \'javaw\' file path', show_default=True, default=config.java_dir, type=click.Path(exists=True))
    config.max_mem = click.prompt('Maximum memory allocated to Minecraft in MB', show_default=True, default=config.max_mem, type=int)
    config.username = click.prompt('Your Minecraft username', show_default=True, default=config.username)
    click.echo('Done! More entries can be reached later manually.\n')
    config.save()

@main.command('list')
@click.argument('src', type=click.Choice(['local', 'remote']), default='local')
@click.option('-m', '--min', help='The oldest version of a range', default=None)
@click.option('-M', '--max', help='The latest version of a range', default=None)
def list_(src, min, max):
    """
    List Minecraft versions in a range(if given).
    The 'src' argument can be 'local'(default) or 'remote'.
    The former will check valid Minecraft versions on your computer.
    The latter will get a list of valid versions released by Mojang.
    """
    if src == 'local':
        launcher = api.LauncherCore(config.mc_dir, config.java_dir)
        vlist = launcher.versions.list
        try:
            begin = vlist.index(min)
        except ValueError:
            begin = 0
        try:
            end = vlist.index(max) + 1
        except ValueError:
            end = len(vlist)
        click.echo('\n'.join(vlist[begin:end]))
    else:
        pass

if __name__ == '__main__':
    main()
