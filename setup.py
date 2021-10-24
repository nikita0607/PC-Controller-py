from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pcclient',
    version='1.0',
    url='https://github.com/the-gigi/conman',
    license='MIT',
    
    author = "Nikita0607",
    author_email = "ecfed205@gmail.com",

    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'requests==2.26.0'
    ]
)
