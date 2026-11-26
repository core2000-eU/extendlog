# extendlog

*extendlog*, a Python module providing customized, high-level logging functions.  

Provides capable, customizable logging features. Easy-to-use, modern, fast. IT JUST WORKS.  
And best of all: results are constant. Logfiles look uniform.  
**You can depend on it.**  

[Supporters](#now-for-the-boring-part) and contributors are welcome any day of the week :)  

> [!NOTE]
> This project is in use by **MPSS - Multi-platform shared storage**, a brand-new way to combine, share and access storage over LAN and WAN. Run servers, workstations and clients, multiple OSs and huge numbers of devices simultaneously.  
[Take a look here if that sounds interesting! \[core2000.com\]](https://core2000.com/software/mpss/)  

## Fast track
Install with `pip install extendlog`; import into your project with `import extendlog`; and refer to the example file [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) on GitHub.  

## Basics
**Compatibility**  in short: any platform on Python 3+.  
Confirmed working: Win10, Win11, RHEL/Rocky Linux 10.x with Python 3.14.2.

**Status:** *public beta*.  
The current functions are tested on compatible platforms. There's some features missing here and there (see below) and I'd be glad for feedback.  
In short, I'm waiting on community response before the release of a final version - but rest assured that current releases are tested extensively.

**Built** on W11 25H2 with python 3.15.0, pip 26.3, build 1.5.0, twine 7.0.0. Standard settings.  

## Installation

  | Type | Details |
  |------|---------|
  | **venv** highly recommended. Please adapt the commands below to your needs. |
  | **Auto install**<br>(preferred, easiest) | run `pip install extendlog`, it will download and install from pypi.org |
  | **Manual install from source** | 1. Download the entire source from GitHub<br>2. unpack from ZIP<br>3. run e.g `python -m pip install "/path/to/folder/extendlog/" --no-cache-dir` |

## Documentation

### Basic usage  
Import with `import extendlog`.  
Initialize a new instance with e.g. `logging = extendlog.logging("logfile_1.log")`, where `logging` is now your instance.  
You must now call `logging.logfile_open()` to open the logfile for r/w access.  
Now you can call all user-facing functions e.g. `logging.log(*)`, `logging.logrunning(*)`, ... .  

### User-facing functions, exception handling, examples:  
because everything is so neatly documented in our example file, please refer to it at [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) on GitHub.  

> [!IMPORTANT]
> Please keep the [quirks, features, todo](#quirks-features-todo) section in mind below  

> [!IMPORTANT]
> Please, account for this library's special [Exception handling (see below)](#exception-handling)

### Quirks, features, ToDo
**Quirks and features**:  
- each log entry in the stdout and logfile outputs feature the same exact structure and order, the same number of characters (except for the logged text of course, which is the very last object in any log entry), and the same encoding (UTF-8). This means that stdout/logfiles are machine-readable and you can trust that in future versions, the format of outputs will stay the same.
- your instance of extendlog MUST be shutdown (by calling the exit() function on your instance)  or background threads will continue to run.
- once exit() is called on your instance, you must throw it away. It's non-reusable.


**ToDo**:  
- [Issue #1:](https://github.com/core2000-eU/extendlog/issues/1) Logging to syslog server needs implementation. ( the "to_514" parameters in log() )  
  Timeframe: Q2/2027. For now, stdout and logfile are the only options.
- [Issue #2:](https://github.com/core2000-eU/extendlog/issues/2) Implement instance-wide settings for [to_file], [to_stdout], [to_514].  
  Timeframe: Q2/2027. For now, you have to set these options on each call to log() and logrunning_now().  

### Source file structure (for contributors and developers):  
```
    <root>
        /samples                      -> sample files
        /src                          -> source code: main folder
            /P                        -> source code: python
                /extendlog            -> 
                    /__init__.py      -> main source code file; front-end (user-facing) functions
                    /backend.py       -> backend functions
        LICENSE                       -> LICENSE
        README.md                     -> README
        setup.py                      -> pip installer setup file
```

### 5.8 Source code structure (for contributors and developers):  
`/src/P/extendlog/__init__.py` is the main entry file which contains front-end (user-facing) functions and structures.  
The universal main entry point is the `__init(*)__` function of class `logging` in this source code file.  
This is a result from the user importing the library `import extendlog` and initializing a new instance e.g. `logging = extendlog.logging(*)`.  

On this instance, the user then calls the relevant functions e.g. `logging.logfile_open()`, `logging.log(*)`.  

`/src/P/extendlog/__init__.py` imports the `backend.py` source code file which contains classes for backend stuff, exception handling, templates and threading.

SELF KEYWORD

When the user calls `extendlog.logging()`, `__init(*)__` generates the required instance variables such as `self.queue_logfile`, `self.logfile`, `self.exitCalled`, ... and is now the owner of the `self` keyword.  
Between source files, to every function in question, the `self` keyword is simply parsed as an argument.  
E.g. when a function from `__init__.py` calls function `queue_join_mind_exit(*)` from a function in `backend.py` -> class `backend`, it passes the `self` keyword as first argument:  
```
backend.backend.queue_join_mind_exit(self,*)
```

THREADING  

The library was designed thread-safe for the front end, so the backend must also use threads:  
Every type of output - stdout, logfile - has it's own background thread which collects the entries from these buffer vars:
```
queue_logfile     type: queue.Queue()     -> queue for logfile entries
queue_stdout      type: queue.Queue()     -> queue for stdout entries
```
The threads are started on initialization of an instance of the library and run until the user exits the instance.

DEBUGGING

Debugging messages are visible only in stdout, so run from terminal.  
Set `debug=True` when initializing a new instance to enable debugging messages:  
```
logging = extendlog.logging("my_log_file.txt", debug=True)
```

## 6. Official Sources

  | Site | URL |
  |------|---------|
  | **GitHub** | [github.com/core2000-eU/extendlog](https://github.com/core2000-eU/extendlog) |
  | **pypi.org** | [pypi.org/project/extendlog](https://pypi.org/project/extendlog) |
  | core2000.com (Website/info only, no release) | [core2000.com/software](https://core2000.com/software/) |

## Now for the boring part
**This library is created and maintained free of cost by a real human being /bla /bla /bla ...** You know the deal by now.  
But seriously, monetary support a serious subject and without some income, I cannot continue to publish and maintain.  

Not that anyone needs my gibberish anyways, but if you find it helpful, **please consider the below. Thanks :)**  
--> [**buymeacoffee.com/core2000**](https://buymeacoffee.com/core2000)

## About
Created on 10.2026 and happily maintained since by **core2000** and it's owner, Benjamin Winter.  
For more details, you can pay us a visit over on [**core2000.com**](https://core2000.com/).
