
from setuptools import setup, find_packages
import os


setup(name='gracc-email',
      version='1.0.0',
      description='GRACC Email',
      author_email='dweitzel@cse.unl.edu',
      author='Derek Weitzel',
      url='https://opensciencegrid.github.io/gracc',
      package_dir={'': 'src'},
      packages = ['gracc_email'],
      install_requires=['python-dateutil',
      'six',
      'toml',
      'urllib3',
      'wsgiref',
      'tabulate'
      ],
      entry_points= {
            'console_scripts': [
                  'backup_report = gracc_email.backup_report:main'
            ]
      },
      scripts=['run_backup_report']
)


