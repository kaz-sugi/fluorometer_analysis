#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import struct
import datetime
import time


def convert_bytes_to_num(_bytes_data, _pos, _convert_type='f'):
    _float = []
    _data_size = 4
    for i in _pos:
        _num = struct.unpack(_convert_type, _bytes_data[i:i + _data_size])[0]
        _float.append(_num)
    return _float


def decode_bytes(_bytes_data, _pos, _char_code='latin-1'):
    _info = []
    for i in range(len(_pos) - 1):
        _info_bytes = _bytes_data[_pos[i]:_pos[i + 1]]
        _info.append(_info_bytes.decode(_char_code).strip('\x00').strip()
                     .replace('\x00', ' '))
    return _info


def load_jws(_file_abspath):
    # Model: FP-6500
    # Software (Spectra Manager): Ver. 1.54B
    # Software (Instrument driver): Ver. 1.07J

    _f = open(_file_abspath, 'rb')
    _all_data = _f.read()
    _f.close()

    _data_pos = [0 + _i for _i in range(8)]
    _format_header = ','.join([str(int(format(_all_data[_i]), 16))
                               for _i in _data_pos])

    if _format_header != '118,294,131,50,1,0,1,304':
        return None, None

    _data_pos = [8, 16, 32, 48, 64, 80, 112, 128]
    _format_info = decode_bytes(_all_data, _data_pos)

    _data_pos = [208, 212, 216, 220]
    _run_info = convert_bytes_to_num(_all_data, _data_pos)

    _data_pos = [248, 280, 312]
    _machine_info = decode_bytes(_all_data, _data_pos)

    _data_pos = [312, 376, 504, 536, 632]
    _sample_info = decode_bytes(_all_data, _data_pos)

    _sec_info_list = [[_all_data[_i + _i2] for _i2 in range(4)]
                      for _i in [632, 636]]
    _epoch_list = []
    for _i in _sec_info_list:
        _sec_hex = ''
        for _i2 in _i[::-1]:
            _hex = format(_i2, 'x')
            if len(_hex) == 1:
                _hex = '0' + _hex
            _sec_hex += _hex
        _sec = int(_sec_hex, 16)
        if _sec != 0:
            _epoch_list.append(_sec)
    if _epoch_list == []:
        _epoch_list = [0]
    _epoch = min(_epoch_list)
    _datetime = datetime.datetime(*time.localtime(_epoch)[:6])

    _data_pos = [780, 796, 812, 828, 844, 860, 884, 908]
    _param_info = decode_bytes(_all_data, _data_pos)

    _data_pos = [1012, 1036]
    _delta_wl = decode_bytes(_all_data, _data_pos)[0]

    _data_pos = [1084, 1212]
    _accessory = decode_bytes(_all_data, _data_pos)[0]

    _data_pos = [_i for _i in range(1784, len(_all_data) + 1 - 4, 4)]
    _data = convert_bytes_to_num(_all_data, _data_pos)

    _data_pitch = (_run_info[2] - _run_info[0]) / (len(_data) - 1)

    _x = [_run_info[0] + _i * _data_pitch for _i in range(len(_data))]

    _mode = _all_data[1036]
    _mode_name = 'Unknown'
    if _mode == 0:
        _mode_name = 'Excitation Spectrum'
    elif _mode == 1:
        _mode_name = 'Emission Spectrum'
    elif _mode == 2:
        _mode_name = 'Sycronize Spectrum'
    elif _mode == 3:
        _mode_name = 'Excitation Single'
    elif _mode == 4:
        _mode_name = 'Emission Single'

    sample_id = _all_data[996]

    _accumulation = True
    if _all_data[924] == 0:
        _accumulation = False

    cycle_num = _all_data[1004] + _all_data[924]

    cycle_max = _all_data[1000]

    _info_dict = {
        'format_header': _format_header,
        'start_wl': _run_info[0],
        'end_wl': _run_info[1],

        'model_num': _machine_info[0],
        'serial_num': _machine_info[1],

        'sample_Name': _sample_info[0],
        'comment': _sample_info[1],
        'operator': _sample_info[2],
        'copyright': _sample_info[3],

        'datetime': _datetime,

        'band_width_ex': _param_info[0],
        'band_width_em': _param_info[1],
        'sensitivity': _param_info[2],
        'response': _param_info[3],
        'scanning_speed': _param_info[4],
        'excitation_wl': _param_info[5],
        'emission_wl': _param_info[6],

        'delta_wl': _delta_wl,
        'accessory': _accessory,
        'data_pitch': _data_pitch,

        'mode': _mode,
        'mode_name': _mode_name,
        'sample_id': sample_id,
        'accumulation': _accumulation,
        'cycle_num': cycle_num,
        'cycle_max': cycle_max,
    }

    _xy_dict = {
        'x': _x,
        'y': _data,
    }

    return _xy_dict, _info_dict

