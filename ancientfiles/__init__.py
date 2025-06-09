from datetime import datetime
from gettext import translation
from importlib import resources

__versiondatetime__ = datetime(2025, 6, 9, 19, 43)
__versiondate__=__versiondatetime__.date()
__version__ = '0.3.0'

try:
    t=translation('ancientfiles', resources.path("ancientfiles","locale"))
    _=t.gettext
except:
    _=str

## Function used in argparse_epilog
## @return String
def argparse_epilog():
    return _("Developed by Mariano Muñoz 2021-{}").format(__versiondate__.year)

from ancientfiles.core import move_files,  create_empty_file
