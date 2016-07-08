JTemplateRex
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
