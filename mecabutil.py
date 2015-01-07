#!/usr/bin/python
# -*- coding: utf-8 -*-

# Wordクラス定義
class Word:
    # コンストラクタ
    def __init__(self, surface = None, pos = None, pos_detail1 = None, pos_detail2 = None, pos_detail3 = None, pos_detail4 = None, pos_detail5 = None, base_form = None, kana = None, pronounse = None):
        self.set_field(surface, pos, pos_detail1, pos_detail2, pos_detail3, pos_detail4, pos_detail5, base_form, kana, pronounse)       
        
    # セッター
    def set_field(self, surface, pos, pos_detail1, pos_detail2, pos_detail3, pos_detail4, pos_detail5, base_form, kana, pronounse):
        self.surface = surface
        self.pos = pos
        self.pos_detail1 = pos_detail1
        self.pos_detail2 = pos_detail2
        self.pos_detail3 = pos_detail3
        self.pos_detail4 = pos_detail4
        self.pos_detail5 = pos_detail5
        self.base_form = base_form
        self.kana = kana
        self.pronounce = pronounse

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

    def get_pos_detail4(self):
        return self.pos_detail4

    def get_pos_detail5(self):
        return self.pos_detail5

    def get_base_form(self):
        return self.base_form

    def get_kana(self):
        return self.kana

    def get_pronounce(self):
        return self.pronounce

def get_words(string):
    import MeCab
    import re
    import vital

    enc_string = string.encode("utf-8")

    result = MeCab.Tagger("--eos-format="" ")\
                  .parse(enc_string)\
                  .decode("utf-8")

    lines = result.split("\n")
    del lines[len(lines) - 1]

    # パターン1 数字や固有名詞の場合，featureが7つ
    pattern_short = r"^(.*?)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)$"
    pattern_long = r"^(.*?)\t(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)$"
    word_arr = []
    for line in lines:
        if re.match(pattern_long, line):
            iterator = re.finditer(pattern_long, line)
            for match in iterator:
                surface = match.group(1)
                pos = match.group(2)
                pos_detail1 = match.group(3)
                pos_detail2 = match.group(4)
                pos_detail3 = match.group(5)
                pos_detail4 = match.group(6)
                pos_detail5 = match.group(7)
                base_form = match.group(8)
                kana = match.group(9)
                pronounce = match.group(10)

                word = Word(surface, pos, pos_detail1, pos_detail2, pos_detail3, pos_detail4, pos_detail5, base_form, kana, pronounce)
                word_arr.append(word)
        else:
            iterator = re.finditer(pattern_short, line)
            for match in iterator:
                surface = match.group(1)
                pos = match.group(2)
                pos_detail1 = match.group(3)
                pos_detail2 = match.group(4)
                pos_detail3 = match.group(5)
                pos_detail4 = match.group(6)
                pos_detail5 = match.group(7)
                base_form = match.group(8)
                kana = "*"
                pronounce = "*"

                # 原型が登録されていない場合，表層単語を原型として用いる．
                if base_form == "*":
                    base_form = surface

                word = Word(surface, pos, pos_detail1, pos_detail2, pos_detail3, pos_detail4, pos_detail5, base_form, kana, pronounce)
                word_arr.append(word)

    return word_arr


# Wordクラスの情報出力関数
def print_word(word):
    print(word.get_surface()) ,
    print(word.get_pos()) ,
    print(word.get_pos_detail1()) ,
    print(word.get_pos_detail2()) ,
    print(word.get_pos_detail3()) ,
    print(word.get_pos_detail4()) ,
    print(word.get_pos_detail5()) ,
    print(word.get_base_form()) ,
    print(word.get_kana()) ,
    print(word.get_pronounce())
