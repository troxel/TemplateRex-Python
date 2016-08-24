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
display_flg = False
tdata_make_flg = False

class TestCase(unittest.TestCase):

  # --- Test Case ---- 

  def test_functions(self):
 
    func_custom = {'format':format}
      
    #trex = TemplateRex(fname=fspec_template,func_reg=func_custom)
     
    trex = TemplateRex()
    trex.functions.update( func_custom )
    trex.get_template(fspec_template)
     
     
    fid = open(fspec_data_flwr,'r')
    row_data = json.load(fid)
    fid.close()

    for inc,row in enumerate(row_data[0]):
      row['inc'] = inc
      trm = trex.render_sec('row', row )

    rtn = trex.render_sec('tbl')
       
    nltxt = "This is a comment\nthat contains newlines\nand used to test a function\nThank you"
    
    now = datetime.now()
    
    rtn = trex.render_sec('content',{'title':"FLOWERS",'comment':nltxt, 'now':now, 'voltage':54.3123})
    rtn_str = trex.render()

    if display_flg:
        print("--------------");print(rtn_str);print("------------\n");

    if tdata_make_flg:
      fid = open( fspec_render  ,'w')
      fid.write(rtn_str)
      fid.close()
      print("\nCreating!!!!!\n ",fspec_render,"\ntest data\n")

    fid = open( fspec_render,'r')
    trender_str = fid.read()
    fid.close()

    self.assertTrue(rtn_str == trender_str)


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        arg1 = sys.argv.pop()
        if arg1 == '-d':
            display_flg = 1
        if arg1 == '-m':
            tdata_make_flg = 1
    
    unittest.main()
