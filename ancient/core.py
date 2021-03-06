import argparse
import gettext
from datetime import datetime, timedelta
from glob import iglob
from os import path,remove, makedirs, utime
from shutil import rmtree, move
import pkg_resources
import subprocess
import sys

from ancient.version import argparse_epilog,  __version__

try:
    t=gettext.translation('ancient',pkg_resources.resource_filename("ancient","locale"))
    _=t.gettext
except:
    _=str

## Creates an empty file with a specific mtime
def create_empty_file(path, mtime):
    f=open(path,"w")
    f.close()
    utime(path, (mtime.timestamp(),mtime.timestamp()))
    print(f"  - Creating '{path}' with mtime: {mtime}")
    

def example_create(days_old):
    example_remove();
    source="ancient_example/source"
    destiny="ancient_example/destiny"
    makedirs(source, exist_ok=True)
    makedirs(destiny, exist_ok=True)
    print(_("Creating example files"))
    create_empty_file(f"{source}/more1month.txt", datetime.now()-timedelta(days=32))
    create_empty_file(f"{source}/more1year.txt", datetime.now()-timedelta(days=367))
    create_empty_file(f"{source}/more2year.txt", datetime.now()-timedelta(days=367*2))
    print(_("Processing example pretending"))
    process(source, destiny, days_old, False)
    print(_("Processing example moving with --write parameter"))
    process(source, destiny, days_old, True)

def example_remove():
    rmtree("ancient_example",ignore_errors=True)

def process(source,destiny,days_old,write):
    cut=datetime.now()-timedelta(days=days_old)
    for filename in iglob(source + '**/**', recursive=True):
        if path.isfile(filename):
            mtime=datetime.fromtimestamp(path.getmtime(filename))
            if mtime<cut:
                destiny_file=filename.replace(source,destiny)
                if write is True:
                    move(filename, destiny_file )
                    print(_(f"  - Moving '{filename}' >> '{destiny_file}'. {(cut-mtime).days} days"))
                else:
                    print(_(f"  - Will be moved '{filename}' >> '{destiny_file}'. {(cut-mtime).days} days"))



def main():
    parser=argparse.ArgumentParser(prog='ancient', description=_('Moves ancient files from a directory to another one. Then you can backup result'), epilog=argparse_epilog(), formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source', action='store', help=_('Directory from'))
    parser.add_argument('--destiny', action='store', help=_('Directory to'))
    parser.add_argument('--days_old', action='store', type=int, help=_('Days old of the files to move'), default=365)
    parser.add_argument('--write', action="store_true", help=_("Moves files instead of showing changes"), default=False)
    group.add_argument('--create_example', action='store_true', help=_('Creates an automatic example to show features in ancient_example directory'), default=False)
    group.add_argument('--remove_example', action='store_true', help=_('Removes example directory'), default=False)
    args=parser.parse_args()

    if args.source:
        if args.destiny is None:
            print(_("You must set a to directory"))
            exit(1)
        process(args.source,args.destiny,args.days_old,args.write)
    elif args.create_example:
        example_create(args.days_old)
    elif args.remove_example:
        example_remove()
