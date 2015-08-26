import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

reqs = [line.strip() for line in open('requirements.txt')]

setup(
   name='Unicon',
   version='0.1',
   author = "Hyungro Lee",
   author_email = "hroe.lee@gmail.com",
   description = ("Unified Controller for Virtual Clusters"),
   license = "GPLv3",
   keywords = "Virtual Cluster, Management",
   url = "https://github.com/virtualclusters/unicon",
   packages = ['unicon'],
   install_requires = reqs,
   long_description = read('README.md'),
   classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Scientific/Engineering",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU GEneral Public License v3 (GPLv3)",
            "Operating System :: POSIX :: Linux",
            "programming Language :: Python",
            ],
   py_modules=['unicon'],
   entry_points='''
      [console_scripts]
      unicon=unicon.cmd:main
      ''',
)
   
