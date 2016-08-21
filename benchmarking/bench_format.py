import re
import sys
from timeit import Timer

from pstats import Stats
from datetime import datetime

ctx = {'what':3,'verb':1,'verb1':2,'verb2':3,'verb3':'ran','verb4':'ran','verb5':'ran','verb6':'ran','verb7':'ran'}

string_fmt = """string to replace things the little {what} {verb:.2f} over"""
string_sub = """string to replace things the little $what $verb over"""


def parse_fmt():
    string = string_fmt.format(**ctx)
    return string

#string = parse_fmt();print(string)

id_pattern = r'\$([a-zA-Z][\w]+)'
id_re      = re.compile(id_pattern,re.DOTALL)

def parse_sub():
    def process_capture(obj):
        try: return str(format(ctx[obj.group(1)],'.2f'))
        except: return ""

    rtn = id_re.sub(process_capture, string_sub)
    #print(rtn)
    return rtn

def parse_parts():
    #rtn = "string to replace things the little " + str(ctx['what']) + " " + str(ctx['verb']) + " over"
    str_lst = ("string to replace things the little ",'what'," ",'verb'," over")

    _str = str

    rtn = ""
    for i,s in enumerate(str_lst):
        if i % 2:
            rtn = rtn + _str(format(ctx[s],'.2f'))
        else:
            rtn = rtn + s

    return rtn

#string = parse_parts(); print(string); sys.exit(0)
#string = parse_sub(); print(string)

tm={}
for test in 'parse_fmt','parse_sub', 'parse_parts':
        t = Timer(setup='from __main__ import %s as bench' % test, stmt='bench()')
        sys.stdout.write(' >> %-20s<running>' % test)
        sys.stdout.flush()

        tm[test] = t.timeit(number=2750)
        sys.stdout.write('\r    %-20s%.9f seconds\n' % (test, tm[test] / 10000))

sys.stdout.write('Ratio    %.2f seconds\n' % (tm['parse_sub'] / tm['parse_fmt']) )

