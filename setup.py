from setuptools import setup, Command
import site
import os
import platform



## Class to define doc command
class Doc(Command):
    description = "Update translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/ancientfiles.pot *.py ancientfiles/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/ancientfiles.pot")
        os.system("msgfmt -cv -o ancientfiles/locale/es/LC_MESSAGES/ancientfiles.mo locale/es.po")

class Procedure(Command):
    description = "Show release procedure"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
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

## Class to define doxygen command
class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/ancientfiles/ --delete-after")
        os.chdir("..")

## Class to define uninstall command
class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/ancientfiles*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/ancientfiles*")
        else:
            os.system("pip uninstall ancientfiles")

########################################################################


## Version of modele captured from version to avoid problems with package dependencies
__version__= None
with open('ancientfiles/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]


setup(name='ancientfiles',
     version=__version__,
     description='Moves ancient files from a directory to another selecting is age. Then you can backup them.',
     long_description='Project web page is in https://github.com/turulomio/ancientfiles',
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='move old files backup',
     url='https://github.com/turulomio/ancientfiles',
     author='Turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=['ancientfiles'],
     install_requires=[''],
     entry_points = {'console_scripts': [
                                           'ancientfiles=ancientfiles.core:main',
                                        ],
                    },
     cmdclass={'doxygen': Doxygen,
               'uninstall':Uninstall, 
               'doc': Doc,
               'procedure': Procedure,
              },
     zip_safe=False,
     include_package_data=True
)
