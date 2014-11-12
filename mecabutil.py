#!/usr/bin/python
# -*- coding: utf-8 -*-

import MeCab
import re

# Wordクラス定義
class Word:
    # コンストラクタ
    def __init__(self, surface = None, pos = None, pos_detail1 = None, pos_detail2 = None, pos_detail3 = None):
        self.set_field(surface, pos, pos_detail1, pos_detail2, pos_detail3)       
        
    # セッター
    def set_field(self, surface, pos, pos_detail1, pos_detail2, pos_detail3):
        self.surface = surface
        self.pos = pos
        self.pos_detail1 = pos_detail1
        self.pos_detail2 = pos_detail2
        self.pos_detail3 = pos_detail3

    # ゲッター
    def get_surface(self):
        return self.surface

    def get_pos(self):
        return self.pos

    def get_pos_detail1(self):
        return self.pos_detail1

    def get_pos_detail2(self):
        return self.pos_detail2

    def get_pos_detail3(self):
        return self.pos_detail3

def get_words(string):
    enc_string = string.encode("utf-8")

    result = MeCab.Tagger("")\
                  .parse(enc_string)\
                  .decode("utf-8")

    lines = result.split("\n")
    pattern = r"^(.*?)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)$"
    word_arr = []
    for line in lines:
        iterator = re.finditer(pattern, line)
        for match in iterator:
            surface = match.group(1)
            pos = match.group(2)
            pos_detail1 = match.group(3)
            pos_detail2 = match.group(4)
            pos_detail3 = match.group(5)

            word = Word(surface, pos, pos_detail1, pos_detail2, pos_detail3)
            word_arr.append(word)

    return word_arr

# Wordクラスの情報出力関数
def print_word(word):
    print(word.get_surface()) ,
    print(word.get_pos()) ,
    print(word.get_pos_detail1()) ,
    print(word.get_pos_detail2()) ,
    print(word.get_pos_detail3())
