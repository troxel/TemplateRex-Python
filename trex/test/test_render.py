import unittest
import pprint
import sys
import json

# The test object
    
sys.path.append('../')
from template import TemplateRex

fspec_template =  't-home.html'
fspec_tsections =  "./test_data/tsections.py"
fspec_render =  "./test_data/trender.html"

fspec_data_cell =  "./test_data/data_cell.json"
fspec_data_flwr =  "./test_data/data_flwr.json"

display_flg = 0
tdata_make_flg = 0

class TestCase(unittest.TestCase):

  # ----------------------------  
  def test_template_process(self):

    trex = TemplateRex(fname=fspec_template)

    if tdata_make_flg:
      fid = open( fspec_tsections  ,'w')
      pprint.pprint(trex.tsections,stream=fid)
      print("Creating ",fspec_tsections," test data")
      fid.close()

    fid = open( fspec_tsections,'r')
    tsections_str = fid.read()
    fid.close()
    self.assertTrue(trex.tsections,tsections_str)
    
  # ----------------------------  
  def test_template_render(self):
    trex = TemplateRex(fname=fspec_template)

    fid = open(fspec_data_flwr,'r')
    row_data = json.load(fid)
    fid.close()

    for row in row_data[0]:
      trm = trex.render_sec('row', row )
    rtn = trex.render_sec('tbl',{'category':'Flowers'})

    for row in row_data[1]:
      trm = trex.render_sec('row', row )
    rtn = trex.render_sec('tbl',{'category':'Fruit'})

    # Complex table with each cell rendered
    fid = open(fspec_data_cell,'r')
    cell_data = json.load(fid)
    fid.close()

    inx=0
    for cell in cell_data:
      trm = trex.render_sec('cell_complex', cell)
      inx += 1
      if not inx%4:
        trex.render_sec('row_complex')

    trex.render_sec('row_complex')
    trex.render_sec('tbl_complex')

    # Test if object is passed instead of dict type
    # -----------------------
    class User(object):

        def __init__(self, username):
            self.href = '/user/%s' % username
            self.username = username

    users = list( map(User, [u'John Doe', u'Jane Doe', u'Peter Somewhat']) )
    # -----------------------

    for user in users:
        trex.render_sec('user_sec',user)

    rtn = trex.render_sec('ftr')
    rtn_str = trex.render()

    if display_flg:
        print("-----------\n");print(rtn_str);print("-----------\n");

    if tdata_make_flg:
      fid = open( fspec_render  ,'w')
      fid.write(rtn_str)
      fid.close()
      print("Creating ",fspec_render," test data")

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
