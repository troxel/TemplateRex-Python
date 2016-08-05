# -*- coding: utf-8 -*-
"""
    Benchmark against Jinja2 template engine to gauge the effect of 
    various coding changes. 
"""

from memory_profiler import profile

import sys
from os.path import join, dirname, abspath

from random import choice, randrange

# -- relative location -- 
import sys
sys.path.append("../trex")
from template import TemplateRex 
# -----------------------

#from pprint import pprint

dir_root = abspath(dirname(__file__))

# -----------------------------------------------------
# Generate some random "battery" data
battery_status = []
for inx in range(200):
    status = {"volt":randrange(1,25)/10,"temp":randrange(50,120)}
    battery_status.append(status)
# -----------------------------------------------------

break_row = 10
context = dict(battery_status=battery_status,break_rows=range(1,break_row+1))

trex = TemplateRex(fname='trex-battery_filter.html',template_dirs=['./trex_templates'])
# -----------------------------------------------------
@profile
def test_trex():

    for index in range(1,break_row+1):
        trex.render_sec("caption_cell", {"index":index} )
    
    loop_count = 1
    
    context['battery_status'] = sorted( context['battery_status'],key=lambda k: k['volt'] )
    
    for status in context['battery_status']:
        if status['volt'] > 2:    status['cell_class'] =  'high'
        elif status['volt'] > 1:  status['cell_class'] =  'med'
        elif status['volt'] <= 1: status['cell_class'] =  'low'
        
        status['temp'] = round(status['temp'])
        status['volt'] = round(status['volt'],1)
        
        trex.render_sec("battery_cell", status )
        if not (loop_count % break_row):
            trex.render_sec("battery_row",{"order":loop_count-break_row})
    
        loop_count += 1
   
    trex.render_sec('body')

    return trex.render()
# -----------------------------------------------------

rtn = test_trex();  
#print(rtn); 
sys.exit()

