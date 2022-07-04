import os
from setuptools import setup

if __name__ == '__main__':
    setup(
        install_requires=[
            'pyyaml',
            'coloredlogs',
            f'pdf-generator @ file://{os.getcwd()}/lib/pdf-generator'
        ]
    )
