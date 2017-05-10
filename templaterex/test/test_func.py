import unittest
import pprint
import sys
import os
import json

# The test object
from template import TemplateRex

fspec_template =  't-detail_functions.html'
fspec_render =  "./test_data/trender_base_functions.html"

fspec_data_flwr =  "./test_data/data_flwr.json"

# set as true to make new set to test data
tdata_make = False
if tdata_make: print("\nWarning test data be generated!\n\n")

class TestCase(unittest.TestCase):

  # --- These are the test functions
  def func_test_no_args(self):
      return "No Args"

  def func_test_1_args(self,arg1):
      return ">>>>"+arg1+"<<<<"

  def func_test_list_args(self,*args):
      string = ""
      for arg in args:
          string += ">>>" + arg + "<<<"
      return string
  #----------------------------- 

  # --- Test Case ---- 

  def test_template_base_render(self):
    trex = TemplateRex(fname=fspec_template)
    trex.func_registered = { 'func_test_no_args':self.func_test_no_args, \
                             'func_test_1_args':self.func_test_1_args,   \
                             'func_test_list_args':self.func_test_list_args }

    fid = open(fspec_data_flwr,'r')
    row_data = json.load(fid)
    fid.close()

    inc = 1
    for row in row_data[0]:
      row['inc'] = inc
      trm = trex.render_sec('row', row )
      inc += 1

    rtn = trex.render_sec('tbl')
    rtn = trex.render_sec('ftr')
    rtn = trex.render_sec('content')
    rtn_str = trex.render()

    ##print("--------------",rtn_str,"------------\n")

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
