# -*- coding: utf-8 -*-
"""
    Benchmark against Jinja2 template engine to gauge the effect of 
    various coding changes. 

"""
import sys
from os.path import join, dirname, abspath

try:
    from cProfile import Profile
except ImportError:
    from profile import Profile

from pstats import Stats

from random import choice, randrange
from datetime import datetime
from timeit import Timer
from jinja2 import Environment, FileSystemLoader
from jinja2.utils import generate_lorem_ipsum

# -- relative location -- 
import sys
sys.path.append("../trex")
from template import TemplateRex 
# -----------------------

import pprint
pp = pprint.PrettyPrinter(indent=4)

def dateformat(x):
    return x.strftime('%Y-%m-%d')

dir_root = abspath(dirname(__file__))

jinja_env = Environment(loader=FileSystemLoader(join(dir_root, 'jinja_templates')))
jinja_env.filters['dateformat'] = dateformat

# -----------------------------------------------------
# Generate some random "battery" data
battery_status = []
for inx in range(200):
    status = {"volt":randrange(1,25)/10,"temp":randrange(50,120),"id":randrange(100000,200000)}
    battery_status.append(status)
# -----------------------------------------------------

#print(jinja_template.render(context))
#sys.exit()

break_row = 10
dtnow = datetime.now()
context = dict(battery_status=battery_status,break_row=break_row,dt=dtnow)

# *** jinja **** 
# -----------------------------------------------------
jinja_template = jinja_env.get_template('jinja_index.html')
def test_jinja():
    return jinja_template.render(context)
# -----------------------------------------------------

# *** trex **** 
# -----------------------------------------------------
trex = TemplateRex(fname='trex-index.html',template_dirs=['./trex_templates'])
def test_trex():
  
    for index in range(1,break_row+1):
        trex.render_sec("caption_cell", {"index":index} )
    
    cnt=0
    for status in battery_status:
        cnt += 1
        status['cell_class'] =  'low'
        if status['volt'] > 2:  status['cell_class'] =  'high'
        elif status['volt'] > 1: status['cell_class'] =  'med'
        
        trex.render_sec("batt_cell", status )
        if not ( cnt % break_row):
           trex.render_sec("batt_row",{"order":(cnt-break_row)})
   
    trex.render_sec('body')
    return trex.render(context)
# -----------------------------------------------------

#rtn = test_jinja(); print(rtn); sys.exit()
#rtn = test_trex();  print(rtn); sys.exit()

if __name__ == '__main__':
    sys.stdout.write('Benchmark:\n')
    for test in 'trex','jinja':
        t = Timer(setup='from __main__ import test_%s as bench' % test,
                  stmt='bench()')
        sys.stdout.write(' >> %-20s<running>' % test)
        sys.stdout.flush()
        sys.stdout.write('\r    %-20s%.4f seconds\n' % (test, t.timeit(number=250) / 250))

    if '-p' in sys.argv:
        print('Jinja profile')
        p = Profile()
        p.runcall(test_jinja)
        stats = Stats(p)
        stats.sort_stats('time', 'calls')
        stats.print_stats()

        print('trex profile')
        p = Profile()
        p.runcall(test_trex)
        stats = Stats(p)
        stats.sort_stats('time', 'calls')
        stats.print_stats()
