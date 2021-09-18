# -*- coding: utf-8 -*-
import codecs
import os
import re

import jieba
import matplotlib.pyplot as plt
import wordcloud as wc
from matplotlib.font_manager import FontProperties

from IKE.settings import BASE_DIR
from IKEdata.extract_from_CSDN import SummaryTxt

SIMKAI = os.path.join(BASE_DIR, 'static/fonts/simkai.ttf')


def extract(context):
    total_articlelist, x_data = article_to_word(context)
    obj = SummaryTxt(os.path.join(BASE_DIR, 'IKEdata/stopwords-master/hit_stopwords.txt'))
    obj.summaryScoredtxt(context)
    extract_text = obj.summaryTopNtxt(context)
    # freq(total_articlelist)
    keywords = freq(total_articlelist)
    return extract_text, keywords


# 文本处理
def remove_stopwords(words, path):
    # stopwords = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
    # with open(path, 'r', encoding="utf-8") as f:  # 读取停用词
    #     stopwords = f.read().split("\n")
    # print(stopwords)
    stopwords = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
    filtered_words = []
    for word in words:
        if word not in stopwords:
            filtered_words.append(word)
    return filtered_words


# 以文章为单位的分词
def article_to_word(article):
    # 对句子替换标点
    article = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+", ",", article)  # 替换标点符号

    # 分词
    jieba.add_word('新冠', tag='n')
    words = jieba.lcut(article)
    sentence_word_list = remove_stopwords(words,
                                          os.path.join(BASE_DIR, 'IKEdata/stopwords-master/hit_stopwords.txt'))  # 去停用词
    total_wordlist = []
    total_wordlist.append(" ".join(sentence_word_list))
    if len(total_wordlist[0]) == 0:
        sentence_word_list, total_wordlist = ['_'], ['_']
    return sentence_word_list, total_wordlist


def freq(words_list):
    # 词频统计
    dic = {}
    for word in words_list:
        if word not in dic:
            dic[word] = 1
        else:
            dic[word] = dic[word] + 1
    freq = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    # 频率柱状图（频率大于5）
    plt.figure()
    data = freq
    del_data = []
    for i in data:
        if i[1] <= 0:
            del_data.append(i)
    for i in del_data:
        data.remove(i)

    def takeSecond(elem):
        return elem[1]

    data.sort(key=takeSecond, reverse=True)
    data = data[0:8]

    x_index = range(len(data))
    x_data = [i[0] for i in data]
    y_data = [i[1] for i in data]
    plt.bar(x_index, y_data, width=0.35, color='b', tick_label=x_data)
    myfont = FontProperties(fname=SIMKAI)
    plt.xticks(fontproperties=myfont)
    plt.rcParams['axes.unicode_minus'] = False
    # gcf: Get Current Figure
    fig = plt.gcf()
    # plt.show()
    # fig.savefig('../statics/images/plt.png', dpi=100)
    fig.savefig(os.path.join(BASE_DIR, 'static/images/plt.png'), dpi=100)

    # Wordcloud
    all_word = ' '
    for i in words_list:
        all_word = all_word + i + ' '

    # # 判断是已有图片
    # filename = ''
    # for root, dirs, files in os.walk('D:/Python/Project/IKE/static/images/'):
    #     for file in files:
    #         if os.path.splitext(file)[0] == 'wcimage':
    #             filename = os.path.join(root, file)
    # mask = np.array(Image.open(filename))

    # 生成词云对象，设置参数
    cloud = wc.WordCloud(font_path=SIMKAI,  # 中文处理，用系统自带的字体
                         background_color="black",  # 背景颜色
                         max_words=100,  # 词云显示的最大词数
                         # mask=color_mask,#设置背景图片
                         max_font_size=100,  # 字体最大值
                         # mask = mask,   # 使用已有图片
                         random_state=42)
    # 绘制词云图
    mywc = cloud.generate(all_word)
    # mywc.to_file('../statics/images/wordcloud.png')
    # Without filename, paddle method is called and updated pic can't be got
    mywc.to_file(filename=os.path.join(BASE_DIR, 'static/images/wordcloud.png'))

    return data
