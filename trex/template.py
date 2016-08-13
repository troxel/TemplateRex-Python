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
        
    # ----------------------
    def __init__(self, **args):

        #if 'fname' in args.keys():
        #    self.fname = args['fname']
        #else: raise Exception('fname arguement required')

        self.cmnt_verbose = 1
    
        self.tblks={}
 
        self.pblks_str = { 'BLK_MAIN':"", 'base':""}   # processed sections rendered str
        self.pblks_lst = { 'BLK_MAIN':[], 'base':[]}   # processed sections as lst
        self.cblks = { 'BLK_MAIN':[], 'base':[] }  # child sections
        self.last_parent = ['BLK_MAIN']     # used to determine last found parent in recursive func
    
        self.block_pattern = self.cmnt_prefix + r'\s*BEGIN=(?P<nm>\w+)\s*' + self.cmnt_postfix + r'(?P<inner>.*?)' + self.cmnt_prefix + r'\s*END=\1 ' + self.cmnt_postfix
        self.base_pattern  = self.cmnt_prefix + r'\s*BASE=(?P<nm>\S+)\s*' + self.cmnt_postfix
        self.func_pattern  = self.func_prefix + r'({?[a-zA-Z][\w]+}?)\((.*?)\)'
        
        self.block_re  = re.compile(self.block_pattern, re.DOTALL)
        self.func_re   = re.compile(self.func_pattern)
        self.fld_re     = re.compile(r'{(\w+)\S*?}', re.DOTALL)
        self.quotes_re = re.compile('[\'\"]')

        self.BLK_MAIN_pre  = "{0} {1} {2}".format(self.cmnt_prefix,"BEGIN=BLK_MAIN",self.cmnt_postfix)
        self.BLK_MAIN_post = "{0} {1} {2}".format(self.cmnt_prefix,"END=BLK_MAIN",self.cmnt_postfix)

        for key in args.keys():
            self.__dict__[key] = args[key]
            
        # load template based on a search list
        self.get_template(self.fname)
        
        #print("***********")
        #pp.pprint(self.tblks)
        #pp.pprint(self.cblks)
        #print("***********")
        #sys.exit()
       
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
                        self.tblks = marshal.load(fid)
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
                        self.get_template(fname_base)
                        self.parse_template(file_str)
                    else:
                        # If main template wrap in a main block for parse_template
                        template_str = "{0}\n{1}\n{2}\n".format(self.BLK_MAIN_pre,file_str,self.BLK_MAIN_post)
                        self.parse_template(template_str)
                    
                    # Process functions populates self.tblks[blk_name]['funcs']
                    self.parse_functions()
                    
                    ### if compile_flg marshal tsections to fspec_msh

                break

        if not self.tblks:
            print('No Template File %s Found' % (fname),'in search path -> ', ' , '.join(self.template_dirs))
            raise

    # ----------------------
    def parse_template(self, t_str):

        def parse_capture(obj):
            blk_name = obj.group(1)
            
            self.cblks[blk_name] = []
            self.last_parent.append(blk_name)

            proc_rtn = self.parse_template(obj.group(2))  # recursive call group(2) is next template section

            self.last_parent.pop()
            self.cblks[self.last_parent[-1]].append(blk_name)

            # Assign and init to template blk structure  
            self.tblks[blk_name] = {}
            
            self.tblks[blk_name]['blk_str'] = proc_rtn.strip()
            self.tblks[blk_name]['flds'] = self.fld_re.findall(self.tblks[blk_name]['blk_str'])  
            self.tblks[blk_name]['funcs'] = {}

            self.pblks_str[blk_name] = ""   # need to initialize to prevent key exceptions
            self.pblks_lst[blk_name] = []   # ...
            
            return "{" + blk_name + "}"

        blk = self.block_re.sub(parse_capture, t_str, re.DOTALL)
        return blk
        
    # ----------------------
    def parse_functions(self):

        # ----------------------------
        def arg_study(arg):
     
            (arg,cnt) = self.fld_re.subn('',arg)
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

            return "{" + slug + "}"
        
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
            #self.pblks_str[child] = "\n".join(self.pblks_lst[child])
            self.pblks_str[child] = ""
            self.pblks_lst[child] = []


        # Function processing
        for slug in self.tblks[blk]['funcs']:
            func_args = self.tblks[blk]['funcs'][slug]['args_rnd'] 
               
            for inx in self.tblks[blk]['funcs'][slug]['args_ctx']:
                func_args[inx] = context[self.tblks[blk]['funcs'][slug]['args'][inx]]
                                                            
            func_kwargs = self.tblks[blk]['funcs'][slug]['kwargs']
            context[slug] = self.tblks[blk]['funcs'][slug]['ref'](*func_args,**func_kwargs)

        # Fld substitution
        if blk == 'BLK_MAIN':
            self.pblks_str[blk] = self.subtitute_fld(self.tblks[blk]['blk_str'],context)
        else: 
            #self.pblks_lst[blk].append( self.subtitute_fld(self.tblks[blk]['blk_str'],context) ) 
            self.pblks_str[blk] += self.subtitute_fld(self.tblks[blk]['blk_str'],context) 
            
        return(self.pblks_str[blk])

    # ----------------------
    def render(self, context={}):
        return self.render_sec('BLK_MAIN', context)

    # ----------------------
    def subtitute_fld(self, str_in, context):

        rtn = str_in.format(**context)
        return rtn

# ----------------------
    def subtitute_var(self, str_in, context):
        _str = str
        def process_capture(obj):
            try: return _str(context[obj.group(1)])
            except: return "" 

        rtn = self.id_re.sub(process_capture, str_in)
        return rtn

