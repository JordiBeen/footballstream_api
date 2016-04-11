import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'pyramid_mako',
    'python-magic',
    'python-dateutil',
    'psycopg2',
    'transaction',
    'zope.sqlalchemy',
    'pyramid_beaker',
    'marshmallow==1.2.4',
    'itsdangerous',
    'GeoAlchemy2',
    'bcrypt',
    'pycrypto',
    'waitress',
    'requests'
]

setup(name='footballstream_api',
      version='1.0',
      description='footballstream_api',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="footballstream_api",
      entry_points="""\
      [paste.app_factory]
      main = footballstream_api:main
      [console_scripts]
      initialize_footballstream_api_db = \
        footballstream_api.scripts.initializedb:main
      updatecompetitions = footballstream_api.scripts.updatecompetitions:main
      updatestandings = footballstream_api.scripts.updatestandings:main
      updatematches = footballstream_api.scripts.updatematches:main
      updatecommentaries = footballstream_api.scripts.updatecommentaries:main
      updateteams = footballstream_api.scripts.updateteams:main
      updateplayers = footballstream_api.scripts.updateplayers:main
      """,
      )
