# -*- coding: utf-8 -*-
"""
    trex.functions
     
    Default filters
    
    To register a custom function
    
    def myfunc(arg):
        # do something with arg
        return arg
    
    trex.functions['myfunc'] = myfunc
    
    Note: borrowed some code from jinja filters since evidently 
    some of these are common use cases
"""
import pprint
from markupsafe import escape
import re

def default(value, default_value=u'', boolean=False):
    """If the value is undefined it will return the passed default value,
    otherwise the value of the variable:

    .. sourcecode

        &default($my_variable, default_value='my_variable is not defined')
        
    This will output the value of ``my_variable`` if the variable was
    defined, otherwise ``'my_variable is not defined'``. If you want
    to use default with variables that evaluate to false you have to
    set the second parameter to `true`:
    """
    if isinstance(value, Undefined) or (boolean and not value):
        return default_value
    return value

def center(value, width=80):
    """Centers the value in a field of a given width."""
    return value.center(width)

def format_float(value, specifier):
    """ Formats a variable. Refer to python docs on format specifications."""
    rtn = format(float(value),specifier)
    return rtn

def filesizeformat(value, binary=False):
    """Format the value like a 'human-readable' file size (i.e. 13 kB,
    4.1 MB, 102 Bytes, etc).  Per default decimal prefixes are used (Mega,
    Giga, etc.), if the second parameter is set to `True` the binary
    prefixes are used (Mebi, Gibi).
    """
    bytes = float(value)
    base = binary and 1024 or 1000
    prefixes = [
        (binary and 'KiB' or 'kB'),
        (binary and 'MiB' or 'MB'),
        (binary and 'GiB' or 'GB'),
        (binary and 'TiB' or 'TB'),
        (binary and 'PiB' or 'PB'),
        (binary and 'EiB' or 'EB'),
        (binary and 'ZiB' or 'ZB'),
        (binary and 'YiB' or 'YB')
    ]
    if bytes == 1:
        return '1 Byte'
    elif bytes < base:
        return '%d Bytes' % bytes
    else:
        for i, prefix in enumerate(prefixes):
            unit = base ** (i + 2)
            if bytes < unit:
                return '%.1f %s' % ((base * bytes / unit), prefix)
        return '%.1f %s' % ((base * bytes / unit), prefix)


def pprint(value, verbose=False):
    """Pretty print a variable. Useful for debugging.
    """
    return pprint.pformat(value, verbose=verbose)

def truncate(string, length=255, killwords=False, end='...'):
    """Return a truncated copy of the string. The length is specified
    with the first parameter which defaults to ``255``. If the second
    parameter is ``true`` the filter will cut the text at length. Otherwise
    it will discard the last word. If the text was in fact
    truncated it will append an ellipsis sign (``"..."``). If you want a
    different ellipsis sign than ``"..."`` you can specify it using the
    third parameter.



    .. sourcecode::

    in views.py 

    context['my_string'] = 'foo bar baz'
       
    in template    
       
        &truncate($my_string,5)
          -> "foo ..."

        &truncate($my_string,5,killwords=True)
          -> "foo ba..."

    """
    if len(string) <= length:
        return string
    elif killwords:
        return string[:length - len(end)] + end

    result = string[:length - len(end)].rsplit(' ', 1)[0]
    if len(result) < length:
        result += ' '
    return result + end

#-------------------------------------------------------
_cntr_dict = {}
#def cycler(*args,seq_id='default',reset=False,current_only=False):
def cycler(*args,**kwargs):
    
    # ugliness to remain py2 compatible
    seq_id = 'default'
    if 'seq_id' in kwargs: seq_id = kwargs['seq_id']

    reset = False 
    if 'reset' in kwargs: reset = kwargs['reset']

    current_only = False 
    if 'current_only' in kwargs: current_only = kwargs['current_only']
        
    if not seq_id in _cntr_dict: _cntr_dict[seq_id] = -1
    if reset: _cntr_dict[seq_id] = -1
    if current_only: return args[_cntr_dict[seq_id]]
                
    _cntr_dict[seq_id] += 1
    _cntr_dict[seq_id] = _cntr_dict[seq_id] % len(args)
     
    return args[_cntr_dict[seq_id]]

#-------------------------------------------------------
def dateformat(dt_obj,fmt='%Y-%m-%d'):
    return dt_obj.strftime(fmt)

#-------------------------------------------------------
def now(fmt='%Y-%m-%d'):
    """ Print the current time ie now """
    now = datetime.now()
    return now.strftime(fmt)

#-------------------------------------------------------
def nltobr(string):
    string = re.sub(r"\n","<br>\n",string,re.DOTALL)
    return string

#-------------------------------------------------------
def select_list(name,values,sel,labels={},**attr):

    #id_str = ''
    #if id: id_str = 'id="{}"'.format(id)
    attr_lst = []
    for key,val in attr.items():
       attr_lst.append('{}="{}" '.format(key,val))
    attr_str = " ".join(attr_lst)

    string = '<select name="{}" {}>\n'.format(name,attr_str)
    for val in values:
       if val in labels:
          label = labels[val]
       else:
          label = val

       selected_str = ''
       if val == sel:
          selected_str = 'SELECTED'
          print(val,sel)
          print(selected_str)
          
       string += '<option value="{}" {}> {} </option>\n'.format(val,selected_str,label)

    string += "</select>"

    return string

FUNCTIONS = {
    'center':               center,
    'default':              default,
    'filesizeformat':       filesizeformat,
    'pprint':               pprint,
    'format_float':         format_float,
    'truncate':             truncate,
    'cycler':               cycler,
    'dateformat':           dateformat,
    'nltobr':               nltobr,
    'now':                  now,
    'select_list':          select_list,
}

