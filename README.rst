TemplateRex
===========

TemplateRex is a pure template engine that has no embedded logic and is 
written in Python - small and fast.   

Philosophy
----------

First order is KISS - keep it simple. Second is to strive to keep logic 
together in the logic domain handled by a first class scripting language 
and content/presentation (html,xml) in the presentation domain. 

Invariably template engines that embed logic/code within html continue 
to add functionality to the point where they themselves become a complex 
programming environment which is less functional but more complex and 
cryptic than the underlying python language itself - violating the KISS
principle and raising the learning curve. 

TemplateRex templates are fully viewable in a browser or WYSIWYG 
editor. This facilitates divsion of labor by allowing front-end 
designers and back-end developers to work seperately - and not introduce 
security issues. 

This approach often results in dry'er code due to seperation of domains.
For example a common core code base could serve up completely different
look and feel presentations and data scope by using diifferent templates
sets without a single for-loop or if-clause repeated.

There are other benefits refer to the paper "Enforcing Strict Model-View Separation in
Template Engines" by Terence Parr University of San Francisco 


Synopsis
--------

Here is a small hello world example.

Python Code::

    # --- Python Code ----

    trex = TemplateRex(fname='t-mytemplate.html')

    row = [ {'username:'Mary'},{'username':'Sam'} ]

    for row in row_data:
        trex.render_sec('row', row )
        
    trex.render_sec('tbl',{'category':'List of Usernames'})

    rendered_str = trex.render()

    # ---------------------

Template text::

    # --- Template t-mytemplate.html --------
    
    <!doctype html>
    <html>
    <head>...</head>
    <body>
    
    <table>
        <!-- BEGIN=row -->
        <tr><td>Hello $username</td></tr>
        <!-- END=row -->
    </table>
    </body>
    </html>
    # ---------------------

As shown text blocks are bracketed with BEGIN=name/END=name delimiters 
placed inside html comments. Note the END delimiter is named which helps
with fast comprehension of complex templates. 

Text in these blocks (or sections) are rendered via a call to 
render_sec(block_name,context). The overall or base template
is rendered with a call to render(). These blocks can be hierarchically
specified for example.

Python code::

    # --- Python Code ----

    trex = TemplateRex(fname='t-mytemplate.html')

    row = [ {'username:'Mary'},{'username':'Sam'} ]
    
    bat_lo_cell = [{ 'cellid':321,'volt':1.5}, { 'cellid':101,'volt':1.7}] }
    bat_hi_cell = [{ 'cellid':102,'volt':2.5}, { 'cellid':141,'volt':2.7}] }

    for row in bat_lo_cell:
        trex.render_sec('row', row )

    trex.render_sec('tbl', {'caption': 'Low Cells' } )

    for row in bat_hi_cell:
        trex.render_sec('row', row )

    trex.render_sec('tbl', {'caption': 'High Cells' } )

    rendered_str = trex.render()

    # ---------------------

Template text::

    # --- Template t-mytemplate.html --------
    
    ... surrounding html ...     
        
    <!-- BEGIN=tbl -->
    <table>
    <caption>$caption</caption>
        <tr><th>Cell ID</th><th>Voltage</th></tr>
        <!-- BEGIN=row -->
        <tr><td>$cellid </td><td> $volt</td></tr>
        <!-- END=row -->
    </table>
    <!-- END=tbl -->

    ... surrounding html ...     

    # ---------------------

This will render two tables one after the other with the unique caption and data. Over course this could be
done with a for-loop inside a for-loop but given as it for clarity. 




 


