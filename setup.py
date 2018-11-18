# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='TemplateRex',
      version='1.0',
      packages=['templaterex'],
      license='BSD',
      author='Steve Troxel',
      author_email='troxel@perlworks.com',
      description='KISS Pure Logicless Template Engine',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords="template web html text logicless",
      url='https://github.com/troxel/TemplateRex-Python',
      include_package_data=False,
      install_requires=['MarkupSafe'],
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    project_urls={ 
        'Bug Reports': 'https://github.com/troxel/TemplateRex-Python/issues',
        'Source': 'https://github.com/troxel/TemplateRex-Python',
    },
)
