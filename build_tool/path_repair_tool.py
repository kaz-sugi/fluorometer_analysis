#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import os
import glob
import subprocess


def shell_cmd(cmd):
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
    ).communicate()[0]


def change_filepath_excfile(file_path, file_names):
    cmd = ('otool -L ' + str(file_path))
    try:
        output = shell_cmd(cmd).decode('utf-8')
    except Exception:
        output = ''
    output_n = [str(s) for s in output.split('\n') if s]
    if len(output_n) >= 2:
        target = output_n[0]
        if target[-1] == ':':
            target = target[0:-1]
        for dep_info in output_n[1:]:
            if dep_info[0] == '\t':
                dep_info = dep_info[1:]
            dep_path = dep_info[0:dep_info.rfind(' (')]
            try:
                target_name = str(os.path.basename(target))
                dep_name = str(os.path.basename(dep_path))
                if (dep_name in file_names) is True:
                    result = shell_cmd(
                        'install_name_tool -change ' +
                        str(dep_path) + ' ' +
                        str(
                            os.path.join(
                                '@executable_path',
                                dep_name,
                            )
                        ) + ' ' +
                        str(target)
                    )
            except Exception:
                pass


def change_filepath_excfiles(file_paths):
    file_names = [os.path.basename(r) for r in file_paths]
    for file_path in file_paths:
        change_filepath_excfile(file_path, file_names)


def repair_dependence(build_path):
    print(build_path)

    dirs_files = os.listdir(build_path)
    dirs = [f for f in dirs_files if os.path.isdir(
        os.path.join(build_path, f))]

    for dir_name in dirs:
        dir_path = os.path.join(
            build_path,
            dir_name,
        )
        dir_file_paths = glob.glob(
            os.path.join(
                dir_path,
                '*',
            )
        )
        file_paths = [f for f in dir_file_paths if os.path.isfile(f)]
        change_filepath_excfiles(file_paths)

