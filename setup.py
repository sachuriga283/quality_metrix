from setuptools import setup, find_packages
import setuptools
import warnings
def read_requirements():
    try:
        with open('requirements.txt', encoding='utf-8-sig') as req:
            return [line.strip() for line in req if line.strip() and not line.startswith('#')]
    except UnicodeDecodeError:
        with open('requirements.txt', encoding='utf-16') as req:
            return [line.strip() for line in req if line.strip() and not line.startswith('#')]

setup(
    name='nwb4fprobe',
    version='0.1.9.2',
    url='https://github.com/sachuriga283/quality_metrix.git',
    author='sachuriga283',
    author_email='sachuriga.sachuriga@ntnu.no',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=read_requirements(),
)

if __name__ == "__main__":
    setuptools.setup()