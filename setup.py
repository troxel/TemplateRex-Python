# -*- coding: utf-8 -*-
"""
TemplateRex
~~~~~~

TemplateRex is a pure template engine (ie no embedded logic) written in 
Python - small and fast.   

Nutshell
--------

Here is a small example:

    # --- Python Code ----

    trex = TemplateRex(fname='t-mytemplate.html')

    row = [ {'username:'Mary'},{'username':'Sam'} ]

    for row in row_data:
        trex.render_sec('row', row )
        
    trex.render_sec('tbl',{'category':'List of Usernames'})

    rendered_str = trex.render()

    # ---------------------


    # --- Template t-mytemplate.html --------
    
    <!-- BASE name=t-base.html -->

    <!-- BEGIN name=tbl -->
    <table>
    <caption>$caption</caption>
        <!-- BEGIN name=row -->
        <tr><td>$username</td></tr>
        <!-- END name=row -->
    </table>
    <!-- END name=tbl -->

    # ---------------------


Philosophy
----------

First order is KISS - keep it simple. Second is to strive to keep logic 
together in the logic domain (if,for,while,etc) and presentation 
(html,xml,etc) in the presentation domain. 

Invariably template engines that embed logic/code within html continue 
to add functionality to the point where they themselves become a complex 
programming environment which is less functional but more complex and 
cryptic than the underlying python language itself - violating the KISS
principle and raising the learning curve.  

Also TemplateRex templates
are fully viewable in a browser or WYSIWYG editor. Allowing front-end
designers and back-end developers to work seperately - and not introduce 
security issues.     

"""

from distutils.core import setup
setup(name='TemplateRex',
      version='1.0',
      packages=['trex'],
      license='BSD',
      author='Steve Troxel',
      author_email='troxel@perlworks.com',
      url='http://perlworks.com',
      description='KISS Pure Template Engine',
      long_description=__doc__,
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
