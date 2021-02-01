from setuptools import setup, find_packages
from embedhtml.version import __version__ as version

setup(
    name='embedhtml',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        embedhtml=embedhtml.embedhtml:cli
    ''',
)
