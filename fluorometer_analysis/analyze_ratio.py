#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import os
import csv
import copy

import format_analyzer_jws
import peak_calculatoin


def output_csv(_output_abspath, _header, _output_data, _do_zip=False):
    if _do_zip:
        _output_data = list(map(list, zip(*_output_data)))
    _f = open(_output_abspath, 'w', encoding='utf-8')
    _csv_writer = csv.writer(_f, lineterminator='\n')
    _csv_writer.writerow(_header)
    _csv_writer.writerows(_output_data)
    _f.close()


def collect_wl_value(_xy_dict, _wl_list, _zero_wl_region):
    _x = _xy_dict['x']
    _y = _xy_dict['y']

    _wl_val_dict = {}
    for _i in _wl_list:
        if _i in _x:
            _wl_val_dict[_i] = peak_calculatoin.return_value(_x, _y, _i)
        else:
            _wl_val_dict[_i] = None
    if _zero_wl_region[0] in _x and _zero_wl_region[1] in _x:
        _zero_val = peak_calculatoin.return_min_value(
            _x, _y, _zero_wl_region[0], _zero_wl_region[1])
    else:
        _zero_val = None
    _zero_revise = {'zero': _zero_val, '0': 0}
    return _wl_val_dict, _zero_revise


def calculate_ratio(_val_1, _val_2, _zero_val):
    _val_1_2_ratio = None
    if _val_1 is not None and _val_2 is not None and \
       _zero_val is not None:
        _val_1_zero = _val_1 - _zero_val
        _val_2_zero = _val_2 - _zero_val
        if _val_2_zero != 0:
            _val_1_2_ratio = _val_1_zero / _val_2_zero
        elif _val_1_zero == abs(_val_1_zero):
            _val_1_2_ratio = 'Inf'
        elif _val_1_zero != abs(_val_1_zero):
            _val_1_2_ratio = '-Inf'
    else:
        _val_1_2_ratio = '-'
    return _val_1_2_ratio


def calculate_all_ratio(_xy_dict, _std_wl_val, _zero_val):
    _x = _xy_dict['x']
    _y = _xy_dict['y']

    _ratio_list = [calculate_ratio(_i, _std_wl_val, _zero_val) for _i in _y]
    _ratio_dict = {str(_x[_i]): _ratio_list[_i]
                   for _i in range(len(_ratio_list))}

    return _ratio_dict


def create_std_vals(_wl_list, _wl_val_dict):
    _std_dict = {}
    _sum_std_list = []
    for _i2 in _wl_list:
        if _i2 in _wl_val_dict and _wl_val_dict[_i2] is not None:
            _std_dict[str(_i2)] = _wl_val_dict[_i2]
            if _sum_std_list is not None:
                _sum_std_list.append(_wl_val_dict[_i2])
        else:
            _std_dict[str(_i2)] = None
            _sum_std_list = [None]

    _std_with_sum_dict = {_k: [_v] for _k, _v in _std_dict.items()}
    _std_with_sum_dict['sum'] = _sum_std_list
    _std_with_sum_dict['raw'] = [1]

    return _std_dict, _std_with_sum_dict


def create_ratio_vals(_std_dict, _zero_revise):
    _ratio_val_dict = {}
    for _k, _v in _std_dict.items():
        for _k2, _v2 in _std_dict.items():
            if _k != _k2:
                _zero_diff_dict = {}
                for _k3, _v3 in _zero_revise.items():
                    if _v is not None and _v2 is not None and \
                       _v3 is not None:
                        _ratio_val = calculate_ratio(_v, _v2, _v3)
                        _zero_diff_dict[_k3] = _ratio_val
                    else:
                        _zero_diff_dict[_k3] = None
                _key_name = str(_k) + '/' + str(_k2)
                _ratio_val_dict[_key_name] = _zero_diff_dict

    return _ratio_val_dict


