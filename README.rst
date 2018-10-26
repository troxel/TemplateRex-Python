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
    from templaterex import TemplateRex

    trex = TemplateRex(fname='t-mytemplate.html')

    row = [ {'cellId:'A123','volt':1.21}, {'cellId:'B321','volt':1.52} ]

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
        <tr><th>Cell ID </th><th> Voltage </th></tr>
        <!-- BEGIN=row -->
        <tr><td>$cellId </td><td> $volt   </td></tr>
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
    from templaterex import TemplateRex

    trex = TemplateRex(fname='t-mytemplate.html')

    row = [ {'username:'Mary'},{'username':'Sam'} ]
    
    bat_lo_cell = [{ 'cellId':321,'volt':1.5}, { 'cellId':101,'volt':1.7}] }
    bat_hi_cell = [{ 'cellId':102,'volt':2.5}, { 'cellId':141,'volt':2.7}] }

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
        <tr><td>$cellId </td><td> $volt</td></tr>
        <!-- END=row -->
    </table>
    <!-- END=tbl -->

    ... surrounding html ...     

    # ---------------------

This will render two tables one following the other with the unique caption 
and data. Of course this could be done with a nested for-loop but given 
as is for clarity. 


Template Inheritance
~~~~~~~~~~~~~~~~~~~~

You can specify a base or layout template. If the first line in a template 
call contains a BASE specifier such as 

<!-- BASE=t-layout.html -->

The template algorithm will search the path for the base 
template as specified and parses this template first.  

 
Called Template text::

    # --- Template t-mytemplate.html --------
    <!-- BASE=t-layout.html -->

    <!-- BEGIN=content -->
    <div class="conent">
    
    ... content here ...
    
    </div>
    <!-- END=content -->

    ... surrounding html ...     

    # ---------------------


Base Template text::

    # --- Template t-layout.html --------
    <!doctype html>
    <html>
    <head>...</head>
    <script type="text/javascript" src="../static/jquery.js"></script>
    <link rel="stylesheet" href="../static/style.css" type="text/css" />
    <body>
    <header> ...heading stuff... </header>
    
    $content
    
    <footer> ...footing stuff... </footer>
    </body>
    </html>

Python Code::

    # --- Python Code ----
    from templaterex import TemplateRex

    trex = TemplateRex(fname='t-mytemplate.html')

    ....
    trex.render_sec('content', context_dict)
    ....

    rendered_str = trex.render()

    # ---------------------
 

Template Includes
~~~~~~~~~~~~~~~~~

Another basic capability is to include snippets within a templates. If
during processing an include statement is encountered such as 
    
    <!- INCLUDE=t-header.html -->
    
The contents of that template are included in the calling template 
        
Function/Filters
~~~~~~~~~~~~~~~~~~~~

Functions (sometimes called filters in other template engines) calls can
be specified within the template text with the following syntax::

    &function_to_be called($args1,'arg2',kwarg1=True,kwarg2='test')

The function name (behind the &) has to be either one of the builtin functions
or a custom registered function call. If a function does not have args the 
follwing matching parenthesis are required. 

The args can either be string literals identified with quotes, True or False
booleans, integer or floating point numbers or a context variable. Context 
variables are identified with either a leading $ or just bare word - using the 
$ delimiter is faster and encouraged for clarity.  If a context variable is 
not found in the context the function call is silent. 

Functions can be easily registered in two ways. The easiest is to specify
custom functions during object creation the func_reg keyword. 

For example::  

    func_custom_dict = {'format':format, 'myfunc':myfunc}
    trex = TemplateRex(fname=fspec_template, func_reg=func_custom_dict)

Which is equivalent to::

    func_custom_dict = {'format':format, 'myfunc':myfunc}

    trex = TemplateRex()
    trex.functions.update( func_custom_dict )
    trex.get_template(fspec_template)

would register the python format function and your own custom myfunc function.
Then you could use the following in your template: 

    Voltage is: &format($voltage,'.1f')

Where voltage is a context variable and needs to be passed in the context
dictionary of the render call (either render_sec() or render() ) where the 
function is exists.  

Builtin Function/Filters
~~~~~~~~~~~~~~~~~~~~
TBD - look in functions.py for code

Options: Comment Character(s)
~~~~~~~~~~~~~~~~~~~~

HTML comment characters for specifying section blocks are the default <!-- and -->. However these are selectable. For example,
here is an object creation with different comment prefix and postfix characters options:: 

    trex = TemplateRex(fname='dhcpcd-template.conf',cmnt_prefix='##-',cmnt_postfix='-##')
    
This will parse the template looking for section blocks delimited as::

    ##- BEGIN=static_section -##
    ... section block ... 
    ##- END=static_section -##

Options: Development or Verbose Mode
~~~~~~~~~~~~~~~~~~~~

Sometimes it is convienent to see what the file source of the templates used in rendered template outputs. This mode can be selected with a dev_mode argument. For example::

    trex = TemplateRex(fname='/etc/dhcpcd-template.conf',cmnt_prefix='##-',cmnt_postfix='-##',dev_mode=True)

When the template is rendered on this object there will be commented hints about the location and section of templates used such as::    

    ##- Template:/etc/dhcpcd-template.conf Section:static_section Below -##
    interface eth0
    static ip_address=10.10.80.202/24
    static routers=10.10.80.1
    static domain_name_servers=192.168.101.210
    ##- Template:/etc/dhcpcd-template.conf Section:static_section Above -##




