# -*- coding: utf-8 -*-
"""

"""

from memory_profiler import profile

import sys
from os.path import join, dirname, abspath


from random import choice, randrange
from datetime import datetime
from timeit import Timer
from jinja2 import Environment, FileSystemLoader
from jinja2.utils import generate_lorem_ipsum

def dateformat(x):
    return x.strftime('%Y-%m-%d')

dir_root = abspath(dirname(__file__))

jinja_env = Environment(loader=FileSystemLoader(join(dir_root, 'jinja_templates')))
jinja_env.filters['dateformat'] = dateformat

# -----------------------------------------------------
# Generate some random "battery" data
battery_status = []
for inx in range(200):
    status = {"volt":randrange(1,25)/10,"temp":randrange(50,120)}
    battery_status.append(status)
# -----------------------------------------------------

#print(jinja_template.render(context))
#sys.exit()

##pprint(context)
##pprint(context['users'][0].href)

break_row = 10
context = dict(battery_status=battery_status,break_rows=range(1,break_row+1))

jinja_template = jinja_env.get_template('jinja_battery_filter.html')
# -----------------------------------------------------
@profile
def test_jinja():
    return jinja_template.render(context)
# -----------------------------------------------------

rtn = test_jinja(); 
#print(rtn); 
sys.exit()
