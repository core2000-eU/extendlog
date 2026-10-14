# extendlog

*extendlog*, a Python module providing customized, high-level logging functions.  

Provides capable, customizable logging features. Easy-to-use, modern, fast. IT JUST WORKS.  
And best of all: results are constant. Logfiles look uniform.  
**You can depend on it.**  

> [!NOTE]
> This project is in use by **MPSS - Multi-platform shared storage**, a brand-new way to combine, share and access storage over LAN and WAN. Run servers, workstations and clients, multiple OSs and huge numbers of devices simultaneously.  
[Take a look here if that sounds interesting! \[core2000.com\]](https://core2000.com/software/mpss/)  

[Supporters](#now-for-the-boring-part) and contributors are welcome any day of the week :)

## Fast track
Install with `pip install extendlog`; import into your project with `import extendlog`; and refer to the [documentation](#documentation) section below to know your way around;  
and/or download, open and run example file [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) from GitHub.  

## Basics
**Compatibility**  in short: any platform on Python 3+.  
Here's a list of confirmed options:  

  | Name | Version | Description |
  |------|---------|-------------|
  | -- |
  | Windows 10 |      | ✅ should work   |
  | Windows 11 | 25H2 | ✅ confirmed working  |
  | RHEL/Rocky Linux  | 10        | ✅ confirmed working |
  | -- |
  | Python  | 3.14.2        | ✅ confirmed working |
  | Python  | 3.15.0        | ✅ confirmed working |

**Status:** *public beta*.  
The current functions are tested on compatible platforms. There's some features missing here and there (see below) and I'd be glad for feedback.  
In short, I'm waiting on community response before the release of a final version - but rest assured that current releases are tested extensively.

**Built** on W11 25H2 with python 3.14.2, pip 26.2.1, build 1.5.0, twine 7.0.0. Standard settings.

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
You must now call `logging.logfile_open()` to open the logfile for r/w access and keep it open until you exit the instance.  

After that, you can call all user-facing functions e.g. `logging.log(*)`, `logging.logrunning(*)`, ... .  

> [!IMPORTANT]
> Please keep the [quirks, features, todo](#quirks-features-todo) section in mind below  

> [!IMPORTANT]
> Please, account for this library's special [Exception handling (see below)](#exception-handling)  

> [!NOTE]
> For a guide and reference, you may download, open and run example file [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) from GitHub.  

### User-facing functions  
\>\>\> because everything is so neatly documented in our example file, please refer to it at [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) on GitHub.  
All user-facing functions are documented inside.  

### Exception handling
\>\>\> because everything is so neatly documented in our example file, please refer to it at [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) on GitHub.  
Exception handling is explicitely documented inside.  

### Examples  
> [!NOTE]
> For a vast collection of examples and further reference, open and run example file [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) from GitHub.

<br>

**Import; initialize instance of library; let extendlog open the logfile for r/w access**:  
```
import
import extendlog

#initialize a new instance while also providing a log file path:
logging = extendlog.logging("logfile_1.log")

#we need to make the library open the logfile in the background (for writing access) and keep it open until we exit
logging.logfile_open()
```

**simply log a single line to stdout and to file**:  
```
# ! you must import, initialize the library and call logfile_open() first !

#log
logging.log(caller="my_func_1", status="INFO", texttolog="log test no. 1")

#you can omit the parameter names when keeping their order:
logging.log("my_func_1", "INFO", "log test no. 1")

#using all parameters
logging.log(caller="my_func_2", status="INFO", texttolog="log test no. 2", logid=1234, serial=654321, level=6, nonewlines=True, to_std=True, to_file=True, to_514=False)
```

> [!NOTE]
> RUNNINGLOG
> The runninglog feature is a highly capable feature, especially for time-senstitive and multi-thread applications. It is described in detail in the example file [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) on GitHub.

**log entries to runninglog; process/output the runninglog afterwards**:  
```
# ! you must import, initialize the library and call logfile_open() first !

#log multiple entries using runninglog (non-blocking):
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 5", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 6", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 7", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="INFO", texttolog="logrunning no. 8", logid=1236, level=6)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 9", logid=1237, level=2)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 10", logid=1237, level=2)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 11", logid=1237, level=2)
logging.logrunning(caller="my_func_5", status="CRITICAL", texttolog="logrunning no. 12", logid=1237, level=2)

#process/output the entries stored in runninglog. It would make sense to call this from within a background thread (blocking):
logging.logrunning_now(combine=True)
```

**roting the logfile (can be done anytime, anywhere after logfile_open(\*) was called)**:  
```
logging.logfile_rotate("logfile_2.log")
```

> [!NOTE]
> EXCEPTION HANDLING
> Is described in detail in the example file [`/samples/extendlog_sample1.py`](https://github.com/core2000-eU/extendlog/blob/main/samples/extendlog_sample1.py) on GitHub.

**You must exit/shutdown every instance of extendlog like this**:  
```
logging.exit(wait=True)
```

### Quirks, features, ToDo
**Quirks and features**:  
- **This** library handles XML comments as "default" XML elements in *xml_struct*, meaning that all comments are also of type *templates.xml_struct.element(\*)*, but with their *is_comment* export set *TRUE*.  
- **CDATA** is not supported (future release).  
- **namespaces** are not supported (future release).
- **special characters** &, <, >, ", ':  
  - NOT ALLOWED in names (element names, attribute names).  
  - ALLOWED in values ESCAPED-ONLY (element values, attribute values):  
    - escape with:  
      - \& ... &amp  
      - \" ... &quot  
      - \' ... &quot  
      - \< ... &lt  
      - \> ... &gt  
    - the standard specifies that some special chars may be allowed even in values, **this will never be implemented**.  
    - on read() and write(), ALL [\"] are replaced with [\&quot].  
- **Mixed content** is not allowed and will probably never be implemented:  
  - not allowed:  
    \<a> CAT \<b>AND_MOUSE\</b> AND_DOG \</a>  
- **comment within XML element value** are not supported, and will probably never be implemented.  
- **old-school schema** mechanism not supported, only XSD.  
- **multi-line strings**:  
  - for function **read()**:  
    - **multi-line comments** are supported  
    - **multi-line element values** are supported but newline characters get discarded from output - you won't see them  
    - **multi-line attribute values** are supported  
    - **newline character** is '\\n' on output *xml_struct*  
  - for function **write()**:  
    - **newline character** is '\\n'  
    - **multi-line comments** are supported  
    - **multi-line element values** are supported but newline characters get discarded from output  
    - **multi-line attribute values** are supported  
- **nested comments** are not supported.  

**ToDo**:  
- [Issue #TODO:](https://github.com/core2000-eU/TODO) Logging to syslog server needs implementation. ( the "to_514" parameters in log() )  
  Timeframe: Q2/2027. For now, stdout and logfile are the only options.  

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
