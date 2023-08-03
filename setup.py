from setuptools import setup

setup(
    name='LoadShedAware',
    version='0.1',
    packages=['loadshedaware'],
    entry_points={
        'console_scripts': [
            'loadshedaware = loadshedaware.main:main',
        ],
    },
)