# # -*- coding: utf-8 -*-
# import re
# import math
# import nltk
# import time
# import graphviz
# import gensim
# import keras
# import openpyxl
# import multiprocessing
# from collections import Counter
# import jieba
# import pandas as pd
# import numpy as np
# from tqdm import tqdm
# import networkx as nx
# import logging
# import xlrd
# import xlwt
# import tensorflow
# from sklearn.metrics import precision_recall_fscore_support, classification_report
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
# from sklearn.linear_model import LogisticRegressionCV
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import train_test_split
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.models import Sequential,load_model,Model
# from keras.layers import Dense, Flatten, Embedding, Dropout, BatchNormalization, concatenate, Input, MaxPool1D
# from keras.layers.convolutional import Conv1D,MaxPooling1D
# from keras.utils import plot_model
# from sklearn.metrics import accuracy_score
# import matplotlib.pyplot as plt
# import wordcloud as wc
# from IKEdata.extract_from_CSDN import SummaryTxt
# import codecs
# from PIL import Image
# import os
#
#
# def extract(context):
#     total_articlelist, x_data = article_to_word(context)
#     obj = SummaryTxt('D:\Python\Project\IKE\IKEdata\stopwords-master\hit_stopwords.txt')
#     obj.summaryScoredtxt(context)
#     extract_text = obj.summaryTopNtxt(context)
#     print(extract_text)
#     freq(total_articlelist)
#
#     return extract_text
#
# #文本处理
# def remove_stopwords(words, path):
#     # stopwords = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
#     # with open(path, 'r', encoding="utf-8") as f:  # 读取停用词
#     #     stopwords = f.read().split("\n")
#     # print(stopwords)
#     stopwords = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
#     print(stopwords)
#     filtered_words=[]
#     for word in words:
#         if word not in stopwords:
#             filtered_words.append(word)
#     return filtered_words
#
# #以文章为单位的分词
# def article_to_word(article):
#     # 对句子替换标点
#     article =re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+", ",", article) # 替换标点符号
#
#     #分词
#     jieba.add_word('新冠', tag='n')
#     words = jieba.lcut(article)
#     sentence_word_list = remove_stopwords(words, 'D:\Python\Project\IKE\IKEdata\stopwords-master\hit_stopwords.txt')  # 去停用词
#     total_wordlist = []
#     total_wordlist.append(" ".join(sentence_word_list))
#     return sentence_word_list, total_wordlist
#
# def freq(words_list):
#     # 词频统计
#     dic = {}
#     for word in words_list:
#         if word not in dic:
#             dic[word] = 1
#         else:
#             dic[word] = dic[word] + 1
#     freq = sorted(dic.items(), key=lambda x: x[1], reverse=True)
#     print(freq)  # 频数结果
#
#     # 频率柱状图（频率大于5）
#     plt.figure()
#     data = freq
#     del_data = []
#     for i in data:
#         if i[1] <= 5:
#             del_data.append(i)
#     for i in del_data:
#         data.remove(i)
#     x_index = range(len(data))
#     x_data = [i[0] for i in data]
#     y_data = [i[1] for i in data]
#     rects1 = plt.bar(x_index, y_data, width=0.35, color='b', tick_label=x_data)
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     plt.rcParams['axes.unicode_minus'] = False
#     # gcf: Get Current Figure
#     fig = plt.gcf()
#     # plt.show()
#     # fig.savefig('../statics/images/plt.png', dpi=100)
#     fig.savefig('D:\Python\Project\IKE\static\images\plt2.png', dpi=100)
#
#     # Wordcloud
#     all_word = ' '
#     for i in words_list:
#         all_word = all_word + i + ' '
#
#     # # 判断是已有图片
#     # filename = ''
#     # for root, dirs, files in os.walk('D:/Python/Project/IKE/static/images/'):
#     #     for file in files:
#     #         if os.path.splitext(file)[0] == 'wcimage':
#     #             filename = os.path.join(root, file)
#     # mask = np.array(Image.open(filename))
#
#     # 生成词云对象，设置参数
#     cloud = wc.WordCloud(font_path='C:/Windows/Fonts/simkai.ttf',  # 中文处理，用系统自带的字体
#                          background_color="black",  # 背景颜色
#                          max_words=100,  # 词云显示的最大词数
#                          # mask=color_mask,#设置背景图片
#                          max_font_size=100,  # 字体最大值
#                          # mask = mask,   # 使用已有图片
#                          random_state=42)
#     # 绘制词云图
#     mywc = cloud.generate(all_word)
#     # mywc.to_file('../statics/images/wordcloud.png')
#     # Without filename, paddle method is called and updated pic can't be got
#     mywc.to_file(filename = 'D:/Python/Project/IKE/static/images/wordcloud2.png')
#
# df = pd.read_excel('D:\Python\Project\IKE\IKEdata\京东商品评论.xlsx', sheet_name='Sheet1')
# comments = ''
# for j in range(len(df.index.values)):
#     i = j + 1
#     content = df.iloc[i, 3]
#     comments = comments + content
#     if i == 999:
#         exit()
#
