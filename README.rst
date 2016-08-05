TemplateRex
===========

TemplateRex is a pure template engine (ie no embedded logic) written in 
Python - small and fast.   

Philosophy
----------

First order is KISS - keep it simple. Second is to strive to keep logic 
together in the logic domain handled by a first class scripting language 
and presentation (html,xml) in the presentation domain. 

Invariably template engines that embed logic/code within html continue 
to add functionality to the point where they themselves become a complex 
programming environment which is less functional but more complex and 
cryptic than the underlying python language itself - violating the KISS
principle and raising the learning curve. 

TemplateRex templates are fully viewable in a browser or WYSIWYG 
editor. Allowing front-end designers and back-end developers to work 
seperately - and not introduce security issues.     

This approach often results in dry'er code due to seperation of domains.
For example a template object can be feed to a common function for 
different look, feel and data scope. 


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
