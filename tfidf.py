#%!/usr/bin/python
# -*- coding: utf-8 -*-

def get_tf(file_path):
    """
    引数のファイルを読み込み，TFを計算する．
    
    Args:
        file_path: TFを計算するファイルの相対，または絶対パス．

    Returns:
        単語とそのTF値を組にした辞書型．
    """
    import vital        # 自作，よく使う処理群
    import mecabutil    # 自作，MeCabのwrapperとそのクラス

    tf = {}

    # ファイル読み込み
    contents = vital.file_read(file_path)

    # 形態素解析し，結果をWordクラスの配列に格納
    words = mecabutil.get_words(contents)
    
    # 形態素解析結果から，名詞の単語の表層のみを抽出
    nouns = [word.surface for word in words if word.pos == u"名詞"]

    # 名詞の集合(重複なし)を用意し，各名詞毎に出現回数をカウントする
    for key in set(nouns):
        tf[key] = float( nouns.count(key) ) / float( len(nouns) )

    return tf

def get_idf(directory_path):
    """
    ディレクトリ中の全ファイルからidf値を計算する．

    Args:
        directory_path: idfを計算するファイル群が存在するディレクトリの相対，または絶対パス．

    Returns:
        単語とそのIDF値を組にした辞書型．
    """
    import vital        # 自作，よく使う処理群
    import mecabutil    # 自作，MeCabのwrapperとそのクラス
    import math

    files = vital.get_abs_path(directory_path)   

    df = {}
    idf = {}
    df_default = 0  # dfハッシュのデフォルト値

    for file in files:
        contents = vital.file_read(file)

        # 形態素解析し，結果をWordクラスの配列に格納
        words = mecabutil.get_words(contents)
        
        # 形態素解析結果から，名詞の単語の表層のみを抽出
        nouns = [word.surface for word in words if word.pos == u"名詞"]

        # 文書中の名詞を集合(重複なしの要素の集まり)とし，存在する名詞のdf値をインクリメント
        for key in set(nouns):
            df[key] = df.get(key, df_default) + 1

        # dfからidfを計算
        for k,v in df.items():
            idf[k] = math.log10( 1.0 + (len(files) / v) )


    return idf

def get_tfidf(tf, idf):
    """
    TFとIDFからTF-IDFを計算する．

    Args:
        tf:  単語とそのTF値を組に持つ辞書型．
        idf: 単語とそのIDF値を組に持つ辞書型．
    
    Returns:
        単語とそのTF-IDF値を組に持つ辞書型．
    """
    tfidf = {}
    idf_unknown = 0 #未知語のidf値．0は不適切だが，今は考えない．

    for k,v in tf.items():
        tfidf[k] = v * idf.get(k, idf_unknown)

    return tfidf
