#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import copy

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import analyze_ratio
import format_analyzer_jws
import wls_data_set
import compiled_path


wls_default_file_path = os.path.abspath('wls_default.txt')


class qt_push_button(QPushButton):
    def __init__(self, parent=None, _size_wh=(35, 35), _icon_size_wh=(20, 20)):
        super().__init__(parent)
        self.size_wh = _size_wh
        self.cursor = Qt.PointingHandCursor
        self.tooltip = ''
        self.backcolor = '0, 255, 255'
        self.icon_path = ''
        self.icon_size_wh = _icon_size_wh
        self.setAcceptDrops(False)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(False)

        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        _palette = QPalette()
        _palette.setColor(QPalette.Background, QColor(self.backcolor))
        self.setPalette(_palette)
        self.setCursor(self.cursor)

        self.change_ui()
        self.show()

    def change_ui(self):
        self.setFixedSize(self.size_wh[0], self.size_wh[1])
        self.setToolTip(self.tooltip)
        self.setIcon(QIcon(self.icon_path))
        self.setIconSize(QSize(self.icon_size_wh[0], self.icon_size_wh[1]))

    def wheelEvent(self, _event):
        return QWidget.wheelEvent(self, _event)


class qt_file_dialog(QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.open_paths = []
        self.open_path = ''
        self.save_path = ''
        self.dir_open_paths = ''
        self.dir_open_path = ''
        self.dir_save_path = ''

    def load_files_dialog(self, _file_filter='all (*.*)'):
        self.open_paths, _ = self.getOpenFileNames(
            None,
            'Open Files',
            self.dir_open_paths,
            _file_filter
        )
        return self.open_paths

    def load_file_dialog(self, _file_filter='all (*.*)'):
        self.open_path, _ = self.getOpenFileName(
            None,
            'Open File',
            self.dir_open_path,
            _file_filter
        )
        return self.open_path

    def save_file_dialog(self, _file_filter='all (*.*)'):
        self.save_path, _ = self.getSaveFileName(
            None,
            'Save File',
            self.dir_save_path,
            _file_filter,
        )
        return self.save_path


class qt_text_label(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        self.setAcceptDrops(False)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(False)
        _palette = QPalette()
        _palette.setColor(QPalette.Foreground, QColor('black'))
        self.setPalette(_palette)

        self.setText('File List')

        _font = QFont('Times New Roman')
        _font.setPointSize(16)
        _font.setBold(False)
        _font.setWeight(1)
        self.setFont(_font)

        self.setCursor(Qt.ArrowCursor)

        self.setWordWrap(True)

        self.show()

    def wheelEvent(self, _event):
        return QWidget.wheelEvent(self, _event)


class qt_list_view(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(False)
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(False)
        _palette = QPalette()
        _palette.setColor(QPalette.Foreground, QColor('black'))
        self.setPalette(_palette)
        self.setCursor(Qt.ArrowCursor)
        _font = QFont('Times New Roman')
        _font.setPointSize(12)
        _font.setBold(False)
        _font.setWeight(1)
        self.setFont(_font)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.show()

    def wheelEvent(self, _event):
        return QWidget.wheelEvent(self, _event)


class qt_open_file_list(QWidget):
    itemAdd = pyqtSignal(str)
    itemDel = pyqtSignal(QListWidgetItem)
    itemReset = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dialog = qt_file_dialog()
        self.setAcceptDrops(True)
        self.setMinimumSize(100, 200)
        self.margin = 10
        self.initUI()
        self.item_brush = QBrush()
        self.item_brush.setStyle(Qt.SolidPattern)

    def initUI(self):
        self.setAutoFillBackground(False)

        self.title_label = qt_text_label(self)

        self.FileOpenBtn = qt_push_button(self, (40, 40), (32, 32))
        self.FileOpenBtn.tooltip = 'Open Files'
        self.FileOpenBtn.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'add.png')
        self.FileOpenBtn.change_ui()
        self.FileOpenBtn.clicked.connect(self._open_file_dialog)

        self.FileDelBtn = qt_push_button(self, (40, 40), (32, 32))
        self.FileDelBtn.tooltip = 'Del Files'
        self.FileDelBtn.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'del.png')
        self.FileDelBtn.change_ui()
        self.FileDelBtn.clicked.connect(self._del_file_event)

        self.ResetBtn = qt_push_button(self, (40, 40), (32, 32))
        self.ResetBtn.tooltip = 'Reset List'
        self.ResetBtn.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'reset.png')
        self.ResetBtn.change_ui()
        self.ResetBtn.clicked.connect(self._reset_list_event)

        self.list_wid = qt_list_view(self)

        self.v_4 = QVBoxLayout()
        self.v_4.setContentsMargins(0, 0, 0, 0)
        self.v_4.setSpacing(0)
        self.v_4.addWidget(self.FileOpenBtn)

        self.v_5 = QVBoxLayout()
        self.v_5.setContentsMargins(0, 0, 0, 0)
        self.v_5.setSpacing(0)
        self.v_5.addWidget(self.FileDelBtn)

        self.v_6 = QVBoxLayout()
        self.v_6.setContentsMargins(0, 0, 0, 0)
        self.v_6.setSpacing(0)
        self.v_6.addWidget(self.ResetBtn)

        self.h_10 = QHBoxLayout()
        self.h_10.setContentsMargins(0, 0, 0, 0)
        self.h_10.setSpacing(0)
        self.h_10.addWidget(self.title_label)
        self.h_10.addStretch(10)
        self.h_10.addSpacing(1)
        self.h_10.addLayout(self.v_4)
        self.h_10.addStretch(0)
        self.h_10.addSpacing(1)
        self.h_10.addLayout(self.v_5)
        self.h_10.addStretch(0)
        self.h_10.addSpacing(1)
        self.h_10.addLayout(self.v_6)

        self.h_20 = QHBoxLayout()
        self.h_20.setContentsMargins(0, 0, 0, 0)
        self.h_20.setSpacing(0)
        self.h_20.addWidget(self.list_wid)

        self.v_10 = QVBoxLayout()
        self.v_10.setContentsMargins(self.margin, self.margin, self.margin,
                                     self.margin)
        self.v_10.setSpacing(0)
        self.v_10.addLayout(self.h_10)
        self.v_10.addLayout(self.h_20)

        self.setLayout(self.v_10)

        self.show()

    def _open_file_dialog(self):
        self.dialog.load_files_dialog('jws (*.jws);;all (*.*)')
        for _file_path in self.dialog.open_paths:
            self.add_file_path(_file_path)

    def add_file_path(self, _file_path):
        self.itemAdd.emit(_file_path)

    def _del_file_event(self, _event):
        self.del_file()

    def del_file(self):
        for _i in self.list_wid.selectedItems():
            self.list_wid.takeItem(self.list_wid.row(_i))
            self.itemDel.emit(_i)

    def _reset_list_event(self, _event):
        if self.list_wid.count() >= 1:
            _confirm = QMessageBox.question(
                self, 'Confirm', 'Reset file list?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if _confirm == QMessageBox.Yes:
                self.reset_list()

    def reset_list(self):
        self.itemReset.emit()

    def dragEnterEvent(self, _event):
        mimedata = _event.mimeData()
        if mimedata.hasUrls():
            _event.accept()
        else:
            _event.ignore()

    def dropEvent(self, _event):
        _mimedata = _event.mimeData()
        if not _mimedata.hasUrls():
            _event.ignore()
            return
        for _url in _mimedata.urls():
            _file_path = _url.toLocalFile()
            self.add_file_path(_file_path)

    def wheelEvent(self, _event):
        return QWidget.wheelEvent(self, _event)

    def keyPressEvent(self, _event):
        if _event.key() == Qt.Key_Delete:
            self.del_file()


class fluorometer_analysis_gui(QMainWindow):
    def __init__(self, _disp_info, parent=None):
        super().__init__(parent)
        self._disp_info = _disp_info
        self.dialog = qt_file_dialog()
        self.mw_w = 300
        self.mw_h = 500
        self.margin = 10
        self.initUI()
        self.all_items = []
        self.accum_items = []
        self.wls_mode = ''
        self.wls_dict = {}
        self._load_wls_data_set()
        self.setting_widget = setting_widget(self)

    def initUI(self):
        self.setStyleSheet('QMainWindow{background-color: rgb(159, 223, 190);'
                           'border: 3px solid rgb(204, 0, 0);}')

        _pos_x = int(self._disp_info['avail_size'].width() / 2 - self.mw_w / 2)
        _pos_y = int(
            self._disp_info['avail_size'].height() / 2 - self.mw_h / 2)
        self.setGeometry(_pos_x, _pos_y, self.mw_w, self.mw_h)

        self.setWindowTitle('Fluorometer Analysis')

        self.main_widget = QWidget(self)

        self.output_button = qt_push_button(self, (100, 40), (92, 32))
        self.output_button.tooltip = 'Output csv'
        self.output_button.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'output.png')
        self.output_button.change_ui()
        self.output_button.clicked.connect(self._start_calculation_event)

        self.setting_button = qt_push_button(self, (40, 40), (32, 32))
        self.setting_button.tooltip = 'Setting'
        self.setting_button.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'setting.png')
        self.setting_button.change_ui()
        self.setting_button.clicked.connect(self._setting_event)

        self.only_accum = QCheckBox(self)
        self.only_accum.tooltip = 'Only Accumulation Sample(s)'
        self.only_accum.setText('Only Accumulation Sample(s)')
        self.only_accum.setChecked(True)
        _font = QFont('Times New Roman')
        _font.setPointSize(13)
        _font.setBold(False)
        _font.setWeight(1)
        self.only_accum.setFont(_font)
        self.only_accum.stateChanged.connect(self._only_accum_event)

        self.open_file_list = qt_open_file_list(self)
        self.open_file_list.itemAdd.connect(self._item_add_event)
        self.open_file_list.itemDel.connect(self._item_del_event)
        self.open_file_list.itemReset.connect(self._item_reset_event)

        self.h_10 = QHBoxLayout()
        self.h_10.setContentsMargins(0, 0, 0, 0)
        self.h_10.setSpacing(10)
        self.h_10.addWidget(self.output_button)
        self.h_10.addStretch(10)
        self.h_10.addWidget(self.setting_button)

        self.h_20 = QHBoxLayout()
        self.h_20.setContentsMargins(0, 0, 0, 0)
        self.h_20.setSpacing(10)
        self.h_20.addSpacing(10)
        self.h_20.addWidget(self.only_accum)

        self.h_30 = QHBoxLayout()
        self.h_30.setContentsMargins(0, 0, 0, 0)
        self.h_30.setSpacing(10)
        self.h_30.addWidget(self.open_file_list)

        self.v_10 = QVBoxLayout()
        self.v_10.setContentsMargins(self.margin, self.margin, self.margin,
                                     self.margin)
        self.v_10.setSpacing(10)
        self.v_10.addLayout(self.h_10)
        self.v_10.addLayout(self.h_20)
        self.v_10.addLayout(self.h_30)

        self.main_widget.setLayout(self.v_10)

        self.resize_replace_items()

        self.show()

    def _load_wls_data_set(self):
        self.wls_dict = wls_data_set.wls_dict
        self.wls_dict.update({
            'User Custom': {'wl_list': [687.0, 713.0],
                            'zero_wl_region': (600.0, 675.0), }, })
        _wls_mode = None
        if os.path.isfile(wls_default_file_path):
            _f = open(wls_default_file_path, 'r')
            _cont = _f.read()
            _f.close()
            if _cont in self.wls_dict:
                _wls_mode = _cont
        if _wls_mode is None:
            _wls_mode = sorted(list(self.wls_dict))[0]
            _f = open(wls_default_file_path, 'w')
            _f.write(_wls_mode)
            _f.close()
        self.wls_mode = _wls_mode

    def _item_add(self, _file_path):
        _base_name = os.path.basename(_file_path)
        _name, _ext = os.path.splitext(_base_name)
        _disp_name = _base_name
        _item_data = {
            'disp_name': str(_base_name),
            'path': _file_path,
        }
        for _i in self.all_items:
            _ref_item_data = _i.data(Qt.UserRole)
            if _item_data['path'] == _ref_item_data['path']:
                self._del_item(_i)

        _file_path = _item_data['path']
        _xy_dict, _info_dict = format_analyzer_jws.load_jws(_file_path)

        if _xy_dict is None or _info_dict is None:
            return

        _item_data['xy_dict'] = _xy_dict
        _item_data['info_dict'] = _info_dict
        _item = QListWidgetItem()
        _item.setText(_item_data['disp_name'])
        _item.setData(Qt.UserRole, _item_data)

        self.all_items.append(_item)
        if _item_data['info_dict']['accumulation']:
            self.accum_items.append(_item)

        if self.only_accum.isChecked() is False or \
           self.only_accum.isChecked() and \
           _item_data['info_dict']['accumulation']:
            self.open_file_list.list_wid.addItem(_item)
            self.open_file_list.list_wid.sortItems()

    def _item_add_event(self, _file_path):
        self._item_add(_file_path)

    def _del_item(self, _item):
        self.open_file_list.list_wid.takeItem(
            self.open_file_list.list_wid.row(_item))
        if _item in self.all_items:
            self.all_items.remove(_item)
        if _item in self.accum_items:
            self.accum_items.remove(_item)

    def _item_del_event(self, _item):
        self._del_item(_item)

    def _reset_item(self):
        self.all_items = []
        self.accum_items = []
        self.open_file_list.list_wid.clear()

    def _item_reset_event(self):
        self._reset_item()

    def _hide_all_items(self):
        for _i in self.all_items:
            self.open_file_list.list_wid.takeItem(
                self.open_file_list.list_wid.row(_i))

    def _active_items(self):
        _active_items = []
        if self.only_accum.isChecked():
            _active_items = self.accum_items
        else:
            _active_items = self.all_items
        return _active_items

    def _show_active_items(self):
        self._hide_all_items()
        _active_items = self._active_items()
        for _i in _active_items:
            self.open_file_list.list_wid.addItem(_i)
        self.open_file_list.list_wid.sortItems()

    def _only_accum_event(self, _event):
        self._show_active_items()

    def resize_replace_items(self):
        self.main_widget.setGeometry(
            0, 0, self.size().width(), self.size().height())

    def resizeEvent(self, _event):
        self.mw_w = self.width()
        self.mw_h = self.height()
        self.resize_replace_items()
        return QWidget.resizeEvent(self, _event)

    def _start_calculation_event(self, _event):
        if self.open_file_list.list_wid.count() == 0:
            return

        _file_list = []
        for _i in range(self.open_file_list.list_wid.count()):
            _item_data = self.open_file_list.list_wid.item(_i).data(
                Qt.UserRole)
            _file_list.append(_item_data['path'])

        self.dialog.dir_save_path = str(datetime.datetime.now().strftime(
                                        '%Y%m%d_%H%M%S'))
        self.dialog.save_file_dialog('csv (*.csv)')
        self.save_path = self.dialog.save_path
        if self.save_path == '':
            return

        _wl_list = self.wls_dict[self.wls_mode]['wl_list']
        _zero_wl_region = self.wls_dict[self.wls_mode][
            'zero_wl_region']

        _result_data = analyze_ratio.analyze_ratio_files(
            _file_list, _wl_list, _zero_wl_region)

        _base_abspath, _ext = os.path.splitext(self.save_path)
        _ext = '.csv'

        _file_name_list = _result_data['file_name_list']
        _ratio_val_list = _result_data['ratio_val_list']

        _header = []
        _data = []
        for _i, _i2 in zip(_file_name_list, _ratio_val_list):
            _header = ['FileName']
            _file_data = [_i]
            for _k in sorted(_i2.keys()):
                for _k2 in sorted(_i2[_k].keys()):
                    _file_data.append(_i2[_k][_k2])
                    if _k2 == 'zero':
                        _header.append(str(_k) + ' (-zero)')
                    else:
                        _header.append(str(_k))
            _data.append(_file_data)
        _output_abspath = str(_base_abspath) + '_ratio' + _ext
        analyze_ratio.output_csv(_output_abspath, _header, _data)

        _wl_all = _result_data['wl_all']
        _all_data_dict = _result_data['all_data_dict']
        _empty_data = _result_data['empty_data']

        _header_temp = ['WaveLength']
        _data_temp = [_wl_all]
        for _k, _v in _all_data_dict.items():
            for _k2, _v2 in _v.items():
                _header = copy.deepcopy(_header_temp)
                _header.extend(_file_name_list)
                _data = copy.deepcopy(_data_temp)
                _data.extend(_v2)
                if _k2 == 'zero':
                    _method = '_' + _k + '_zero'
                else:
                    _method = '_' + _k
                _output_abspath = str(_base_abspath) + '_data' + _method + _ext
                analyze_ratio.output_csv(_output_abspath, _header, _data, True)

    def _setting_event(self, _event):
        self.setting_widget.reset_value()
        if self.setting_widget.exec_():
            self.wls_mode = self.setting_widget.wls_mode
            self.wls_dict = self.setting_widget.wls_dict
            _f = open(wls_default_file_path, 'w')
            _f.write(self.wls_mode)
            _f.close()


