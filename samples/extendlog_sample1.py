#Copyright (c) 2026 Benjamin Winter
#This file is part of extendlog which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/extendlog for full license details.

#DESCRIPTION
#extendlog, a Python module providing customized, high-level logging functions.

#imports
import                              extendlog
import                              time

## 
## INITIALIZATION
##

#initialize a new instance while also providing a log file path:
logging = extendlog.logging("logfile_1.log")
#we need to make the library open the logfile in the background (for writing access) and keep it open until we exit
logging.logfile_open()



## 
## SIMPLE LOGGING
##



#first, let's use the most simple way to produce a log entry
#   'my_func_1'     -> the caller; name/identifier, can be any string you want; optional
#   'INFO'          -> the staus for the entry; can be any string you want; optional
#   'log test ...'  -> the text to log
logging.log(caller="my_func_1", status="INFO", texttolog=f"log test no. 1; path_to_logfile is {logging.logfilepath}")

#here is a list of all parameters the log() function accepts:
#   param [caller] STR (max. 36 chars) that specifies the caller (any format you like, e.g. "201.10" or "myprog.myfunction.mysubfunction")
#   param [status] STR (max. 18 chars) any status you like, e.g. INFO, WARNING, EXCEPTION, ...
#   param [texttolog] STR the text to log
#   param [logid] INT (max. 999_999_999) optional logid of the event; e.g. use the same logid for the same exact occurences of an event; default:0
#   param [serial] INT (max. 999_999_999) optional serial number of this specific log entry; max:999_999_999, default:randomly-generated if not provided
#   param [level] INT (max. 9) optional loglevel as known from many linux-based systems, e.g.4; recommended:0-7, max:9, default:4
#   param [nonewlines] BOOL optional if True, both \r \n will be removed from texttolog; default:True
#   param [to_std] BOOL optional if True, will log to stdout (terminal); default:True
#   param [to_file] BOOL optional if True, will log to logfile; default:True
#   param [to_514] BOOL optional if True, will log to syslog server (often at port 514); default:False; NO FUNCTION AT THIS TIME because syslogging is not yet implemented
logging.log(caller="my_func_2", status="INFO", texttolog="log test no. 2", logid=1234, serial=654321, level=6, nonewlines=True, to_std=True, to_file=True, to_514=False)

#see what happens when we log an invalid code point that is not compatible with UTF-8:
#-> does not raise an exception but replaces the code point with '?'
logging.log(caller="my_func_3", status="", texttolog="log test no. 3; invalid code point: \ud800")

#log separation chars
logging.log("", "", f"--------------------------------")

#info: calling log() blocks until all content written.



## 
## RUNNING LOG
##


#The runninglog feature is a highly capable feature, especially for time-senstitive and multi-thread applications.
#The runninglog lets you append entries to a buffer, but output them later (process/print/write to logfile later).
#Plus, it adds the benefit of being able to "cleanup" the output; e.g. if you've got the same entry 5 times, you can decide to print only one.
#calling logrunning() adds entries to the buffer. Non-blocking so you can call this from time-sensitive functions.
#calling logrunning_now() processes/outputs the entries stored in buffer; blocking; i.e. call this once every second from a background thread at runtime.

#appending entries to the buffer; notice 2 different values for [logid]:
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 5", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 6", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 7", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 8", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 9", logid=1237, level=2)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 10", logid=1237, level=2)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 11", logid=1237, level=2)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 12", logid=1237, level=2)

#logrunning() supports these parameters:
#   param [caller] STR (max. 36 chars) that specifies the caller in any format you like, e.g. "my_func" or "201.10"
#   param [status] STR (max. 18 chars) any status you like, e.g. INFO, WARNING, EXCEPTION, ...
#   param [texttolog] STR the text to log
#   param [logid] INT (max. 999_999_999) optional logid of the event; e.g. use the same logid for the same occurence of an event
#   param [level] INT (max. 9) optional loglevel as known from many linux-based systems, e.g.4; recommended:0-7, max:9, default:4

#Our entries are now stored in a buffer.

#calling logrunning_now() will cause them to be written/printed immediately
#Use the [combine] parameter to clean up the final output -> this will combine all entries using the same [logid] into one.

