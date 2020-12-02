from setuptools import setup

setup(
    name='embedhtml',
    version='0.1',
    py_modules=['embedhtml'],
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        embedhtml=embedhtml:cli
    ''',
)
