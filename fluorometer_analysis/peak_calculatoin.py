#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-


def return_value(x, y, x_val):
    pos = x.index(x_val)
    selected_y = y[pos]

    return selected_y


def return_min_value(x, y, x_val_0, x_val_1):
    pos0 = x.index(x_val_0)
    pos1 = x.index(x_val_1)

    selected_y_list = y[pos0:pos1 + 1]
    min_y = min(selected_y_list)

    return min_y
