import os
import os.path
import sys
import re

import fnmatch
import pprint
import marshal
import functions

pp = pprint.PrettyPrinter(indent=4)

class TemplateRex:
    
    template_dirs = ["./", "./templates", '/']
    
    cmnt_prefix = '<!--'
    cmnt_postfix = '-->'
    func_prefix = '&'
    
    fld_struct = {'default':{'pre':'$','fld':'([a-zA-Z_]\w*)','post':''}, 
                  'pyfmt':  {'pre':'{', 'fld':'([a-zA-Z_][\S]*?)','post':'}'} }

    # ----------------------
    def __init__(self, **args):

        #if 'fname' in args.keys():
        #    self.fname = args['fname']
        #else: raise Exception('fname arguement required')

        self.cmnt_verbose = 1
    
        self.tblks={}
 
        self.pblks_str = { 'BLK_MAIN':""}   # processed sections rendered str
        self.pblks_lst = { 'BLK_MAIN':[]}   # processed sections as lst
        self.cblks     = { 'BLK_MAIN':[]}  # child sections
        self.last_parent = ['BLK_MAIN']     # used to determine last found parent in recursive func
    
        self.block_pattern = self.cmnt_prefix + r'\s*BEGIN=(?P<nm>\w+)\s+(?P<opt>[\w=,]+)?\s*' + self.cmnt_postfix + r'(?P<blk>.*?)' + self.cmnt_prefix + r'\s*END=\1 ' + self.cmnt_postfix
        self.incl_pattern  = self.cmnt_prefix + r'\s*INCLUDE=(?P<nm>\w[\w.\-]+\w)\s*' + self.cmnt_postfix
        self.base_pattern  = self.cmnt_prefix + r'\s*BASE=(?P<nm>\w+[\w\-.]+)\s*' + self.cmnt_postfix
        self.func_pattern  = self.func_prefix + r'({?[a-zA-Z][\w]+}?)\((.*?)\)'
        
        self.block_re  = re.compile(self.block_pattern, re.DOTALL)
        self.func_re   = re.compile(self.func_pattern)
        self.incl_re   = re.compile(self.incl_pattern)
        self.quotes_re = re.compile('[\'\"]')

        for key in self.fld_struct:
            fld = self.fld_struct[key]
            fld['re'] = re.compile(  re.escape(fld['pre']) + fld['fld']+ fld['post'], re.DOTALL )
     
        self.fld = self.fld_struct['default'] 
       
        self.BLK_MAIN_pre  = "{0} {1} {2}".format(self.cmnt_prefix,"BEGIN=BLK_MAIN",self.cmnt_postfix)
        self.BLK_MAIN_post = "{0} {1} {2}".format(self.cmnt_prefix,"END=BLK_MAIN",self.cmnt_postfix)

        for key in args.keys():
            self.__dict__[key] = args[key]
            
        # load template based on a search list
        self.get_template(self.fname)
        
        """
        print("***********")
        pp.pprint(self.tblks)
        pp.pprint(self.cblks)
        print("***********")
        sys.exit()
        """
    # ----------------------
    def get_template(self,fname):
        """ Loads a template into self.tsection """
        fspec = self.search_template(fname)
        
        fspec_cmp = re.sub('\.\w+$','pyc',fspec)
        if os.path.isfile(fspec_cmp):
            if os.stat(fspec_cmp).st_mtime > os.stat(fspec).st_mtime:
                try: 
                    fid = open(fspec_cmp, 'rb')
                    self.tblks = marshal.load(fid)
                    fid.close()
                    return(self.tblks)
                except: 
                    print('Error reading compiled template File {0}'.format(fspec_cmp))
                    raise
                    
        try: 
            fid = open(fspec, 'r') 
            file_str = fid.read()
            fid.close()
        except: 
            print('Error reading template File {0}'.format(fspec_cmp))
            raise
             
        # Check for includes 
        def incl_capture(obj):
            fname_incl = obj.group('nm')
            fspec_incl = self.search_template(fname_incl)
            try: 
                fid = open(fspec_incl, 'r') 
                incl_str = fid.read()
                fid.close()
            except: 
                print('Error reading include template File {0}'.format(fspec_incl))
                raise
                    
            return(incl_str)        
        file_str = self.incl_re.sub(incl_capture, file_str, re.DOTALL)
               
        # Check for a base specifier
        match = re.match(self.base_pattern, file_str)
        if match:
             fname_base = match.group('nm')
             self.get_template(fname_base)
             self.parse_template(file_str)
        else:
             # If main template wrap in a main block for parse_template
             file_str = self.BLK_MAIN_pre + file_str + self.BLK_MAIN_post
             self.parse_template(file_str)
         
        # Process functions populates self.tblks[blk_name]['funcs']
        self.parse_functions()

        if not self.tblks:
            print('No Template File %s Found' % (fname),'in search path -> ', ' , '.join(self.template_dirs))
            raise
        return(self.tblks)

    # ----------------------
    def search_template(self,fname):
        for dir_spec in self.template_dirs:
            fspec = os.path.join(dir_spec, fname)
            if os.path.isfile(fspec):
                return(fspec)
        print('No Template File {0} Found in search path {1}'.format(fname), ','.join(self.template_dirs))
        raise

    # ----------------------
    def parse_template(self, t_str):

        def parse_capture(obj):
            blk_name = obj.group('nm')
            
            self.cblks[blk_name] = []
            self.last_parent.append(blk_name)

            proc_rtn = self.parse_template(obj.group('blk'))  # recursive call group(2) is next template section

            #if obj.group('opt'): print("******");print(obj.group('opt'));

            self.last_parent.pop()
            self.cblks[self.last_parent[-1]].append(blk_name)

            # Assign and init to template blk structure  
            self.tblks[blk_name] = {}
            
            self.tblks[blk_name]['blk_str'] = proc_rtn.lstrip()
            self.tblks[blk_name]['flds'] = self.fld['re'].findall(self.tblks[blk_name]['blk_str'])  
            self.tblks[blk_name]['funcs'] = {}

            self.pblks_str[blk_name] = ""   # need to initialize to prevent key exceptions
            self.pblks_lst[blk_name] = []   # ...
            
            return self.fld['pre'] + blk_name + self.fld['post']
       
        blk = self.block_re.sub(parse_capture, t_str, re.DOTALL)
        return blk
        
    # ----------------------
    def parse_functions(self):

        # ----------------------------
        def arg_study(arg):
     
            (arg,cnt) = self.fld['re'].subn('',arg)
            if cnt: return arg,True                 # context
        
            (arg,cnt) = self.quotes_re.subn('',arg)
            if cnt: return arg,False                # not context 
        
            if arg == 'False': return(False,False)
            if arg == 'True':  return(True,False)
                    
            try: return int(arg),False
            except: pass

            try: return float(arg),False
            except: pass
    
            return arg,False

        def parse_capture(obj):

            func_name = obj.group(1)
            arg_str = obj.group(2)

            # Create unique slug name
            arg_lst = re.split('\s*,\s*',arg_str)
            arg_slug = "_".join(arg_lst)   
            slug = "FUNC_" + func_name + "_" + arg_slug    
            slug = re.sub('\W+',"",slug)

            func_ref = functions.FUNCTIONS[func_name]   # Should we check if exists or just default to something?
            
            self.tblks[blk_name]['funcs'][slug] = {'args_ctx':[],'args':[],'args_rnd':[],'kwargs':{},'ref':func_ref}
            
            # Determine nature of the args
            arg_pos_lst = [arg for arg in arg_lst if not re.search("=",arg)]
            arg_kw_lst  = [arg for arg in arg_lst if re.search("=",arg)]
            
            for inx,arg in enumerate(arg_pos_lst):
                arg,ctx = arg_study(arg)
                self.tblks[blk_name]['funcs'][slug]['args'].append(arg)
                self.tblks[blk_name]['funcs'][slug]['args_rnd'].append(arg)  # rendering scratchpad
                if ctx: 
                    self.tblks[blk_name]['funcs'][slug]['args_ctx'].append(inx)
                   
            # Assemble kwargs (note not facilitating context kwargs at this time)
            for arg in arg_kw_lst:
                kw,val = arg.split("=")
                val,ctx = arg_study(val)
                self.tblks[blk_name]['funcs'][slug]['kwargs'][kw] = val

            return self.fld['pre'] + slug + self.fld['post']
        
        for blk_name in self.tblks:                 
            self.tblks[blk_name]['blk_str'] = self.func_re.sub(parse_capture, self.tblks[blk_name]['blk_str'] )

        return
            
    # ----------------------
    def render_sec(self, blk, context={}):
        if not blk in self.tblks: 
            print("Warning no blk",blk,"found in template")
            return
                            
        if not isinstance(context, dict):
            context = context.__dict__
            
        # Optimization: if no children then no sub-blks to update   
        if self.cblks[blk]:
            context.update(self.pblks_str)

        for child in self.cblks[blk]:
            self.pblks_str[child] = ""
            self.pblks_lst[child] = []

        # Function processing
        for slug in self.tblks[blk]['funcs']:
            func_args = self.tblks[blk]['funcs'][slug]['args_rnd'] 
               
            for inx in self.tblks[blk]['funcs'][slug]['args_ctx']:
                func_args[inx] = context[self.tblks[blk]['funcs'][slug]['args'][inx]]
                                                            
            func_kwargs = self.tblks[blk]['funcs'][slug]['kwargs']
            context[slug] = self.tblks[blk]['funcs'][slug]['ref'](*func_args,**func_kwargs)

        self.pblks_str[blk] = self.pblks_str[blk] + self.fld['subst']( self, self.tblks[blk]['blk_str'], context )
            
        return(self.pblks_str[blk])

    # ----------------------
    def render(self, context={}):
        return self.render_sec('BLK_MAIN', context)

    # ----------------------
    def substitute_fmt(self, str_in, context):

        rtn = str_in.format(**context)
        return rtn
    fld_struct['pyfmt']['subst'] = substitute_fmt

    # ----------------------
    def substitute_re(self, str_in, context):
        _str = str
        def process_capture(obj):
            try: return _str(context[obj.group(1)])
            except: return "" 

        rtn = self.fld['re'].sub(process_capture, str_in)
        return rtn
    fld_struct['default']['subst'] = substitute_re
