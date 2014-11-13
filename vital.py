#!/usr/bin/python
# -*- coding: utf-8 -*-

# 日本語対応prettyprint
# 参考：http://qiita.com/HirofumiYashima/items/4a5d6f1f0a23e787bc34
def pp(obj):
    import re, pprint

    pp = pprint.PrettyPrinter(indent=4, width=160)
    str = pp.pformat(obj)

    print( re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str) )

def file_list(directory_path):
    import os

    file_list = os.listdir(directory_path)
    absolute_filepath = [directory_path + file_name for file_name in file_list]

    return absolute_filepath

# ファイルを読み込み，文字コード変換
def file_read(file_path):
    import nkf

    # ファイルオープン
    contents = open(file_path).read()
    contents = nkf.nkf("-w -d", contents)\
            .decode("utf_8")

    return contents

def dict_cosine(dict1, dict2):
    import scipy.spatial.distance

    # 基底となる単語の和集合を計算
    keys = set( dict1.keys() ) | set( dict2.keys() )

    # 次元を揃えて，dictからコサイン類似度計算用のベクトルを生成
    vector1 = [ dict1.get(key, 0) for key in keys]
    vector2 = [ dict2.get(key, 0) for key in keys]

    # cosine でコサイン距離を計算，1-cosineでコサイン類似度となる．
    sim = 1 - scipy.spatial.distance.cosine(vector1, vector2)

    return sim

def parse(file_path, separator):
    import re

    f = open(file_path)
    result = [line.strip("\n").decode("utf-8").split(separator) for line in f]

    return result

