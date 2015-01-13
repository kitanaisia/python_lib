#!/usr/bin/python
# -*- coding: utf-8 -*-

def tf(contents, content_poslist):
    #
    # 引数のファイルを読み込み，TFを計算する．
    #
    # Args:
    #     contents: TFを計算するUnicode型文字列．
    #     content_poslist:  内容語の品詞．内容語に対してのみtfを計算する．str型を要素に持つlist.
    #
    # Returns:
    #     単語とそのTF値を組にした辞書型．
    #
    import vital        # 自作，よく使う処理群
    import mecabutil    # 自作，MeCabのwrapperとそのクラス

    # 形態素解析し，結果をWordクラスの配列に格納
    words = mecabutil.get_words(contents)
    
    # 形態素解析結果から，名詞の単語の表層のみを抽出
    nouns = [word.base_form for word in words if word.pos in content_poslist]

    # 名詞の集合(重複なし)を用意し，各名詞毎に出現回数をカウントする
    tf = {key : ( float( nouns.count(key) ) / float( len(nouns) ) ) for key in set(nouns)}

    return tf

def idf(directory_path, content_poslist):
    # 
    # ディレクトリ中の全ファイルからidf値を計算する．
    # 
    # Args:
    #     directory_path:   idfを計算するファイル群が存在するディレクトリの相対，または絶対パス．
    #     content_poslist:  内容語の品詞．内容語に対してのみidfを計算する．str型を要素に持つlist.
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
        nouns = [word.base_form for word in words if word.pos in content_poslist]

        # 文書中の名詞を集合(重複なしの要素の集まり)とし，存在する名詞のdf値をインクリメント
        for key in set(nouns):
            df[key] += 1

    # dfからidfを計算
    idf = {k:math.log10( 1.0 + ( float (len(files) ) ) / float(v) ) for k,v in df.items()}

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
    # TODO:
    #     語彙が1単語の場合，構造が二重配列になって帰ってくる
    #
    import mecabutil
    import numpy
    import vital
    from gensim.models import word2vec

    # 型チェック．content_wordsがstringでも，1語単位でfor文が回り，エラーなく結果がでてしまうため．
    if not isinstance(content_words, list):
        raise Exception, "doc_convoluteの型がlist型でありません．"

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

    ## エラー処理:辞書にある語が1単語しかない場合，畳み込み不可能．そのベクトルを返す
    if len(matrix) == 1:
        return matrix

    ## エラー処理:入力単語全てがOOVの場合，ベクトル計算不可能．
    if matrix.ndim == 1:
        raise Exception, u"入力単語が全てOOV"

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

def keyword2vec(keywords, word2vec_model, ndim):
    # 
    # Args:
    #     keywords      : 文書中のキーワード群，文字列のlist．
    #     word2vec_model: Word2Vec.load(model)したもの
    #     ndim:           modelの次元数．
    #
    import vital
    import numpy
    from gensim.models import word2vec

    matrix = numpy.zeros(ndim)  # いい初期化方法がないのでこれで
    for word in keywords:
        try:
            matrix = numpy.vstack([ matrix, word2vec_model[word] ])
        except:
            pass

    # 変数初期化のために作成した0ベクトルを削除
    matrix = numpy.delete(matrix, 0, 0)

    ## エラー処理:入力単語全てがOOVの場合，ベクトル計算不可能．
    if matrix.ndim == 1:
        raise Exception, u"入力単語が全てOOV"

    # 各行のavg値を取得
    vector = numpy.array([sum(row) / float(len(row)) for row in matrix.T])
    # vector = numpy.array([max(row) for row in matrix.T])

    return vector

def n_similarity(words1, words2, model):
    import numpy
    import gensim.matutils as matutils
    """
    Compute cosine similarity between two sets of words.

    Example::

      >>> trained_model.n_similarity(['sushi', 'shop'], ['japanese', 'restaurant'])
      0.61540466561049689

      >>> trained_model.n_similarity(['restaurant', 'japanese'], ['japanese', 'restaurant'])
      1.0000000000000004

      >>> trained_model.n_similarity(['sushi'], ['restaurant']) == trained_model.similarity('sushi', 'restaurant')
      True

    """
    v1 = []
    v2 = []
    for word in words1:
        try:
            v1.append(model[word])
        except:
            pass

    for word in words2:
        try:
            v2.append(model[word])
        except:
            pass

    if v1 == []:
        raise Exception, "入力語が全てOOV"
    if v2 == []:
        raise Exception, "入力語が全てOOV"

    # mean(axis=0):縦方向に平均を取る．多分，単語の各次元毎に平均を取る．
    # unitvec     :単位ベクトルのこと．つまり正規化
    # dot         :行列積．
    sim = numpy.dot(matutils.unitvec(numpy.array(v1).mean(axis=0)), matutils.unitvec(numpy.array(v2).mean(axis=0)))
    return sim

