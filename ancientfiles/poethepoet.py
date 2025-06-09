from os import system
from ancientfiles import __version__




def translate():
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o ancientfiles/locale/ancientfiles.pot ancientfiles/*.py")
    system("msgmerge -N --no-wrap -U ancientfiles/locale/es.po ancientfiles/locale/ancientfiles.pot")
    system("msgfmt -cv -o ancientfiles/locale/es/LC_MESSAGES/ancientfiles.mo ancientfiles/locale/es.po")

def release():
    print("""Nueva versión:
  * Cambiar la versión y la fecha en version.py
  * Modificar el Changelog en README
  * python setup.py doc
  * Update locale/*.po
  * python setup.py doc
  * python setup.py install
  * python setup.py doxygen
  * git commit -a -m 'ancientfiles-{}'
  * git push
  * Hacer un nuevo tag en GitHub
  * python setup.py sdist upload -r pypi
  * python setup.py uninstall
  * Crea un nuevo ebuild de Gentoo con la nueva versión
  * Subelo al repositorio del portage
""".format(__version__))
