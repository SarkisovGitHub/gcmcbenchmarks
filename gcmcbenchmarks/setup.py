from setuptools import setup, find_packages

from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()


setup(
    name = 'gcmcbenchmarks',
    version = '1.0.0',
    long_description=long_description,

    packages=find_packages(),
    include_package_data=True,

    scripts = [
        'bin/make_cassandra_sims.py',
        'bin/make_dlm_sims.py',
        'bin/make_towhee_sims.py',
        'bin/make_music_sims.py',
        'bin/make_raspa_sims.py',
        'bin/check_exit.py',
    ],
)
