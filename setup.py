from setuptools import setup
import os

if __name__ == '__main__':
    setup(
        install_requires=[
            f'pdf-generator @ file://{os.getcwd()}/lib/pdf-generator'
        ]
        )