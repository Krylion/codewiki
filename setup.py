import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='codewiki',
      version='0.1',
      description='codewiki',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python"
        ],
      author='Cezary Kaszuba | Sebastian Talarowski,
      author_email='kaszuba.cezary@gmail.com | talarek992@gmail.com',
      url='http://www.ckaszuba.com',
      keywords='wiki code cezary kaszuba sebastian talarowski wsinf wsiu',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='codewiki',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = codewiki:main
      [console_scripts]
      initialize_codewiki_db = codewiki.scripts.initializedb:main
      """,
      )
