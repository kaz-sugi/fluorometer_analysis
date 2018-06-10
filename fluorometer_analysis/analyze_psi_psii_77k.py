#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import os
import csv
import datetime

import format_analyzer_jws
import peak_calculatoin


def output_csv(_output_abspath, _header, _output_data):
    _output_data = list(map(list, zip(*_output_data)))
    _f = open(_output_abspath, 'w')
    _csv_writer = csv.writer(_f, lineterminator='\n')
    _csv_writer.writerow(_header)
    _csv_writer.writerows(_output_data)
    _f.close()


def detect_ps1_ps2_ratio(_analyzed_jws):
    _x = _analyzed_jws['x']
    _y = _analyzed_jws['y']
    _ps2 = peak_calculatoin.return_value(_x, _y, 687)
    _ps1 = peak_calculatoin.return_value(_x, _y, 713)
    _min_y = peak_calculatoin.return_min_value(_x, _y, 600, 675)

    _ps1_ps2_ratio_dict = {
        'ps1/ps2': _ps1/_ps2,
        'min_y': _min_y,
        '(ps1-min_y)/(ps2-min_y)': (_ps1-_min_y)/(_ps2-_min_y),
    }

    return _ps1_ps2_ratio_dict


def analyze_analysis_dir():
    _dir_abspath = os.path.abspath(os.path.join('analysis'))
    _file_list = os.listdir(_dir_abspath)
    _ps1_ps2_ratio_dict_list = []
    for _i in sorted(_file_list):
        _file_abspath = os.path.join(_dir_abspath, _i)
        _analyzed_jws = format_analyzer_jws.load_jws(_file_abspath)
        _ps1_ps2_ratio_dict = detect_ps1_ps2_ratio(_analyzed_jws)
        _ps1_ps2_ratio_dict_list.append(_ps1_ps2_ratio_dict)

    _ps1_ps2_list = [_i['ps1/ps2'] for _i in _ps1_ps2_ratio_dict_list]
    _ps1_ps2_min_list = [_i['(ps1-min_y)/(ps2-min_y)'] for _i in
                         _ps1_ps2_ratio_dict_list]

    _now = str(datetime.datetime.now()).replace(' ', '').replace('-', '') \
           .replace(':', '').replace('.', '')
    _output_abspath = os.path.abspath(
        os.path.join(str(_now)+'_psi_psii_ratio.csv'))
    _header = ['file_name', 'ps1/ps2', '(ps1-min_y)/(ps2-min_y)']
    _output_data = [_file_list, _ps1_ps2_list, _ps1_ps2_min_list]
    output_csv(_output_abspath, _header, _output_data)


if __name__ == '__main__':
    analyze_analysis_dir()
