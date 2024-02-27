from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()


setup(
    name='nwb4fprobe',
    version='0.1.1',
    url='https://github.com/sachuriga283/quality_metrix.git',
    author='sachuriga283',
    author_email='sachuriga.sachuriga@ntnu.no',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=read_requirements(),
)