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
from datetime import datetime
from timeit import Timer

import re

str_in = "{yo} {yo1} Ths is a test {name} here {that} and {more} and yet {morethis} double on {day} which is {beer} with {ing}"
#str_in = str_in + " " + str_in + " " + str_in + " " + str_in
contxt = {'name':"Joe",'that':"howdy",'more':"good stuff",'morethis':"yet more",'day':"Friday",'beer':"IPA",'ing':"hops",'yo':"",'yo1':""}
contxt_copy = contxt.copy()
contxt_default = {'name':"",'that':"",'more':"",'morethis':"",'yo':"",'day':"",'beer':"",'ing':"",'yo':"",'yo1':""}
key_lst = ['yo','yo1','name','that','more','morethis','yo','day','beer','ing','name1']


id_re     = re.compile(r'{([^}]+)}', re.DOTALL)

def sub_var():

        def process_capture(obj):
            try: return str(contxt[obj.group(1)])
            except: return "" 

        rtn = id_re.sub(process_capture, str_in)
        return rtn

######################
# Really really slow        
#import string

#class BlankFormatter(string.Formatter):
#    def __init__(self, default=''):
#        self.default=default

#    def get_value(self, key, args, kwds):
#        if isinstance(key, str):
#            return kwds.get(key, self.default)
#        else:
#            Formatter.get_value(key, args, kwds)
#fmt=BlankFormatter()
#rtn = fmt.format(str_in,**contxt)
#########################        
        
######################
# Not bad speed wise 
# Ratio 2.6901708174699337 vs ~5
# doesn't work with python2
#class format_dict(dict):
#    def __missing__(self, key):
#        return "..."
#spec_dict = format_dict(contxt)
#rtn = str_in.format(**spec_dict)

######################
 
 
######################
# Ratio 2.207058711959082
# doesn't work with python2
#from collections import defaultdict 
#        def dfl():
#            return ""
        
#        d = defaultdict(dfl, contxt)
#        rtn = str_in.format(**d)
######################
        
def fmt_var():
    
        try: rtn = str_in.format(**contxt)
        except: 
            #print('e')
            #contxt_copy.update({ k:"" for k in key_lst if k not in contxt}) # ratio 2.1
            #rtn = str_in.format(**contxt_copy)
            
            # !Winner! ratio 2.7 works with python2
            # Compared to ratio 4 when the try does not fail roughly 30% faster 
            contxt_default.update(contxt) 
            rtn = str_in.format(**contxt_default)
            
        return rtn
        
print(sub_var())    
print(fmt_var())    
 
 
if __name__ == '__main__':
    tm = {}   
    sys.stdout.write('Benchmark:\n')
    for test in 'sub_var','fmt_var':
        t = Timer(setup='from __main__ import %s as bench' % test,
                  stmt='bench()')
        sys.stdout.write(' >> %-20s<running>' % test)
        sys.stdout.flush()
        tm[test] = t.timeit(number=1750)
        sys.stdout.write('\r    %-20s%.9f seconds\n' % (test, tm[test] / 1750))

    print("Ratio",tm['sub_var']/tm['fmt_var'])


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
