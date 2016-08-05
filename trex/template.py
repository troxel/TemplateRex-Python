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
    id_prefix   = '\$'
        
    # ----------------------
    def __init__(self, **args):

        #if 'fname' in args.keys():
        #    self.fname = args['fname']
        #else: raise Exception('fname arguement required')

        self.cmnt_verbose = 1
        self.func_registered = {}

        self.tsections = {}         # template sections
        self.tsections_funcs = {}   # template section function structs    

        self.psections_str = { 'main':"", 'base':""}   # processed sections rendered str
        self.psections_lst = { 'main':[], 'base':[]}   # processed sections as lst
        self.csections = { 'main':[], 'base':[] }  # child sections
        self.last_parent = ['main']     # used to determine last found parent in recursive func
    
        self.block_pattern = self.cmnt_prefix + r'\s*BEGIN=(?P<nm>\w+)\s*' + self.cmnt_postfix + r'(?P<inner>.*?)' + self.cmnt_prefix + r'\s*END=\1 ' + self.cmnt_postfix
        self.base_pattern  = self.cmnt_prefix + r'\s*BASE=(?P<nm>\S+)\s*' + self.cmnt_postfix
        #self.func_pattern  = self.func_prefix + r'(?P<fn_nm>\S+)\((?P<fn_args>.*?)\)'
        self.func_pattern  = self.func_prefix + r'({?[a-zA-Z][\w]+}?)\((.*?)\)'
        self.id_pattern  = self.id_prefix + r'({?[a-zA-Z][\w]+}?)'
        
        self.block_re = re.compile(self.block_pattern, re.DOTALL)
        self.func_re  = re.compile(self.func_pattern)
        self.id_re    = re.compile(self.id_pattern,re.DOTALL)
        self.quotes_re = re.compile('[\'\"]')
        self.id_prefix_re = re.compile(r'^\$')

        for key in args.keys():
            self.__dict__[key] = args[key]
            
        # load template based on a search list
        self.get_template(self.fname)
       
    # ----------------------
    def get_template(self,fname):
        """ Loads a template into self.tsection """

        for dir_spec in self.template_dirs:
            fspec = os.path.join(dir_spec, fname)
            if os.path.isfile(fspec):

                # Assumes ext .html but replace twice as fast as re
                fspec_msh = fspec.replace('.html','.msh')
                if os.path.isfile(fspec_msh):
                    if os.stat(fspec_msh).st_mtime > os.stat(fspec_msh).st_mtime:
                        fid = open(fspec_msh, 'rb')
                        self.tsections = marshal.load(fid)
                        fid.close()
                else:
                    try: fid = open(fspec, 'r')
                    except: continue
                    
                    file_str = fid.read()
                    fid.close()

                    # First check for a base specifier
                    match = re.match(self.base_pattern, file_str)
                    if match:
                        fname_base = match.group('nm')
                        # Save to 'base' as this is rendered in the final render if present
                        self.tsections['main'] = self.get_template(fname_base)
                        self.tsections['main_child'] = self.parse_template(file_str)
                    else:
                        self.tsections['main'] = self.parse_template(file_str)
                    
                    # Process functions populates self.tsections_funcs
                    self.parse_functions()
                    
                    ### if compile_flg marshal tsections to fspec_msh

                break

        if not self.tsections:
            print('No Template File %s Found' % (fname),'in search path -> ', ' , '.join(self.template_dirs))
            raise

        return self.tsections['main']

    # ----------------------
    def parse_template(self, t_str):

        def parse_capture(obj):
            name_sec = obj.group(1)
            
            self.csections[name_sec] = []
            self.last_parent.append(name_sec)

            proc_rtn = self.parse_template(obj.group(2))  # recursive call group(2) is next template section

            self.last_parent.pop()
            self.csections[self.last_parent[-1]].append(name_sec)

            self.tsections[name_sec] = proc_rtn.strip()
            self.psections_str[name_sec] = ""   # need to initialize to prevent key exceptions
            self.psections_lst[name_sec] = []   # ...
            
            return "$" + name_sec

        section = self.block_re.sub(parse_capture, t_str, re.DOTALL)
        return section

    # ----------------------
    def parse_functions(self):

        # ----------------------------
        def arg_study(arg):
     
            (arg,cnt) = self.id_prefix_re.subn('',arg)
            if cnt: return arg,True
        
            (arg,cnt) = self.quotes_re.subn('',arg)
            if cnt: return arg,False
        
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
           
            if not section in self.tsections_funcs: 
                self.tsections_funcs[section] = {}
            
            self.tsections_funcs[section][slug] = {'args_ctx':[],'args':[],'args_rnd':[],'kwargs':{},'ref':func_ref}
            
            # Determine nature of the args
            arg_pos_lst = [arg for arg in arg_lst if not re.search("=",arg)]
            arg_kw_lst  = [arg for arg in arg_lst if re.search("=",arg)]
            
            for inx,arg in enumerate(arg_pos_lst):
                arg,ctx = arg_study(arg)
                self.tsections_funcs[section][slug]['args'].append(arg)
                self.tsections_funcs[section][slug]['args_rnd'].append(arg)  # rendering scratchpad
                if ctx: 
                    self.tsections_funcs[section][slug]['args_ctx'].append(inx)
                   
            # Assemble kwargs (note not facilitating context kwargs are this time)
            for arg in arg_kw_lst:
                kw,val = arg.split("=")
                val,ctx = arg_study(val)
                self.tsections_funcs[section][slug]['kwargs'][kw] = val

            return "$" + slug

        for section in self.tsections:                        
            self.tsections[section] = self.func_re.sub(parse_capture, self.tsections[section], count=1)
           
        return
            
    # ----------------------
    def render_sec(self, section, context={}):

        for child in self.csections[section]:
            self.psections_str[child] = "\n".join(self.psections_lst[child])
            self.psections_lst[child] = []
                
        if not isinstance(context, dict):
            context = context.__dict__
            
        # Optimization: if no children then no sub-sections to update   
        if self.csections[section]:
            context.update(self.psections_str)

        # Function processing
        if section in self.tsections_funcs:
            for key_slug in self.tsections_funcs[section]:
                func_args = self.tsections_funcs[section][key_slug]['args_rnd'] 
               
                for inx in self.tsections_funcs[section][key_slug]['args_ctx']:
                    func_args[inx] = context[self.tsections_funcs[section][key_slug]['args'][inx]]
                                                            
                func_kwargs = self.tsections_funcs[section][key_slug]['kwargs']
                context[key_slug] = self.tsections_funcs[section][key_slug]['ref'](*func_args,**func_kwargs)

        # Var substitution       
        if section == 'main':
            self.psections_str[section] = self.subtitute_var(self.tsections[section],context)
        else: 
            self.psections_lst[section].append( self.subtitute_var(self.tsections[section],context) ) 

        return(self.psections_str[section])

    # ----------------------
    def render(self, context={}):
        return self.render_sec("main", context)

    # ----------------------
    def subtitute_var(self, str_in, context):

        def process_capture(obj):
            try: return str(context[obj.group(1)])
            except: return "" 

        rtn = self.id_re.sub(process_capture, str_in)
        return rtn

