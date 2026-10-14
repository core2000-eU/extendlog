#Copyright (c) 2026 Benjamin Winter
#This file is part of extendlog which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/extendlog for full license details.

#DESCRIPTION
#extendlog, a Python module providing customized, high-level logging functions.

#imports
import                              time
import                              collections
import                              queue
import                              traceback
import                              io
import                              copy

#custom exceptions
class exceptions:
    """
    brief for details, see the docs at https://github.com/core2000-eU/extendlog
    """
    class RuntimeExceptionsExceeded(Exception):
        def __init__(self,error,runtime_exc_buffer,runtime_exc_bufferAsStr): super().__init__(error); self.error=error; self.is_exception_from_extendlog=True; self.runtime_exc_buffer=runtime_exc_buffer; self.runtime_exc_bufferAsStr=runtime_exc_bufferAsStr
        def __str__(self): return f"{self.error}"
        
#backend
class backend:
    def exception_handle(self,funcname,e,debug_str="",to_std=False):
        """
        brief internal function for printing exceptions
        param [self] OBJ
        param [funcname] STR
        param [e] OBJ the Exception
        param [debug_str] STR optional debug string to include in the exception
        param [to_std] BOOL immediately print to stdout
        returns [] None
        """
        #print
        if(to_std):
            temp_buff=io.StringIO()
            traceback.print_exception( e,file=temp_buff )
            temp_buff=temp_buff.getvalue()
            if(debug_str):  print( f"terminal-only output: extendlog: {funcname} raised Exception (see below; for debugging: {debug_str})" )
            else:           print( f"terminal-only output: extendlog: {funcname} raised Exception (see below)" )
            print( temp_buff )
        #append, raise
        backend.exception_append( self,e )
    def exception_append(self,e):
        """
        brief internal function to append exceptions to runtime_exc_buffer and runtime_exc_bufferAsStr
        param [self] OBJ
        param [e] OBJ the Exception
        returns [] None
        """
        #prepare
        temp_buff=io.StringIO()
        traceback.print_exception( e,file=temp_buff )
        temp_buff=temp_buff.getvalue()
        #append
        self.runtime_exc_buffer.append(e)
        self.runtime_exc_bufferAsStr.append(temp_buff)
        #exceeded
        if( self.runtime_exc_raise ) and ( len(self.runtime_exc_buffer)>self.runtime_exc_max ):
            self.exit(wait=False) #ensure proper immediate exit
            raise exceptions.RuntimeExceptionsExceeded(f"extendlog: too many runtime exceptions occured; this exception's [runtime_exc_buffer] and [runtime_exc_bufferAsStr] attributes hold a LIST of the exceptions",self.runtime_exc_buffer,self.runtime_exc_bufferAsStr)
    def shutdown_writeLogfileThread(self,is_exc):
        """
        brief internal function to properly handle emergency shutdown of write_logfile_thread()
        param [self] OBJ
        param [is_exc] BOOL Is the function called from an exception state? Handles I/O differently
        returns [] None
        """
        #to ensure proper shutdown, call task_done() a few times:
        try:
            for i in range(self.queue_logfile.qsize()*2): self.queue_logfile.task_done()
            if(is_exc): print(f"extendlog: logging.backend.shutdown_writeLogfileThread(): shutdown of tasks done")
        except:
            pass
    def shutdown_writeStdoutThread(self,is_exc):
        """
        brief internal function to properly handle emergency shutdown of write_stdout_thread()
        param [self] OBJ
        param [is_exc] BOOL Is the function called from an exception state? Handles I/O differently
        returns [] None
        """
        #to ensure proper shutdown, call task_done() a few times:
        try:
            for i in range(self.queue_stdout.qsize()*2): self.queue_stdout.task_done()
            if(is_exc): print(f"extendlog: logging.backend.shutdown_writeStdoutThread(): shutdown of tasks done")
        except:
            pass
    def debug_handle(self,str_in,level=7):
        """
        brief internal function to handle debug messages
        param [self] OBJ
        param [str_in] STR
        param [level] INT the loglevel to use
        returns [] None
        """
        #stdout
        try:
            if(self.debug):     print( f"terminal-only output: extendlog: DEBUG: debugging message: {str_in}" )
        except: pass #ignore
        #file, 514
        try:
            if(self.debug):     self.log("extendlog", "DEBUG", f"debugging message: {str_in}",level=level,nonewlines=True,to_std=False,to_file=True,to_514=True)
        except: pass
    def checkparam_log(self,caller,logid,serial,level,status,texttolog,nonewlines,timenow,to_std,to_file,to_514):
        """
        brief internal function check parameters on function call
        param [**] self-describing
        returns [] None
        """
        temp_str_prepend=f"extendlog: logging.log(): "
        temp_str_debug=f" (for debugging: function called with parameters: log({backend.reconstr_func_param(caller=caller,logid=logid,serial=serial,level=level,status=status,texttolog=texttolog,nonewlines=nonewlines,timenow=timenow,to_std=to_std,to_file=to_file,to_514=to_514)})"
        if( not isinstance(caller, str) ):          raise ValueError(f"{temp_str_prepend}param [caller] expected to be type STR but is type {type(caller).__name__.upper()}{temp_str_debug}")
        if( not isinstance(logid, int) ):           raise ValueError(f"{temp_str_prepend}param [logid] expected to be type INT but is type {type(logid).__name__.upper()}{temp_str_debug}")
        if( not isinstance(serial, int) ):          raise ValueError(f"{temp_str_prepend}param [serial] expected to be type INT but is type {type(serial).__name__.upper()}{temp_str_debug}")
        if( not isinstance(level, int) ):           raise ValueError(f"{temp_str_prepend}param [level] expected to be type INT but is type {type(level).__name__.upper()}{temp_str_debug}")
        if( not isinstance(status, str) ):          raise ValueError(f"{temp_str_prepend}param [status] expected to be type STR but is type {type(status).__name__.upper()}{temp_str_debug}")
        if( not isinstance(texttolog, str) ):       raise ValueError(f"{temp_str_prepend}param [texttolog] expected to be type STR but is type {type(texttolog).__name__.upper()}{temp_str_debug}")
        if( not isinstance(nonewlines, bool) ):     raise ValueError(f"{temp_str_prepend}param [nonewlines] expected to be type BOOL but is type {type(nonewlines).__name__.upper()}{temp_str_debug}")
        if( not isinstance(timenow, str) ):         raise ValueError(f"{temp_str_prepend}param [timenow] expected to be type STR but is type {type(timenow).__name__.upper()}{temp_str_debug}")
        if( not isinstance(to_std, bool) ):         raise ValueError(f"{temp_str_prepend}param [to_std] expected to be type BOOL but is type {type(to_std).__name__.upper()}{temp_str_debug}")
        if( not isinstance(to_file, bool) ):        raise ValueError(f"{temp_str_prepend}param [to_file] expected to be type BOOL but is type {type(to_file).__name__.upper()}{temp_str_debug}")
        if( not isinstance(to_514, bool) ):         raise ValueError(f"{temp_str_prepend}param [to_514] expected to be type BOOL but is type {type(to_514).__name__.upper()}{temp_str_debug}")
        #special situations
        if(to_file==True and self.logfile==None):
            #raise exception but catch immediately and let exception_handle() do it's job
            try:                    raise ValueError(f"{temp_str_prepend}parameter [to_file=True] but logfile not opened; specify log file path and call logfile_open() before using [to_file=True]{temp_str_debug}")
            except Exception as e:  backend.exception_handle(self,"logging.log()",e)
    def checkparam_logrunning(self,caller,status,texttolog,logid,level):
        """
        brief internal function check parameters on function call
        param [**] self-describing
        returns [] None
        """
        temp_str_prepend=f"extendlog: logging.logrunning(): "
        temp_str_debug=f" (for debugging: function called with parameters: logrunning({backend.reconstr_func_param(caller=caller,status=status,texttolog=texttolog,logid=logid,level=level)})"
        if( not isinstance(caller, str) ):          raise ValueError(f"{temp_str_prepend}param [caller] expected to be type STR but is type {type(caller).__name__.upper()}{temp_str_debug}")
        if( not isinstance(status, str) ):          raise ValueError(f"{temp_str_prepend}param [status] expected to be type STR but is type {type(status).__name__.upper()}{temp_str_debug}")
        if( not isinstance(texttolog, str) ):       raise ValueError(f"{temp_str_prepend}param [texttolog] expected to be type STR but is type {type(texttolog).__name__.upper()}{temp_str_debug}")
        if( not isinstance(logid, int) ):           raise ValueError(f"{temp_str_prepend}param [logid] expected to be type INT but is type {type(logid).__name__.upper()}{temp_str_debug}")
        if( not isinstance(level, int) ):           raise ValueError(f"{temp_str_prepend}param [level] expected to be type INT but is type {type(level).__name__.upper()}{temp_str_debug}")
    def checkparam_logrunningnow(self,entries,queue_reset,combine,status_prefix,nonewlines,to_std,to_file,to_514):
        """
        brief internal function check parameters on function call
        param [**] self-describing
        returns [] None
        """
        temp_str_prepend=f"extendlog: logging.logrunning_now(): "
        temp_str_debug=f" (for debugging: function called with parameters: logrunning_now({backend.reconstr_func_param(entries=entries,queue_reset=queue_reset,combine=combine,status_prefix=status_prefix,nonewlines=nonewlines,to_std=to_std,to_file=to_file,to_514=to_514)})"
        if( not isinstance(entries, int) ):         raise ValueError(f"{temp_str_prepend}param [entries] expected to be type INT but is type {type(entries).__name__.upper()}{temp_str_debug}")
        if( not isinstance(queue_reset, bool) ):    raise ValueError(f"{temp_str_prepend}param [queue_reset] expected to be type BOOL but is type {type(queue_reset).__name__.upper()}{temp_str_debug}")
        if( not isinstance(combine, bool) ):        raise ValueError(f"{temp_str_prepend}param [combine] expected to be type BOOL but is type {type(combine).__name__.upper()}{temp_str_debug}")
        if( not isinstance(status_prefix, str) ):   raise ValueError(f"{temp_str_prepend}param [status_prefix] expected to be type STR but is type {type(status_prefix).__name__.upper()}{temp_str_debug}")
        if( not isinstance(nonewlines, bool) ):     raise ValueError(f"{temp_str_prepend}param [nonewlines] expected to be type BOOL but is type {type(nonewlines).__name__.upper()}{temp_str_debug}")
        if( not isinstance(to_std, bool) ):         raise ValueError(f"{temp_str_prepend}param [to_std] expected to be type BOOL but is type {type(to_std).__name__.upper()}{temp_str_debug}")
        if( not isinstance(to_file, bool) ):        raise ValueError(f"{temp_str_prepend}param [to_file] expected to be type BOOL but is type {type(to_file).__name__.upper()}{temp_str_debug}")
        if( not isinstance(to_514, bool) ):         raise ValueError(f"{temp_str_prepend}param [to_514] expected to be type BOOL but is type {type(to_514).__name__.upper()}{temp_str_debug}")
    def ensure_maxvars_log(caller,status,level,logid,serial):
        """
        brief internal function check parameters on function call
        param [**] self-describing
        returns [] None
        """
        caller=caller[0:36]
        status=status[0:18]
        level=min(level,9)
        logid=min(logid,999_999_999)
        serial=min(serial,999_999_999)
        return( caller,status,level,logid,serial )
    def reconstr_func_param(**kwargs):
        """
        brief internal function to return the set of parameters provided
        param [**] self-describing
        returns [str_out] STR
        """
        return str(kwargs)
    def logid_in_queue(self,logid,buf_to_search):
        """
        brief internal function that tests for specific element already in runninglog_buf
        param [self] OBJ
        param [logid] INT the logid to search for
        param [buf_to_search] COLLECTIONS.DEQUE() the buffer to search in
        returns [] BOOL
        """
        for i in range( len(buf_to_search) ):
            if( buf_to_search[i].logid==logid ): return True
        return False
    def remove_dupli(self,combine,entries,buf_orig_len):
        """
        brief internal function that returns a cleaned-up version of runninglog_buf
        param [self] OBJ
        param [combine] BOOL
        param [entries] INT max. no. of entries
        param [buf_orig_len] INT the original buffer length, to compensate for new entries during runtime
        returns [runninglog_buf_mod] OBJ the cleaned-up version
        returns [runninglog_buf_to_remove] OBJ the cleaned-up version including duplicates
        """
        #prepare
        buf_mod=collections.deque()
        buf_to_remove=collections.deque()
        #do
        if(combine):
            for i in range( min(buf_orig_len,entries) ):
                if( not backend.logid_in_queue(self,self.runninglog_buf[i].logid,buf_mod) ):
                    buf_mod.append( self.runninglog_buf[i] )
                    buf_to_remove.append( self.runninglog_buf[i] )
                else:
                    buf_to_remove.append( self.runninglog_buf[i] )
        else: buf_mod=self.runninglog_buf; buf_to_remove=self.runninglog_buf;
        return( buf_mod,buf_to_remove )
    def pop_entries(self,buf_to_remove,queue_reset,buf_orig_len):
        """
        brief internal function that removes the logged elements from runninglog_buf
        param [self] OBJ
        param [buf_to_remove] OBJ the entries to remove
        param [queue_reset] BOOL
        param [buf_orig_len] INT the original buffer length, to compensate for new entries during runtime
        returns [] None
        """
        if(not queue_reset):
            for i in range(buf_to_remove):  self.runninglog_buf.popleft()
        elif(queue_reset):
            for i in range(buf_orig_len):   self.runninglog_buf.popleft()
    def get_dupli_per_id(self,queue_in):
        """
        brief internal function that returns a list of duplicates found in [queue_in]
        param [self] OBJ
        param [queue_in] OBJ
        returns [dupli_buf] LIST of TEMPLATES.DUPLI_BUF -type objects, one entry for each logid if duplicate was found
        """
        queue_mod=copy.deepcopy(queue_in)
        dupli_buf=[]
        while( len(queue_mod)>0 ):
            entry=queue_mod[0] #index 0 is base
            entry2_num=-1
            index_to_remove=[]
            for entry2 in queue_mod: #for every entry
                entry2_num+=1
                if( entry2_num!=0 ): #do not touch base
                    if( entry.logid==entry2.logid ):
                        index_to_remove.append(entry2_num) #mark index for removal
            #inform of duplicate
            if( len(index_to_remove)>0 ): dupli_buf.append( templates.dupli_buf(entry.logid,len(index_to_remove)) )
            #remove marked indexes
            index_modifier=0
            for index_to_remove_curr in index_to_remove:
                del(queue_mod[index_to_remove_curr+index_modifier]); index_modifier-=1
            #remove self
            del(queue_mod[0])
        return dupli_buf
    def queue_join_mind_exit(self,queue_obj):
        """
        brief internal function for queue.Queue.join() but mind exitCalled
        param [self] OBJ
        param [queue_obj] OBJ the queue.Queue -object in question
        returns [] None
        """
        while( not queue_obj.empty() ):
            if(self.exitCalled): break #break from while loop
            time.sleep(self.thread_default_sleep_time)
        return
        
