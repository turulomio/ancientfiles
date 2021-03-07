from datetime import datetime
from gettext import translation
from pkg_resources import resource_filename

__versiondatetime__ = datetime(2021, 3, 7)
__versiondate__=__versiondatetime__.date()
__version__ = '0.1.0'

try:
    t=translation('ancientfiles', resource_filename("ancientfiles","locale"))
    _=t.gettext
except:
    _=str

## Function used in argparse_epilog
## @return String
def argparse_epilog():
    return _("Developed by Mariano Muñoz 2021-{}").format(__versiondate__.year)
