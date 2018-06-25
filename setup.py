#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import os
import sys
import imp
import platform
from cx_Freeze import setup, Executable
from build_tool.path_repair_tool import repair_dependence


sys.path.append('fluorometer_analysis')


application_title = 'fluorometer_analysis'
exe_python_file = os.path.join('fluorometer_analysis',
                               'fluorometer_analysis.py')
version = '1.0'
icon = os.path.join('fluorometer_analysis', 'icon.ico')
description = 'fluorometer analysis'


PyQt5_path = imp.find_module('PyQt5')[1]


pltf = platform.system()
if pltf == 'Windows':
    platform_dependent_include_files = [
        os.path.join(PyQt5_path, 'libEGL.dll'),
    ]
    base = 'Win32GUI'
elif pltf == 'Linux':
    platform_dependent_include_files = []
    base = None
elif pltf == 'Darwin':
    platform_dependent_include_files = []
    base = None
else:
    platform_dependent_include_files = []
    base = None


include_files = [
    os.path.join('LICENSE'),
    os.path.join('fluorometer_analysis', 'icon'),
    os.path.join('fluorometer_analysis', 'wls_data_set.py'),
]
include_files.extend(platform_dependent_include_files)


includes = [
    'analyze_ratio',
    'format_analyzer_jws',
    'peak_calculatoin',
    'compiled_path',
    're',
    'sys',
    'os',
    'csv',
    'PyQt5',
]


excludes = []


packages = []


setup(
    name=application_title,
    version=version,
    description=description,
    options={
        'build_exe': {
            'includes': includes,
            'include_files': include_files,
            'excludes': excludes,
            'packages': packages,
            'include_msvcr': True,
        },
    },
    executables=[
        Executable(
            exe_python_file,
            base=base,
            compress=True,
            copyDependentFiles=True,
            appendScriptToExe=True,
            appendScriptToLibrary=True,
            icon=icon,
        ),
    ]
)


pltf = platform.system()
if pltf == 'Windows':
    pass
elif pltf == 'Linux':
    pass
elif pltf == 'Darwin':
    build_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'build',
    )
    repair_dependence(build_path)
else:
    pass
