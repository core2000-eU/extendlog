#Copyright (c) 2026 Benjamin Winter
#This file is part of extendlog which is released under the MIT License.
#See file LICENSE or go to https://github.com/core2000-eU/extendlog for full license details.

#DESCRIPTION
#extendlog, a Python module providing customized, high-level logging functions.

import                          setuptools
from pathlib import             Path

parent_dir = Path(__file__).parent
long_description = (parent_dir / "README.md").read_text(encoding="utf-8")

setuptools.setup (
    name =                              "extendlog", 
    version =                           "0.0.1",
    author =                            "Benjamin Winter",
    license=                            "MIT",
    description =                       "extendlog, a Python module providing customized, high-level logging functions.",
    long_description =                  long_description,
    long_description_content_type =     "text/markdown",
    keywords =                          ["python", "logging", "log"],
    classifiers =                       [
                                            "Development Status :: 4 - Beta",
                                            "Programming Language :: Python :: 3",
                                            "Operating System :: OS Independent"
                                        ],
    packages =                          setuptools.find_namespace_packages(where="src/P"),
    package_dir =                       {"": "src/P"},
    install_requires =                  [],
    package_data =                      {},
)