#logrunning_now() supports these parameters:
#   param [entries] INT that specifies the max. number of entries to log, default:999
#   param [queue_reset] BOOL if True, resets queue after this call, e.g. if more than 999 entries are in queue, they will also be removed without being logged; default:True
#   param [combine] BOOL if True, duplicates using same logid are logged only once; default:False
#   param [status_prefix] STR prefix before status, e.g."STAT_", default:""
#   param [nonewlines] BOOL optional if True, both \r \n will be removed from texttolog; default:True
#   param [to_std] BOOL optional if True, will log to stdout (terminal); default:True
#   param [to_file] BOOL optional if True, will log to logfile; default:True
#   param [to_514] BOOL optional if True, will log to syslog server (often at port 514); default:False; NO FUNCTION AT THIS TIME because syslogging is not implemented yet
logging.logrunning_now(combine=True)

#Because we set [combine]=True, the output will now contain two entries: one for logid=1236, and one for logid=1237.
#extendlog will use the first entry when combining multiple entries.

#log separation chars
logging.log("", "", f"--------------------------------")



## 
## ROTATING THE LOGFILE
## 



#This will close the existing logfile and open a new one. Safe to call even if elements are in queue.
#logfile_rotate() accepts these parameters:
#   param [logfilepath] STR full path to new logfile
#   param [loginfo] BOOL if True, log an info that logfile was rotated; default:True
logging.logfile_rotate("logfile_2.log")

#logfile_rotate() supports these parameters:
#   param [logfilepath] STR full path to new logfile
#   param [loginfo] BOOL if True, log an info that the logfile was rotated; default:True

#log separation chars
logging.log("", "", f"--------------------------------")



## 
## EXCEPTION HANDLING
## 



#extendlog uses a non-standard way to catch and handle exceptions.
#Because of this, it can be used in critical parts of your code - and in the default configuration, it's designed to AVOID RAISING EXCEPTIONS at all cost.

#When initializing a new instance of the library - calling the logging() function - these two parameters define exception behaviour:
#   param [runtime_exc_raise] BOOL if True: raise exceptions on user-facing functions; False: do not raise exceptions and store them in a buffer; default:False
#   param [runtime_exc_max] INT only applicable when [runtime_exc_raise]=True: max. no. of silent exceptions, that may occur at runtime, before an exception is raised; default:0

#Default behaviour - [runtime_exc_raise=False]:
#   None of the user-facing functions will raise exceptions.
#   But, exceptions are stored in a buffer.
#   To read the buffer, use the attributes [runtime_exc_buffer] and [runtime_exc_bufferAsStr] on your instance of the library:
#       runtime_exc_buffer[] stores one entry per original exception that occured, as an object
#       runtime_exc_bufferAsStr[] stores one entry per original exception that occured, as a STR
#Like so:
for exc in logging.runtime_exc_buffer:
    print(f"our instance of extendlog raised an exception:")
    print(exc)
    
#when using extendlog, you may check [runtime_exc_buffer] periodically, and handle exceptions accordingly - e.g. from a background thread.

#Custom behaviour - if you manually set [runtime_exc_raise=True]:
#   Like above, all exceptions are still stored in buffer.
#   But, any function you call now can raise exceptions.
#   The exception raised is not the original one - but of this type:
#       extendlog.exceptions.RuntimeExceptionsExceeded
#
#   For a good reason:
#   You can "delay" this behaviour and accept a certain number of runtime exceptions before extendlog raises one.
#   For this, use the [runtime_exc_max] attribute:
#       If you set it to int(10), there may be 10 silent exceptions.
#       Only when 11 exceptions have occured and you call any function, extendlog will raise an exception when a function is called
#       Default:0
#
#   The type of exception raised - extendlog.exceptions.RuntimeExceptionsExceeded - has these attributes:
#       runtime_exc_buffer[] stores one entry per original exception that occured, as an object
#       runtime_exc_bufferAsStr[] stores one entry per original exception that occured, as a STR
#
#   After that event, extendlog will shut down your instance, close all files and exit immediately.
#   At this point, you're not supposed to use the instance again; create a new one.
#   
#   That's why the example below is commented out - it would ruin our show :)

logging.runtime_exc_raise=True #enable raising of Exceptions;
logging.runtime_exc_max=0 #matches the default value
try:
    #uncomment next line to induce an exception
    #logging.log(1234)
    pass
except extendlog.exceptions.RuntimeExceptionsExceeded as e:
    print(e) #print the raised Exception, which is only a placeholder
    for exc in e.runtime_exc_buffer:
        print(f"our instance of extendlog raised an exception:")
        print(exc)



## 
## EXITING / SHUTTING DOWN
## 



#You MUST exit the library, or else extendlog's background thread will BLOCK indefinitely
#exit() supports these parameters:
#   param [wait] BOOL True:wait for all entries to be written; False:exit immediately; default:True
logging.exit(wait=True)
