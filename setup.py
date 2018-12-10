from setuptools import setup, find_packages

setup (
    name = 'rfiweb',
    version='0.1.0',
    description='RFIWeb UI',
    url='https://github.com/jockey10/rfiweb',
    author='Shane Boulden',
    author_email='stb@redhat.com',
    keywords='rcm api web flask',
    include_package_data=True,
    packages=find_packages()
)