#templates
class templates:
    """
    brief provides objects for internal use
    """
    class runninglog:
        def __init__(self,timenow,caller,status,texttolog,logid,level):
            """
            brief provides a template for an entry in the running log
            param [timenow] INT timenow of the logged event, in format of datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
            param [caller] STR caller
            param [status] STR status
            param [texttolog] STR texttolog
            param [logid] INT logid
            returns [] None
            """
            self.timenow =              timenow
            self.caller =               caller
            self.status =               status
            self.texttolog =            texttolog
            self.logid =                logid
            self.level =                level
    class dupli_buf:
        def __init__(self,logid=None,num_dupli=None):
            """
            brief provides a template for the list of duplicates
            param [logid] INT
            param [num_dupli] INT
            returns [] None
            """
            self.logid =                -1 if logid is None else logid
            self.num_dupli =            0 if num_dupli is None else num_dupli
            
#threading
class threading:
    """
    brief provides threading objects and functions
    """
    def write_logfile_thread(self):
        """
        brief thread that writes to logfile
        returns [] None
        """
        try:
            backend.debug_handle(self,"logging.write_logfile_thread() was called and will start while-loop now...")
            while( not self.exitCalled ) or ( self.exitCalled and self.exitWait and self.queue_logfile.qsize()>0 ):
                linesum = ""
                linecount = 0
                for i in range(self.queue_logfile.qsize()):
                    try:
                        linesum+=self.queue_logfile.get_nowait()
                        linecount+=1
                    except queue.Empty: pass #ignore
                    except:
                        try:    self.queue_logfile.task_done()
                        except: pass
                #if everything alright
                if( self.logfile!=None ) and (linesum):
                    self.logfile.write(linesum) #write to logfile
                    self.logfile.flush() #make sure logfile is written to
                    for i in range(linecount): self.queue_logfile.task_done() #remove entries from queue_logfile
                elif( self.logfile==None ): pass
                else:                       raise RuntimeError(f"global var [self.logfile] and local var [linesum] have unexpected value or combination of values: (in order) '{self.logfile!r}', '{linesum!r}'")
                time.sleep(self.thread_default_sleep_time)
            #finally, shut down:
            backend.debug_handle(self,"logging.write_logfile_thread(): while-loop exited and will begin shutdown of thread now...")
            backend.shutdown_writeLogfileThread(self,is_exc=False)
            backend.debug_handle(self,"logging.write_logfile_thread(): shutdown of thread initiated and should have finished, function finished")
        except Exception as e:
            backend.exception_handle(self,"logging.write_logfile_thread()",e,f"shutting down tasks now...",to_std=True)
            backend.shutdown_writeLogfileThread(self,is_exc=True)
    def write_stdout_thread(self):
        """
        brief thread that writes to stdout
        returns [] None
        """
        try:
            backend.debug_handle(self,"logging.write_stdout_thread() was called and will start while-loop now...")
            while (not self.exitCalled) or (self.exitCalled and self.exitWait and self.queue_stdout.qsize()>0):
                linesum = ""
                linecount = 0
                for i in range(self.queue_stdout.qsize()):
                    try:
                        linesum = linesum+self.queue_stdout.get_nowait()+"\r\n"
                        linecount += 1
                    except queue.Empty: pass #ignore
                    except:
                        try:    self.queue_stdout.task_done()
                        except: pass
                try:
                    #if everything alright
                    if linesum:
                        if(linesum.endswith("\r\n")): linesum=linesum[:-2]
                        for i in range(linecount): self.queue_stdout.task_done()
                except Exception as e:
                    backend.exception_handle(self,"logging.write_stdout_thread()",e,f"shutting down tasks now...",to_std=True)
                    backend.shutdown_writeStdoutThread(self,is_exc=True)
                time.sleep(self.thread_default_sleep_time)
            #finally, shut down:
            backend.debug_handle(self,"logging.write_stdout_thread(): while-loop exited and will begin shutdown of thread now...")
            backend.shutdown_writeStdoutThread(self,is_exc=False)
            backend.debug_handle(self,"logging.write_stdout_thread(): shutdown of thread initiated and should have finished, function finished")
        except Exception as e:
            backend.exception_handle(self,"logging.write_stdout_thread()",e,f"shutting down tasks now...",to_std=True)
            backend.shutdown_writeStdoutThread(self,is_exc=True)
