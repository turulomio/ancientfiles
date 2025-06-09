import argparse
from gettext import translation
from datetime import datetime, timedelta
from glob import iglob
from os import path, makedirs, utime
from shutil import rmtree, move
from sys import exit
from importlib import resources


from ancientfiles import argparse_epilog

try:
    t=translation('ancientfiles', resources.path("ancientfiles","locale"))
    _=t.gettext
except:
    _=str

## Creates an empty file with a specific mtime
## @param path String with the file to create
## @param mtime Datetime with the file modification datetime
def create_empty_file(path, mtime):
    f=open(path,"w")
    f.close()
    utime(path, (mtime.timestamp(),mtime.timestamp()))
    print(f"  - Creating '{path}' with mtime: {mtime}")
    

def example_create(days_old):
    example_remove();
    source="ancientfiles_example/source"
    destiny="ancientfiles_example/destiny"
    makedirs(source, exist_ok=True)
    makedirs(destiny, exist_ok=True)
    print(_("Creating example files"))
    create_empty_file(f"{source}/more1month.txt", datetime.now()-timedelta(days=32))
    create_empty_file(f"{source}/more1year.txt", datetime.now()-timedelta(days=367))
    create_empty_file(f"{source}/more2year.txt", datetime.now()-timedelta(days=367*2))
    print(_("Processing example pretending"))
    move_files(source, destiny, days_old, False)
    print(_("Processing example moving with --write parameter"))
    move_files(source, destiny, days_old, True)

def example_remove():
    rmtree("ancientfiles_example",ignore_errors=True)

## Main function
## @param source String with the source directory
## @param destiny String with the destiny directory
## @param days_old Integer with the number of days 
## @param write Boolean set to move files if it's True. If False shows report
def move_files(source,destiny,days_old,write):
    cut=datetime.now()-timedelta(days=days_old)
    count, move_count= 0,  0
    for filename in iglob(source + '**/**', recursive=True):
        if path.isfile(filename):
            count+=1
            mtime=datetime.fromtimestamp(path.getmtime(filename))
            if mtime<cut:
                move_count+=1
                destiny_file=filename.replace(source,destiny)
                if write is True:
                    makedirs(path.dirname(destiny_file), exist_ok=True)
                    move(filename, destiny_file )
                    print(_(f"  - Moving '{filename}' >> '{destiny_file}'. {(cut-mtime).days} days"))
                else:
                    print(_(f"  - Will be moved '{filename}' >> '{destiny_file}'. {(cut-mtime).days} days"))
    print(_(f"Found {count} files in '{source}'. {move_count} files will be moved."))

def main():
    parser=argparse.ArgumentParser(prog='ancientfiles', description=_('Moves ancient files from a directory to another one. Then you can backup result'), epilog=argparse_epilog(), formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source', action='store', help=_('Directory from'))
    parser.add_argument('--destiny', action='store', help=_('Directory to'))
    parser.add_argument('--days_old', action='store', type=int, help=_('Days old of the files to move'), default=365)
    parser.add_argument('--write', action="store_true", help=_("Moves files instead of showing changes"), default=False)
    group.add_argument('--create_example', action='store_true', help=_('Creates an automatic example to show features in ancientfiles_example directory'), default=False)
    group.add_argument('--remove_example', action='store_true', help=_('Removes example directory'), default=False)
    args=parser.parse_args()

    if args.source:
        if args.destiny is None:
            print(_("You must set a to directory"))
            exit(1)
        move_files(args.source,args.destiny,args.days_old,args.write)
    elif args.create_example:
        example_create(args.days_old)
    elif args.remove_example:
        example_remove()
