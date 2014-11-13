python_lib
==========

They are my useful and frequently-used functions.

vital
=====
pp:prettyprintのwrapper.unicode文字列のリストの出力に対応．
file_list:ディレクトリ中のファイルの絶対パスをリストにして返す．  
file_read:ファイルを開き，utf-8に文字コード変換してからdecodeしたものを返す．  
dict_cosine:2辞書間のコサイン類似度を返す．  
parse:ファイルの各行を任意のセパレータで区切り，行毎にリストにして返す.  

tfidf
=====
tf:ファイル中の名詞のTFを計算する．  
idf:ディレクトリ中のファイルの名詞のIDFを計算する．  
tfidf:TFとIDFからTF-IDFを計算する．  

mecabutil
=========
get_words:文字列を形態素解析し，mecabutil.Wordクラスのリストにして返す．   
print_word:Wordクラスの各要素を1行に出力する．  
