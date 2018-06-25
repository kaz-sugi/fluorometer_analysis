#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import os
import sys


def own_dir_path():
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.realpath(__file__))
    return path