class setting_widget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.w = 400
        self.h = 200
        self.margin = 10
        self.wls_mode = parent.wls_mode
        self.wls_dict = parent.wls_dict
        self.wls_list = sorted(list(self.wls_dict))
        self.initUI()
        self.reset_value()

    def initUI(self):
        self.reset_geometry()

        self.setWindowTitle('Setting')

        self.data_set_label = QLabel('Data Set')
        self.data_set_label.setFont(QFont('Times New Roman', 14))
        self.data_set = QComboBox(self)
        self.data_set.setFont(QFont('Times New Roman', 14))
        _list_model = QStringListModel(self.wls_list)
        self.data_set.setModel(_list_model)
        self.data_set.currentIndexChanged.connect(self._data_set_change_event)

        self.ref_wls_label = QLabel('Reference Wavelength(s)')
        self.ref_wls_label.setFont(QFont('Times New Roman', 14))
        self.ref_wls = QLineEdit(self)
        self.ref_wls.setFont(QFont('Times New Roman', 15))

        self.zero_wls_label = QLabel('Zero Region')
        self.zero_wls_label.setFont(QFont('Times New Roman', 14))
        self.zero_wls = QLineEdit(self)
        self.zero_wls.setFont(QFont('Times New Roman', 15))

        self.error_label1 = QLabel('')
        self.error_label1.setFont(QFont('Times New Roman', 14))
        self.error_label1.setStyleSheet('color: rgb(255, 0, 0);')
        self.error_label2 = QLabel('')
        self.error_label2.setFont(QFont('Times New Roman', 12))
        self.error_label2.setStyleSheet('color: rgb(255, 0, 0);')

        self.ok_button = qt_push_button(self, (100, 40), (92, 32))
        self.ok_button.tooltip = 'OK'
        self.ok_button.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'save.png')
        self.ok_button.change_ui()
        self.ok_button.clicked.connect(self._ok_event)

        self.cancel_button = qt_push_button(self, (100, 40), (32, 32))
        self.cancel_button.tooltip = 'Cancel'
        self.cancel_button.icon_path = os.path.join(
            compiled_path.own_dir_path(), 'icon', 'cancel.png')
        self.cancel_button.change_ui()
        self.cancel_button.clicked.connect(self._cancel_event)

        self.v_10 = QVBoxLayout()
        self.v_10.setContentsMargins(0, 0, 0, 0)
        self.v_10.setSpacing(10)
        self.v_10.addWidget(self.data_set_label)
        self.v_10.addStretch(1)
        self.v_10.addWidget(self.ref_wls_label)
        self.v_10.addStretch(1)
        self.v_10.addWidget(self.zero_wls_label)
        self.v_10.addStretch(1)
        self.v_10.addWidget(self.error_label1)
        self.v_10.addStretch(10)

        self.v_20 = QVBoxLayout()
        self.v_20.setContentsMargins(0, 0, 0, 0)
        self.v_20.setSpacing(10)
        self.v_20.addWidget(self.data_set)
        self.v_20.addStretch(1)
        self.v_20.addWidget(self.ref_wls)
        self.v_20.addStretch(1)
        self.v_20.addWidget(self.zero_wls)
        self.v_20.addStretch(1)
        self.v_20.addWidget(self.error_label2)
        self.v_20.addStretch(10)

        self.h_10 = QHBoxLayout()
        self.h_10.setContentsMargins(0, 0, 0, 0)
        self.h_10.setSpacing(10)
        self.h_10.addLayout(self.v_10)
        self.h_10.addLayout(self.v_20)

        self.h_30 = QHBoxLayout()
        self.h_30.setContentsMargins(0, 0, 0, 0)
        self.h_30.setSpacing(10)
        self.h_30.addStretch(10)
        self.h_30.addWidget(self.ok_button)
        self.h_30.addWidget(self.cancel_button)

        self.v_30 = QVBoxLayout()
        self.v_30.setContentsMargins(self.margin, self.margin, self.margin,
                                     self.margin)
        self.v_30.setSpacing(10)
        self.v_30.addLayout(self.h_10)
        self.v_30.addStretch(10)
        self.v_30.addLayout(self.h_30)

        self.setLayout(self.v_30)

        self.resize_replace_items()

    def reset_geometry(self):
        _pos_x = int(self.parent.pos().x() + self.parent.mw_w / 2 - self.w / 2)
        _pos_y = int(self.parent.pos().y() + self.parent.mw_h / 2 - self.h / 2)
        self.setGeometry(_pos_x, _pos_y, self.w, self.h)

    def resize_replace_items(self):
        pass

    def resizeEvent(self, _event):
        self.resize_replace_items()
        return QWidget.resizeEvent(self, _event)

    def _data_set_change_event(self, _event):
        self.reset_value()

    def create_input_info(self):
        _error_list = []
        _error_info = []

        _ref_wls = self.ref_wls.text().split(',')
        _ref_wls = [_i.strip() for _i in _ref_wls]
        _ref_wls_float = []
        for _i in _ref_wls:
            if _i.replace('.', '', 1).isdigit():
                _ref_wls_float.append(float(_i))
            else:
                _error_list.append(self.ref_wls)
                _error_info.append(
                    'Reference Wavelength(s) must be Integer or Float.')
                break

        _zero_wls = self.zero_wls.text().split(',')
        _zero_wls = [_i.strip() for _i in _zero_wls]
        _zero_wls_float = []
        for _i in _zero_wls:
            if _i.replace('.', '', 1).isdigit():
                _zero_wls_float.append(float(_i))
            else:
                _error_list.append(self.zero_wls)
                _error_info.append('Zero Region must be Integer or Float.')
                break

        if len(_zero_wls) != 2:
            _error_list.append(self.zero_wls)
            _error_info.append(
                'Zero Region must be two numerics that is start position '
                'and end position.')

        return _ref_wls_float, _zero_wls_float, _error_list, _error_info

    def _ok_event(self, _event):
        _ref_wls_float, _zero_wls_float, _error_list, _error_info = \
            self.create_input_info()

        if _error_list == []:
            _k = self.data_set.itemText(self.data_set.currentIndex())
            self.wls_mode = _k
            if _k == 'User Custom':
                self.wls_dict['User Custom'] = {
                    'wl_list': _ref_wls_float,
                    'zero_wl_region': tuple(_zero_wls_float), }
            self.accept()
        else:
            self.ref_wls.setStyleSheet('color: rgb(0, 0, 0);')
            self.zero_wls.setStyleSheet('color: rgb(0, 0, 0);')
            for _i in _error_list:
                _i.setStyleSheet('color: rgb(255, 0, 0);')
            self.error_label1.setText('Error Info: ')
            self.error_label2.setText('\n'.join(map(str, _error_info)))

    def _cancel_event(self, _event):
        self.close()

    def showEvent(self, _event):
        _index = 0
        if self.wls_mode in self.wls_list:
            _index = self.wls_list.index(self.wls_mode)
        self.data_set.setCurrentIndex(_index)
        self.reset_value()
        self.reset_geometry()

    def closeEvent(self, _event):
        self.reset_value()
        self.reset_geometry()

    def _obj_set_text(self, _obj, _array):
        _obj.setText(', '.join(map(str, _array)))

    def reset_value(self):
        _k = self.data_set.itemText(self.data_set.currentIndex())
        if _k == 'User Custom':
            self.ref_wls.setReadOnly(False)
            self.zero_wls.setReadOnly(False)
        else:
            self.ref_wls.setReadOnly(True)
            self.zero_wls.setReadOnly(True)
        _wl_list = self.wls_dict[_k]['wl_list']
        self._obj_set_text(self.ref_wls, _wl_list)
        _zero_wl_region = self.wls_dict[_k]['zero_wl_region']
        self._obj_set_text(self.zero_wls, _zero_wl_region)
        self.ref_wls.setStyleSheet('color: rgb(0, 0, 0);')
        self.zero_wls.setStyleSheet('color: rgb(0, 0, 0);')
        self.error_label1.setText('')
        self.error_label2.setText('')


def main():
    app = QApplication(sys.argv)

    _disp = app.primaryScreen()
    _disp_info = {
        'name': _disp.name(),
        'size': _disp.size(),
        'avail_size': _disp.availableGeometry(),
    }

    exec = fluorometer_analysis_gui(_disp_info)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
