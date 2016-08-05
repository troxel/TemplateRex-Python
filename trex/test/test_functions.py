import unittest
import pprint
import sys
import os
import json

from datetime import datetime

# The test object
sys.path.append('../')
from template import TemplateRex

fspec_template =  't-functions.html'
fspec_render =  "./test_data/trender_functions.html"

fspec_data_flwr =  "./test_data/data_flwr.json"

# set as true to make new set to test data
tdata_make = False
if tdata_make: print("\nWarning test data being generated!\n\n")

class TestCase(unittest.TestCase):

  # --- Test Case ---- 

  def test_functions(self):
    trex = TemplateRex(fname=fspec_template)

    fid = open(fspec_data_flwr,'r')
    row_data = json.load(fid)
    fid.close()

    for inc,row in enumerate(row_data[0]):
      row['inc'] = inc
      trm = trex.render_sec('row', row )

    rtn = trex.render_sec('tbl')
    
    nltxt = "This is a comment\nthat contains newlines\nand used to test a function\nThank you"
    
    now = datetime.now()
    
    rtn = trex.render_sec('content',{'title':"FLOWERS",'comment':nltxt, 'now':now})
    rtn_str = trex.render()

    print("--------------");print(rtn_str);print("------------\n");

    if tdata_make:
      fid = open( fspec_render  ,'w')
      fid.write(rtn_str)
      fid.close()
      print("\nCreating!!!!!\n ",fspec_render,"\ntest data\n")

    fid = open( fspec_render,'r')
    trender_str = fid.read()
    fid.close()

    self.assertTrue(rtn_str == trender_str)


if __name__ == '__main__':
    unittest.main()
