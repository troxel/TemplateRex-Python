import os
import os.path
import sys
import re
#from string import Template

import fnmatch
import pprint
import marshal

pp = pprint.PrettyPrinter(indent=4)

class TemplateRex:
    
    template_dirs = ["./", "./templates", '/']
    
    cmnt_prefix = '<!--'
    cmnt_postfix = '-->'
    func_prefix = '&'
    id_pattern  = r'\$({?[a-zA-Z][\w]+}?)'
        
       # ----------------------
    def __init__(self, **args):

        #if 'fname' in args.keys():
        #    self.fname = args['fname']
        #else: raise Exception('fname arguement required')

        self.cmnt_verbose = 1
        self.func_registered = {}

        self.tsections = {}                        # template sections
        self.psections_str = { 'main':"", 'base':""}   # processed sections rendered str
        self.psections_lst = { 'main':[], 'base':[]}   # processed sections as lst
        self.csections = { 'main':[], 'base':[] }  # child sections
        self.last_parent = ['main']     # used to determine last found parent in recursive func

        self.block_pattern = self.cmnt_prefix + r'\s*BEGIN name=(?P<nm>\w+)\s*' + self.cmnt_postfix + r'(?P<inner>.*?)' + self.cmnt_prefix + r'\s*END name=\1 ' + self.cmnt_postfix
        self.base_pattern  = self.cmnt_prefix + r'\s*BASE name=(?P<nm>\S+)\s*' + self.cmnt_postfix
        self.func_pattern  = self.func_prefix + r'(?P<fn_nm>\S+)\((?P<fn_args>.*?)\)'
        self.block_re = re.compile(self.block_pattern, re.DOTALL)
        self.func_re  = re.compile(self.func_pattern)
        self.id_re    = re.compile(self.id_pattern,re.DOTALL)

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
                        self.tsections['main_child'] = self.process_template(file_str)
                    else:
                        self.tsections['main'] = self.process_template(file_str)
                    
                    # if compile_flg marshal tsections to fspec_msh

                break

        if not self.tsections:
            print('No Template File %s Found' % (fname),'in search path -> ', ' , '.join(self.template_dirs))
            raise

        return self.tsections['main']

    # ----------------------
    def process_template(self, t_str):

        def process_capture(obj):

            name_sec = obj.group(1)
            print(name_sec)

            self.csections[name_sec] = []
            self.last_parent.append(name_sec)

            proc_rtn = self.process_template(obj.group(2))  # recursive call group(2) is next template section

            self.last_parent.pop()
            self.csections[self.last_parent[-1]].append(name_sec)

            self.tsections[name_sec] = proc_rtn.strip()
            self.psections_str[name_sec] = ""   # need to initialize to prevent key exceptions
            self.psections_lst[name_sec] = []   # ...
            
            return "$" + name_sec

        section = self.block_re.sub(process_capture, t_str, re.DOTALL)
        return section

    # ----------------------
    def render_sec(self, section, context={}):

        for child in self.csections[section]:
            self.psections_str[child] = "".join(self.psections_lst[child])
            self.psections_lst[child] = []
        
        if not isinstance(context, dict):
            context = context.__dict__
            
        context.update(self.psections_str)

        if section == 'main':
            self.psections_str[section] = self.subtitute_var(self.tsections[section],context)
        else: 
            self.psections_lst[section].append( self.subtitute_var(self.tsections[section],context) ) 

        if self.func_registered:
            self.subtitute_functions(section)

        return(self.psections_str[section])

    # ----------------------
    def render(self, context={}):
        return self.render_sec("main", context)

    # ----------------------
    def subtitute_functions(self, section):

        def process_capture(obj):
            
            rtn = ""
            func_name = obj.group(1)
            if func_name in self.func_registered:
                args = obj.group(2)
                if args:
                  arg_lst = args.split(',')
                  rtn = self.func_registered[func_name](*arg_lst)
                else:
                  rtn = self.func_registered[func_name]()

            return rtn

        self.psections_str[section] = self.func_re.sub(process_capture, self.psections_str[section], re.DOTALL)

    # ----------------------
    def subtitute_var(self, str_in, context):

        def process_capture(obj):
          
            # Invariably somone will send non str value... 
            try: substitute = str(context[obj.group(1)])
            except: substitute = "" 

            return substitute

        rtn = self.id_re.sub(process_capture, str_in, re.DOTALL)
        return rtn

