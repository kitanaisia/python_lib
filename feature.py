#!/usr/bin/python
# -*- coding: utf-8 -*-

def tf(file_path):
    #
    # 引数のファイルを読み込み，TFを計算する．
    #
    # Args:
    #     file_path: TFを計算するファイルの相対，または絶対パス．
    #
    # Returns:
    #     単語とそのTF値を組にした辞書型．
    #
    import vital        # 自作，よく使う処理群
    import mecabutil    # 自作，MeCabのwrapperとそのクラス

    # ファイル読み込み
    contents = vital.file_read(file_path)

    # 形態素解析し，結果をWordクラスの配列に格納
    words = mecabutil.get_words(contents)
    
    # 形態素解析結果から，名詞の単語の表層のみを抽出
    nouns = [word.surface for word in words if word.pos == u"名詞"]

    # 名詞の集合(重複なし)を用意し，各名詞毎に出現回数をカウントする
    tf = {key : ( float( nouns.count(key) ) / float( len(nouns) ) ) for key in set(nouns)}

    return tf

def idf(directory_path):
    # 
    # ディレクトリ中の全ファイルからidf値を計算する．
    # 
    # Args:
    #     directory_path: idfを計算するファイル群が存在するディレクトリの相対，または絶対パス．
    # 
    # Returns:
    #     単語とそのIDF値を組にした辞書型．
    # 
    import vital        # 自作，よく使う処理群
    import mecabutil    # 自作，MeCabのwrapperとそのクラス
    import math
    import collections

    files = vital.file_list(directory_path)   

    df = collections.defaultdict(int)

    for file in files:
        contents = vital.file_read(file)

        # 形態素解析し，結果をWordクラスの配列に格納
        words = mecabutil.get_words(contents)
        
        # 形態素解析結果から，名詞の単語の表層のみを抽出
        nouns = [word.surface for word in words if word.pos == u"名詞"]

        # 文書中の名詞を集合(重複なしの要素の集まり)とし，存在する名詞のdf値をインクリメント
        for key in set(nouns):
            df[key] += 1

    # dfからidfを計算
    idf = {k:math.log( 1.0 + ( len(files) ) / v ) for k,v in df.items()}

    return idf

def tfidf(tf, idf):
    # 
    # TFとIDFからTF-IDFを計算する．
    # 
    # Args:
    #     tf:  単語とそのTF値を組に持つ辞書型．
    #     idf: 単語とそのIDF値を組に持つ辞書型．
    # 
    # Returns:
    #     単語とそのTF-IDF値を組に持つ辞書型．
    #
    idf_unknown = 0 #未知語のidf値．0は不適切だが，今は考えない．

    tfidf = {k:v * idf.get(k,idf_unknown) for k,v in tf.items()}

    return tfidf

def doc_convolute(content_words, word2vec_model, ndim):
    # 
    # Args:
    #     content_words : 特徴量を計算する単語(内容語)のリスト，文字列のlist．
    #     word2vec_model: Word2Vec.load(model)したもの
    #     ndim:           modelの次元数．
    #
    import mecabutil
    import numpy
    from gensim.models import word2vec

    # 文中の名詞数(縦) * modelの次元数(横) の行列の生成
    matrix = numpy.zeros(ndim)  # いい初期化方法がないのでこれで
    for content_word in content_words:
        try:
            matrix = numpy.vstack([ matrix, word2vec_model[content_word] ])
            # matrix += word2vec_model[content_word]
        except:
            pass
            # matrix = numpy.vstack([ matrix, numpy.zeros(ndim)])

    # 変数初期化のために作成した0ベクトルを削除
    matrix = numpy.delete(matrix, 0, 0)

    ## エラー処理:1単語しか存在しない場合，畳み込み不可能．そのベクトルを返す
    if len(matrix) == 1:
        return matrix

    # ベクトルコンボルーション
    conv_matrix = numpy.zeros(ndim)
    for i in range(len(matrix)-1):
        conv_vector = numpy.convolve(matrix[i,:], matrix[i+1,:], "same")
        conv_matrix = numpy.vstack([ conv_matrix, conv_vector])

    ## 変数初期化のために作成した0ベクトルを削除
    conv_matrix = numpy.delete(conv_matrix, 0, 0)

    # 各行のMAX値を取得
    vector = numpy.array([max(row) for row in conv_matrix.T])

    return vector
