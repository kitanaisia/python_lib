#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import nkf

def get_abs_path(directory_path):
    file_list = os.listdir(directory_path)
    absolute_filepath = [directory_path + file_name for file_name in file_list]

    return absolute_filepath

# ファイルを読み込み，文字コード変換
def file_read(file_path):
    # ファイルオープン
    contents = open(file_path).read()
    contents = nkf.nkf("-w -d", contents)\
            .decode("utf_8")

    return contents
