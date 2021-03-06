import argparse
import gettext
from os import path,remove, makedirs
from shutil import rmtree
import pkg_resources
import subprocess
import sys

from ancient.version import argparse_epilog,  __version__

try:
    t=gettext.translation('ancient',pkg_resources.resource_filename("ancient","locale"))
    _=t.gettext
except:
    _=str

def main():
    parser=argparse.ArgumentParser(prog='ancient', description=_('Moves ancient files from a directory to another one. Then you can backup result'), epilog=argparse_epilog(), formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source', action='store', help=_('Directory from'))
    parser.add_argument('--destiny', action='store', help=_('Directory to'))
    parser.add_argument('--days_old', action='store', help=_('Days old of the files to move'), default=365)
    group.add_argument('--create_example', action='store_true', help=_('Creates an automatic example to show features in ancient_example directory'), default=False)
    group.add_argument('--remove_example', action='store_true', help=_('Removes example directory'), default=False)
    args=parser.parse_args()

    if args.source:
        if args.destiny is None:
            print(_("You must set a to directory"))
            exit(1)
    elif args.create_example:
        source="ancient_example/source"
        destiny="ancient_example/destiny"
        makedirs(source, exist_ok=True)
        makedirs(destiny, exist_ok=True)
    elif args.remove_example:
        rmtree("ancient_example")


def process(source,destiny,days_old):
    pass
