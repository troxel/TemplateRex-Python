# -*- coding: utf-8 -*-

def readme():
    with open('README.rst') as f:
        return f.read()

from distutils.core import setup
setup(name='TemplateRex',
      version='1.0',
      packages=['trex'],
      license='BSD',
      author='Steve Troxel',
      author_email='troxel@perlworks.com',
      description='KISS Pure Logicless Template Engine',
      long_description=readme(),
      keywords="template web html text",
      url='https://github.com/troxel/TemplateRex-Python',
      include_package_data=False,
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
)
