#Copyright (c) 2026 Benjamin Winter
#This file is part of extendlog which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/extendlog for full license details.

#DESCRIPTION
#extendlog, a Python module providing customized, high-level logging functions.

#imports
from . import                       backend
import                              collections
import                              datetime
import                              queue
import                              threading
import                              random
import                              pathlib

#global vars
exceptions = backend.exceptions #make it available to end user

#main code
class logging:
    """
    brief main class that provides functions for logging
    """
    def __init__(self, logfilepath=None,runtime_exc_max=None,runtime_exc_raise=None,debug=None):
        """
        brief initialize a new instance
        param [logfilepath] STR full path to logfile; IF empty, subsequent log() calls MUST be made with parameter [to_file]=False
        param [runtime_exc_raise] BOOL if True:raise Exceptions on user-facing functions; False:do not raise Exceptions and only store them in a buffer; default:False
        param [runtime_exc_max] INT only applicable when [runtime_exc_raise]=True: max. no. of silent exceptions, that may occur at runtime, before an exception is raised; default:0
        param [debug] BOOL True:enable debugging, False:disable debugging; default:False
        returns [] None
        """
        self.logfilepath = "" if logfilepath is None else logfilepath
        self.logfile = None
        self.runninglog_buf = collections.deque()
        self.exitCalled = False
        self.exitWait = False
        self.queue_logfile = queue.Queue()
        self.queue_stdout = queue.Queue()
        self.thread_default_sleep_time = 1/64
        self.runtime_exc_max = 0 if runtime_exc_max is None else runtime_exc_max
        self.runtime_exc_buffer = []
        self.runtime_exc_bufferAsStr = []
        self.runtime_exc_raise = False if runtime_exc_raise is None else runtime_exc_raise
        self.debug = False if debug is None else debug
        #prepare
        self.logfilepath = pathlib.Path(self.logfilepath).resolve()
        #start threads
        self.thread_write_logfile = (threading.Thread(name = "write_logfile_thread", target=backend.threading.write_logfile_thread, args=(self,))); self.thread_write_logfile.start()
        self.thread_write_stdout = (threading.Thread(name = "write_stdout_thread", target=backend.threading.write_stdout_thread, args=(self,))); self.thread_write_stdout.start()
    def log(self, caller="", status="", texttolog="", logid=0, serial=0, level=6, nonewlines=True, timenow=None, to_std=True, to_file=True, to_514=False):
        """
        brief append a log entry to stdout or file
        param [caller] STR (max. 36 chars) that specifies the caller (any format you like, e.g. "201.10" or "myprog.myfunction.mysubfunction")
        param [status] STR (max. 18 chars) any status you like, e.g. INFO, WARNING, EXCEPTION, ...
        param [texttolog] STR that specifies the text to log
        param [logid] INT (max. 999_999_999) optional logid of the event; e.g. use the same logid for the same exact occurences of an event; default:0
        param [serial] INT (max. 999_999_999) optional serial number of this specific log entry; max:999_999_999, default:randomly-generated if not provided
        param [level] INT (max. 9) optional loglevel as known from many linux-based systems, e.g.4; recommended:0-7, max:9, default:4
        param [nonewlines] BOOL optional if True, both \r \n will be removed from texttolog; default:True
        param [timenow] STR optional if given, you can overwrite the timestamp used in output; default:None(auto-generated)
        param [to_std] BOOL optional if True, will log to stdout (terminal); default:True
        param [to_file] BOOL optional if True, will log to logfile; default:True
        param [to_514] BOOL optional if True, will log to syslog server (often at port 514); default:False; NO FUNCTION AT THIS TIME because syslogging is not implemented yet
        returns [] None
        """
        try:
            #prepare
            timenow =   ( datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f") ) if timenow is None else timenow
            if(serial<=0): serial=random.randrange(999999999)
            #checks
            backend.backend.checkparam_log(self,caller,logid,serial,level,status,texttolog,nonewlines,timenow,to_std,to_file,to_514)
            #compensate for malicious strings
            caller,status,level,logid,serial=backend.backend.ensure_maxvars_log( caller,status,level,logid,serial )
            texttolog = texttolog.encode(encoding='utf-8',errors='replace').decode(encoding='utf-8',errors='replace')
            if(nonewlines): texttolog = texttolog.replace('\r', '').replace('\n', '')
            #make texttolog_mod
            texttolog_mod = ""
            texttolog_mod_nonl = ""
            texttolog_mod += timenow                                                                                #"2000-01-01_08-00-00.012345"
            for rangecount in range(26+1-len(timenow)): texttolog_mod += " "                                        #"2000-01-01_08-00-00.012345 "
            texttolog_mod += (caller)                                                                               #"2000-01-01_08-00-00.012345 201.10"
            for rangecount in range(36+1-len(caller)): texttolog_mod += " "                                         #"2000-01-01_08-00-00.012345 201.10                               "
            texttolog_mod += str(logid)                                                                             #"2000-01-01_08-00-00.012345 201.10                               123456789"
            for rangecount in range(9+1-len(str(logid))): texttolog_mod += " "                                      #"2000-01-01_08-00-00.012345 201.10                               123456789 "
            texttolog_mod += str(serial)                                                                            #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321"
            for rangecount in range(9+1-len(str(serial))): texttolog_mod += " "                                     #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321 "
            texttolog_mod += str(level)                                                                             #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321 4"
            for rangecount in range(1+1-len(str(level))): texttolog_mod += " "                                      #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321 4 "
            texttolog_mod += (status.upper())                                                                       #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321 4 SUCCESS"
            for rangecount in range(18+1-len(status)): texttolog_mod += " "                                         #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321 4 SUCCESS      "
            texttolog_mod += (texttolog); texttolog_mod_nonl = texttolog_mod; texttolog_mod += ("\n")               #"2000-01-01_08-00-00.012345 201.10                               123456789 987654321 4 SUCCESS      test-string"
            #stdout
            self.queue_stdout.put(texttolog_mod_nonl)
            #file
            self.queue_logfile.put(texttolog_mod)
            #syslog
            #NOT IMPLEMENTED YET
        except Exception as e: backend.backend.exception_handle(self,"logging.log()",e)
    def logrunning(self, caller, status, texttolog, logid=0, level=4):
        """
        brief add an entry to the running log
        param [caller] STR (max. 36 chars) that specifies the caller in any format you like, e.g. "my_func" or "201.10"
        param [status] STR (max. 18 chars) any status you like, e.g. INFO, WARNING, EXCEPTION, ...
        param [texttolog] STR that specifies the text to log
        param [logid] INT (max. 999_999_999) optional logid of the event; e.g. use the same logid for the same occurence of an event
        param [level] INT (max. 9) optional loglevel as known from many linux-based systems, e.g.4; recommended:0-7, max:9, default:4
        returns [] None
        """
        try:
            #checks
            backend.backend.checkparam_logrunning(self,caller,status,texttolog,logid,level)
            #prepare
            timenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
            #compensate for malicious string
            caller = caller[0:36]
            status = status[0:18]
            logid=min(logid,999_999_999)
            level=min(level,9)
            #do
            self.runninglog_buf.append( backend.templates.runninglog(timenow,caller,status,texttolog,logid,level) )
        except Exception as e: backend.backend.exception_handle(self,"logging.logrunning()",e)
    def logrunning_now(self, entries=999, queue_reset=True, combine=False, status_prefix="", nonewlines=True, to_std=True, to_file=True, to_514=False):
        """
        brief output all entries stored in runninglog
        param [entries] INT that specifies the max. number of entries to log, default:999
        param [queue_reset] BOOL if True, resets queue after this call, e.g. if more than 999 entries are in queue, they will also be removed without being logged; default:True
        param [combine] BOOL if True, duplicates using same logid are logged only once; default:False
        param [status_prefix] STR prefix before status, e.g."STAT_", default:""
        param [nonewlines] BOOL optional if True, both \r \n will be removed from texttolog; default:True
        param [to_std] BOOL optional if True, will log to stdout (terminal); default:True
        param [to_file] BOOL optional if True, will log to logfile; default:True
        param [to_514] BOOL optional if True, will log to syslog server (often at port 514); default:False; NO FUNCTION AT THIS TIME because syslogging is not implemented yet
        returns [] None
        """
        try:
            #checks
            backend.backend.checkparam_logrunningnow(self,entries,queue_reset,combine,status_prefix,nonewlines,to_std,to_file,to_514)
            #prepare & get
            buf_orig_len=len(self.runninglog_buf)
            buf_mod,buf_to_remove=backend.backend.remove_dupli(self,combine,entries,buf_orig_len)
            #log
            for i in range( len(buf_mod) ): self.log( (buf_mod[i].caller),(status_prefix+buf_mod[i].status),(buf_mod[i].texttolog),logid=(buf_mod[i].logid),level=(buf_mod[i].level),nonewlines=nonewlines,timenow=(buf_mod[i].timenow),to_std=to_std,to_file=to_file,to_514=to_514 )
            #inform of duplicates
            buf_dupli=backend.backend.get_dupli_per_id(self,buf_to_remove)
            if( combine) and ( len(buf_dupli)>0 ):
                for dupli in buf_dupli:                         self.log("extendlog", "INFO", f"running log: above entry with logid [{dupli.logid}] had [{dupli.num_dupli}] duplicates using the same logid, omitted from output",nonewlines=False,to_std=to_std,to_file=to_file,to_514=to_514)
            if( buf_orig_len>entries and not queue_reset ):     self.log("extendlog", "INFO", f"running log: max. entries reached, [{buf_orig_len-entries}] stay in queue",nonewlines=False,to_std=to_std,to_file=to_file,to_514=to_514)
            elif( buf_orig_len>entries ):                       self.log("extendlog", "INFO", f"running log: max. entries reached, [{buf_orig_len-entries}] removed from queue",nonewlines=False,to_std=to_std,to_file=to_file,to_514=to_514)
            #reset
            backend.backend.pop_entries(self,buf_to_remove,queue_reset,buf_orig_len)
        except Exception as e: backend.backend.exception_handle(self,"logging.logrunning_now()",e)
    def logfile_open(self):
        """
        brief open a logfile, and keep it opened until logfile_close() is called;
        returns [] None
        """
        try:
            if(self.logfilepath == None): raise Exception (f"extendlog: logging.logfile_open(): parameter [logfilepath] is None OR empty. use parameter [logfilepath] first when initializing an instanze of class logging()")
            backend.backend.debug_handle(self,"logging.logfile_open() called and will attempt to open logfile now and store reference to object...")
            self.logfile = open(self.logfilepath, mode="a", encoding="utf-8")
            backend.backend.debug_handle(self,"logging.logfile_open(): logfile opened and reference stored, function finished")
        except Exception as e: backend.backend.exception_handle(self,"logging.logfile_open()",e,to_std=True)
    def logfile_rotate(self, logfilepath="", loginfo=True):
        """
        brief close the existing logfile and open a new logfile; safe to call even if elements are in queue
        param [logfilepath] STR full path to new logfile
        param [loginfo] BOOL if True, log an info that logfile was rotated; default:True
        returns [] None
        """
        try:
            #check
            if(self.logfilepath == None): raise Exception (f"extendlog: logging.logfile_rotate(): parameter [logfilepath] is None OR empty")
            if(self.logfile == None): raise Exception (f"extendlog: logging.logfile_rotate(): can't rotate logfile because no logfile is currently opened")
            backend.backend.debug_handle(self,"logging.logfile_rotate() called and will attempt to resolve path to new logfile now ( pathlib.Path(logfilepath).resolve() )...")
            #calculate
            logfilepath =       pathlib.Path(logfilepath).resolve()
            backend.backend.debug_handle(self,"logging.logfile_rotate(): logfilepath resolve finished and will attempt to store reference to old logfile now...")
            logfile_old =       self.logfile
            logfilepath_old =   self.logfilepath
            backend.backend.debug_handle(self,"logging.logfile_rotate(): reference to old logfile stored, will attempt to log info now...")
            #log
            if(loginfo): self.log("extendlog", "INFO", f"logging.logfile_rotate() was called and logfile will be rotated from '{logfilepath_old}' to '{logfilepath}'",nonewlines=True,to_std=True,to_file=True,to_514=True)
            backend.backend.debug_handle(self,"logging.logfile_rotate(): info logged, will attempt to join logfile queue now to wait for existing buffer to log to old logfile ( backend.backend.queue_join_mind_exit() ) ...")
            if(loginfo): backend.backend.queue_join_mind_exit(self,self.queue_logfile)
            backend.backend.debug_handle(self,"logging.logfile_rotate(): join finished, will attempt to flush() old logfile now...")
            logfile_old.flush()
            backend.backend.debug_handle(self,"logging.logfile_rotate(): flush operation finished, will attempt to open new logfile now...")
            #do
            logfile_new = open(logfilepath, mode="a", encoding="utf-8")
            backend.backend.debug_handle(self,"logging.logfile_rotate(): new logfile opened, will attempt to store reference to new logfile now (exchange old<>new logfile references)...")
            self.logfile =      logfile_new
            self.logfilepath =  logfilepath
            backend.backend.debug_handle(self,"logging.logfile_rotate(): reference to new logfile stored, should be in use now, will attempt to close() old logfile now ( logfile_old.close() )...")
            logfile_old.close()
            backend.backend.debug_handle(self,"logging.logfile_rotate(): old logfile closed, will attempt to log info now...")
            #log
            if(loginfo): self.log("extendlog", "INFO", f"logging.logfile_rotate() was called and logfile was rotated from '{logfilepath_old}' to '{self.logfilepath}'",nonewlines=True,to_std=True,to_file=True,to_514=True)
            backend.backend.debug_handle(self,"logging.logfile_rotate(): info logged, function finished")
        except Exception as e: backend.backend.exception_handle(self,"logging.logfile_rotate()",e,to_std=True)
    def logfile_close(self, wait=True):
        """
        brief close a previously opned logfile
        param [wait] BOOL True:wait for all entries to be written; False:exit immediately; default:True
        returns [] None
        """
        try:
            backend.backend.debug_handle(self,"logging.logfile_close() called and will attempt to join logfile queue now to wait for existing buffer to log ( backend.backend.queue_join_mind_exit() ) ...")
            if(wait):   backend.backend.queue_join_mind_exit(self,self.queue_logfile)
            backend.backend.debug_handle(self,"logging.logfile_close(): join finished, will attempt to close() logfile now ( self.logfile.close() )...")
            try:
                self.logfile.close()
                backend.backend.debug_handle(self,"logging.logfile_close(): logfile closed, will attempt to set [self.logfile=None] now...")
            except:     pass;
            self.logfile = None
            backend.backend.debug_handle(self,"logging.logfile_close(): function finished")
        except Exception as e: backend.backend.exception_handle(self,"logging.logfile_close()",e,to_std=True)
    def exit(self, wait=True):
        """
        brief exit this library and from all created threads
        param [wait] BOOL True:wait for all entries to be written; False:exit immediately; default:True
        returns [] None
        """
        try:
            backend.backend.debug_handle(self,"logging.exit() called and will attempt to close logfile now ( self.logfile_close() )...")
            #close logfile
            self.logfile_close(wait=wait)
            backend.backend.debug_handle(self,"logging.exit(): logfile closed and will attempt to set vars [self.exitWait] and [self.exitCalled] now...")
            #notify everyone of exit
            self.exitWait = wait
            self.exitCalled = True
            #wait for threads
            if wait:
                backend.backend.debug_handle(self,"logging.exit(): vars set and will attempt to wait for thread [self.thread_write_logfile] now...")
                try: self.thread_write_logfile.join()
                except: pass
                backend.backend.debug_handle(self,"logging.exit(): wait for thread finished and will attempt to wait for thread [self.thread_write_stdout] now...")
                try: self.thread_write_stdout.join()
                except: pass
                backend.backend.debug_handle(self,"logging.exit(): wait for threads finished, function finished")
            else:
                backend.backend.debug_handle(self,"logging.exit(): vars set, function finished")
        except Exception as e: backend.backend.exception_handle(self,"logging.exit()",e,to_std=True)
