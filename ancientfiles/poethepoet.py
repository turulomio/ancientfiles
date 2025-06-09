from os import system
from ancientfiles import __version__




def translate():
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o ancientfiles/locale/ancientfiles.pot ancientfiles/*.py")
    system("msgmerge -N --no-wrap -U ancientfiles/locale/es.po ancientfiles/locale/ancientfiles.pot")
    system("msgfmt -cv -o ancientfiles/locale/es/LC_MESSAGES/ancientfiles.mo ancientfiles/locale/es.po")

def release():
    print("""Nueva versión:
  * Crear un issue en Github, una branch asociada, pegar el código que propone Github
  * Cambiar la versión y la fecha en __init__.py
  * Cambiar la versión en pyproject.toml
  * poe release
  * poe translate
  * Update ancientfiles/locale/*.po
  * poe translate
  * git commit -a -m 'ancientfiles-{}'
  * git push
  * Hacer un pull request para unir la versión
  * Hacer un nuevo tag en GitHub
  * poetry build
  * poetry publish --username --password
  * Crea un nuevo ebuild de Gentoo con la nueva versión
  * Subelo al repositorio del portage
""".format(__version__))