def create_ratio_all(_xy_dict, _std_with_sum_dict, _zero_revise):
    _ratio_all_dict = {}
    for _k, _v in _std_with_sum_dict.items():
        _zero_diff_dict = {}
        for _k2, _v2 in _zero_revise.items():
            if _v != [None] and _v2 is not None:
                if _k == 'sum':
                    _s = sum(_v) - _v2 * (len(_v) - 1)
                else:
                    _s = sum(_v)
                _ratio_dict = calculate_all_ratio(_xy_dict, _s, _v2)
                _zero_diff_dict[_k2] = _ratio_dict
            else:
                _zero_diff_dict[_k2] = None
        _ratio_all_dict[_k] = _zero_diff_dict

    return _ratio_all_dict


def analyze_ratio(_xy_dict, _wl_list, _zero_wl_region):
    _wl = _xy_dict['x']

    _wl_val_dict, _zero_revise = collect_wl_value(
        _xy_dict, _wl_list, _zero_wl_region)

    _std_dict, _std_with_sum_dict = create_std_vals(_wl_list, _wl_val_dict)

    _ratio_val_dict = create_ratio_vals(_std_dict, _zero_revise)

    _ratio_all_dict = create_ratio_all(_xy_dict, _std_with_sum_dict,
                                       _zero_revise)
    return _wl, _ratio_val_dict, _ratio_all_dict


def analyze_ratio_file(_file_path, _wl_list, _zero_wl_region):
    _xy_dict, _info_dict = format_analyzer_jws.load_jws(_file_path)

    _file_name = str(os.path.splitext(os.path.basename(_file_path))[0])

    _wl, _ratio_val_dict, _ratio_all_dict = analyze_ratio(
        _xy_dict, _wl_list, _zero_wl_region)

    return _file_name, _info_dict, _wl, _ratio_val_dict, _ratio_all_dict


def create_x_standard_dict(_x, _xy_dict):
    _vals = []
    if isinstance(_xy_dict, dict):
        for _i in _x:
            if _i in _xy_dict:
                _vals.append(_xy_dict[_i])
            else:
                _vals.append('')
    else:
        _vals = ['' for _i in _x]
    return _vals


def create_x_standard_dict_dict_list(_x, _xy_dict_dict_list):
    _all_data_dict = {}
    for _i in _xy_dict_dict_list:
        for _k, _v in _i.items():
            if _k not in _all_data_dict:
                _all_data_dict[_k] = {}
            for _k2, _v2 in _v.items():
                if _k2 not in _all_data_dict[_k]:
                    _all_data_dict[_k][_k2] = []
                _vals = create_x_standard_dict(_x, _v2)
                _all_data_dict[_k][_k2].append(_vals)
    return _all_data_dict


def analyze_ratio_files(_file_list, _wl_list, _zero_wl_region):
    _file_name_list = []
    _info_dict_list = []
    _wl_all = []
    _ratio_val_list = []
    _ratio_all_list = []
    for _i in sorted(_file_list):
        if not os.path.isfile(_i):
            continue

        _file_name, _info_dict, _wl, _ratio_val_dict, _ratio_all_dict = \
            analyze_ratio_file(_i, _wl_list, _zero_wl_region)

        _file_name_list.append(_file_name)

        _info_dict_list.append(_info_dict)

        _wl_all.extend(_wl)
        _wl_all = list(set(_wl_all))

        _ratio_val_list.append(_ratio_val_dict)

        _ratio_all_list.append(_ratio_all_dict)

    _wl_all = [str(_i) for _i in sorted(_wl_all)]

    _all_data_dict = create_x_standard_dict_dict_list(_wl_all, _ratio_all_list)

    _empty_data = ['' for _i in _wl_all]

    _result_data = {
        'file_name_list': _file_name_list,
        'info_dict_list': _info_dict_list,
        'wl_all': _wl_all,
        'ratio_val_list': _ratio_val_list,
        'all_data_dict': _all_data_dict,
        'empty_data': _empty_data,
    }

    return _result_data
