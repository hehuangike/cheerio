# -*- coding: utf-8 -*-
import re
import math
import nltk
import time
import graphviz
import gensim
import keras
import openpyxl
import multiprocessing
from collections import Counter
import jieba
import pandas as pd
import numpy as np
from tqdm import tqdm
import networkx as nx
import logging
import xlrd
import xlwt
import tensorflow
from sklearn.metrics import precision_recall_fscore_support, classification_report
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential,load_model,Model
from keras.layers import Dense, Flatten, Embedding, Dropout, BatchNormalization, concatenate, Input, MaxPool1D
from keras.layers.convolutional import Conv1D,MaxPooling1D
from keras.utils import plot_model
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import wordcloud as wc
from HelloWorld.extract_from_CSDN import SummaryTxt
import codecs
from PIL import Image
import os

from IKE.settings import BASE_DIR


def extract(context):
    total_articlelist, x_data = article_to_word(context)
    # obj = SummaryTxt('stopwords-master\hit_stopwords.txt')
    # obj.summaryScoredtxt(context)
    # extract_text = obj.summaryTopNtxt(context)
    # print(extract_text)
    freq(total_articlelist)

    # return extract_text

#文本处理
def remove_stopwords(words, path):
    # stopwords = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
    # with open(path, 'r', encoding="utf-8") as f:  # 读取停用词
    #     stopwords = f.read().split("\n")
    # print(stopwords)
    stopwords = [line.strip() for line in codecs.open(path, 'r', encoding='utf8').readlines()]
    print(stopwords)
    filtered_words=[]
    for word in words:
        if word not in stopwords:
            filtered_words.append(word)
    return filtered_words

#以文章为单位的分词
def article_to_word(article):
    # 对句子替换标点
    article =re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+", ",", article) # 替换标点符号

    #分词
    jieba.add_word('新冠', tag='n')
    jieba.add_word('百草枯', tag='n')
    words = jieba.lcut(article)
    sentence_word_list = remove_stopwords(words, stopwordsfile)  # 去停用词
    total_wordlist = []
    total_wordlist.append(" ".join(sentence_word_list))
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
    print(freq)  # 频数结果

    # 频率柱状图（频率大于5）
    plt.figure()
    data = freq
    del_data = []
    for i in data:
        if i[1] <= 5:
            del_data.append(i)
    for i in del_data:
        data.remove(i)
    x_index = range(len(data))
    x_data = [i[0] for i in data]
    y_data = [i[1] for i in data]
    rects1 = plt.bar(x_index, y_data, width=0.35, color='b', tick_label=x_data)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # gcf: Get Current Figure
    fig = plt.gcf()
    # plt.show()
    # fig.savefig('../statics/images/plt.png', dpi=100)
    fig.savefig(pltfile, dpi=100)

    # Wordcloud
    all_word = ' '
    for i in words_list:
        all_word = all_word + i + ' '

    # 判断是已有图片
    filename = ''
    # for root, dirs, files in os.walk('C:/Tools/Anaconda3/Lib/site-packages/django/bin/HelloWorld/statics/images/'):
    #     for file in files:
    #         if os.path.splitext(file)[0] == 'wcimage':
    #             filename = os.path.join(root, file)
    # mask = np.array(Image.open(filename))

    # 生成词云对象，设置参数
    cloud = wc.WordCloud(font_path=os.path.join(BASE_DIR, 'static/fonts/simkai.ttf'),  # 中文处理，用系统自带的字体
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
    mywc.to_file(filename = wcfile)

# Get context from file
import csv
content = ''
csvfile = 'C:/Users/ss/Downloads/萝卜爬.csv'
wcfile = 'C:/Tools/Anaconda3/Lib/site-packages/django/bin/HelloWorld/statics/images/wordcloud2.png'
stopwordsfile = 'C:/Users/ss/Desktop/backup/Caixin/HelloWorld/stopwords-master/hit_stopwords.txt'
pltfile = 'C:/Tools/Anaconda3/Lib/site-packages/django/bin/HelloWorld/statics/images/plt.png'

with open(csvfile,'rb','gbk') as myFile:
    lines=csv.reader(myFile)
    for line in lines:
        content += line

# content = '新冠肺炎疫情冲击，叠加自2018年9月以来的减税降费，地方财政捉襟见肘。土地出让金的重要性凸显，政府性基金收入大增。南方站记者，关注时政、法治、民生领域2020年广东全省政府性基金预算收入为8642.42亿元，增长41.4%。1月24日，广东省财政厅厅长戴运龙在该省十三届人大四次会议上作报告，披露上述数据。“主要是国有土地使用权出让收入增加。”戴运龙说。据财新记者了解，官方初步统计，2020年广东省内国有土地使用权出让收入超过7900亿元，占全省政府性基金预算收入的90%以上。这较2020年初的预算有了大幅增长。一年前，戴运龙在广东省十三届人大三次会议上报告称，2020年全省政府性基金预算收入为6112亿元，其中国有土地使用权出让收入为5562亿元。但新冠疫情冲击了上述预算目标。广东省财政厅官方网站显示，因财政收入不达预期，但财政支出不断增长，在2020年，该省先后三次调整当年各项预算。报告显示，在2020年，广东全省政府性基金支出9572.77亿元，同比大增52.2%。“主要是中央下达新增专项债券和抗疫特别国债资金形成支出。”报告称，全省政府性基金预算实现收支平衡。“千方百计保市场主体保就业，切实稳住经济基本盘。”广东省省长马兴瑞在政府工作报告中称，2020年，广东落实国家规模性的助企纾困政策，能减则减、能免则免、能优惠则优惠，为各类市场主体再度减税降费3000亿元，其中减免延缓社会保险费这一项，就达到2100亿元。在2019年，广东减税降费的规模为3400亿元。“实体经济和生产性服务业获益最大，小微企业税费降幅明显。”戴运龙说。报告显示，在2020年，广东全省一般公共预算收入为12921.97亿元，增长2.1%。其中税收收入为9881.21亿元，同比减少1.8%。主体税种（增值税、企业所得税和个人所得税）同比减少3.5%。土地出让金成为了地方财政的有力补充。在2020年，广东省的土地出让金相当于全省税收收入的80%。在2019年，这一比例大约为55%。这一现象并非广东独有。整个2020年，全国多个城市供地规模明显“超标”。华创证券发布于2019年9月的研报指出，“在财政困难年份，土地出让金往往会增加。”在过去三次财政困难年份，即2009年、2012年和2015年之后的第二年，土地成交款都出现了明显上升。（详见财新网报道《楼市观察|广州土地出让金创历史新高 一线城市卖地收入大增》）财政部数据显示，2020年1月至11月，全国政府性基金预算收入为7.27万亿元，同比增长6.7%；其中国有土地使用权出让收入为6.51万亿元，同比增长12.9%。此前房地产业内普遍预期，2021年各地土地出让规模或将有所缩减。但广东省的预算报告显示，预计2021年广东省的国有土地使用权出让收入为7910.76亿元，与2020年持平。这意味着，广东或将在2021年持续大规模供地。2021年的预算草案显示，全省一般公共预算入不敷出的现象还将延续，预计2021年全省一般公共预算收入为13562.22亿元，增长5%；但一般公共预算支出为17834.37亿元，增长2%。广东能否继续大规模卖地，还有待人大批准。'

content = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；：:-【】+\"\']+|[+——！，;：:。？、~@#￥%……&*（）]+", "", content)  # 去标点符号
summary = extract(content)
print(summary)


# context = '新冠肺炎疫情冲击，叠加自2018年9月以来的减税降费，地方财政捉襟见肘。土地出让金的重要性凸显，政府性基金收入大增。南方站记者，关注时政、法治、民生领域2020年广东全省政府性基金预算收入为8642.42亿元，增长41.4%。1月24日，广东省财政厅厅长戴运龙在该省十三届人大四次会议上作报告，披露上述数据。“主要是国有土地使用权出让收入增加。”戴运龙说。据财新记者了解，官方初步统计，2020年广东省内国有土地使用权出让收入超过7900亿元，占全省政府性基金预算收入的90%以上。这较2020年初的预算有了大幅增长。一年前，戴运龙在广东省十三届人大三次会议上报告称，2020年全省政府性基金预算收入为6112亿元，其中国有土地使用权出让收入为5562亿元。但新冠疫情冲击了上述预算目标。广东省财政厅官方网站显示，因财政收入不达预期，但财政支出不断增长，在2020年，该省先后三次调整当年各项预算。报告显示，在2020年，广东全省政府性基金支出9572.77亿元，同比大增52.2%。“主要是中央下达新增专项债券和抗疫特别国债资金形成支出。”报告称，全省政府性基金预算实现收支平衡。“千方百计保市场主体保就业，切实稳住经济基本盘。”广东省省长马兴瑞在政府工作报告中称，2020年，广东落实国家规模性的助企纾困政策，能减则减、能免则免、能优惠则优惠，为各类市场主体再度减税降费3000亿元，其中减免延缓社会保险费这一项，就达到2100亿元。在2019年，广东减税降费的规模为3400亿元。“实体经济和生产性服务业获益最大，小微企业税费降幅明显。”戴运龙说。报告显示，在2020年，广东全省一般公共预算收入为12921.97亿元，增长2.1%。其中税收收入为9881.21亿元，同比减少1.8%。主体税种（增值税、企业所得税和个人所得税）同比减少3.5%。土地出让金成为了地方财政的有力补充。在2020年，广东省的土地出让金相当于全省税收收入的80%。在2019年，这一比例大约为55%。这一现象并非广东独有。整个2020年，全国多个城市供地规模明显“超标”。华创证券发布于2019年9月的研报指出，“在财政困难年份，土地出让金往往会增加。”在过去三次财政困难年份，即2009年、2012年和2015年之后的第二年，土地成交款都出现了明显上升。（详见财新网报道《楼市观察|广州土地出让金创历史新高 一线城市卖地收入大增》）财政部数据显示，2020年1月至11月，全国政府性基金预算收入为7.27万亿元，同比增长6.7%；其中国有土地使用权出让收入为6.51万亿元，同比增长12.9%。此前房地产业内普遍预期，2021年各地土地出让规模或将有所缩减。但广东省的预算报告显示，预计2021年广东省的国有土地使用权出让收入为7910.76亿元，与2020年持平。这意味着，广东或将在2021年持续大规模供地。2021年的预算草案显示，全省一般公共预算入不敷出的现象还将延续，预计2021年全省一般公共预算收入为13562.22亿元，增长5%；但一般公共预算支出为17834.37亿元，增长2%。广东能否继续大规模卖地，还有待人大批准。'
# context = '十八大以来的五年，是党和国家发展进程中极不平凡的五年。面对世界经济复苏乏力、局部冲突和动荡频发、全球性问题加剧的外部环境，面对我国经济发展进入新常态等一系列深刻变化，我们坚持稳中求进工作总基调，迎难而上，开拓进取，取得了改革开放和社会主义现代化建设的历史性成就。' '为贯彻十八大精神，党中央召开七次全会，分别就政府机构改革和职能转变、全面深化改革、全面推进依法治国、制定“十三五”规划、全面从严治党等重大问题作出决定和部署。五年来，我们统筹推进“五位一体”总体布局、协调推进“四个全面”战略布局，“十二五”规划胜利完成，“十三五”规划顺利实施，党和国家事业全面开创新局面。''经济建设取得重大成就。坚定不移贯彻新发展理念，坚决端正发展观念、转变发展方式，发展质量和效益不断提升。经济保持中高速增长，在世界主要国家中名列前茅，国内生产总值从五十四万亿元增长到八十万亿元，稳居世界第二，对世界经济增长贡献率超过百分之三十。供给侧结构性改革深入推进，经济结构不断优化，数字经济等新兴产业蓬勃发展，高铁、公路、桥梁、港口、机场等基础设施建设快速推进。农业现代化稳步推进，粮食生产能力达到一万二千亿斤。城镇化率年均提高一点二个百分点，八千多万农业转移人口成为城镇居民。区域发展协调性增强，“一带一路”建设、京津冀协同发展、长江经济带发展成效显著。创新驱动发展战略大力实施，创新型国家建设成果丰硕，天宫、蛟龙、天眼、悟空、墨子、大飞机等重大科技成果相继问世。南海岛礁建设积极推进。开放型经济新体制逐步健全，对外贸易、对外投资、外汇储备稳居世界前列。''全面深化改革取得重大突破。蹄疾步稳推进全面深化改革，坚决破除各方面体制机制弊端。改革全面发力、多点突破、纵深推进，着力增强改革系统性、整体性、协同性，压茬拓展改革广度和深度，推出一千五百多项改革举措，重要领域和关键环节改革取得突破性进展，主要领域改革主体框架基本确立。中国特色社会主义制度更加完善，国家治理体系和治理能力现代化水平明显提高，全社会发展活力和创新活力明显增强。'
# context = '市场煤价持续走高，主流煤炭价格指数全部停发。12月30日，中国煤炭运销协会、中国电力企业联合会（下称中电联）先后宣布，将从当日暂停发布各自编制的CCTD环渤海动力煤现货参考价、CECI指数，恢复时间待定。加上此前停发的两个指数，可供市场参考的主流港口动力煤指数全部停发。主流指数全线停发的现象系首次出现，两名长期关注煤炭行情的分析人士告诉记者，这一罕见现象的背后是今冬煤价飚涨。停发之前的12月29日，CCTD环渤海5500K动力煤现货参考价、CECI5500各报706元/吨、751元/吨，月内涨幅超过10%，这一水平不仅再度刷新年内新高，也是两指数自发布以来的最高点。此前12月3日，汾渭能源下属汾渭数字信息技术有限公司发布的CCI现货日度指数，以及另一家煤炭资讯机构易煤网发布的日度、周度的易煤北方港价格指数、长江口价格指数先行停发。（详见财新网“动力煤现货价格突破640元 两机构停发价格指数”）中国煤炭运销协会下属的中国煤炭市场网公告称，近期动力煤市场持续出现剧烈异常波动，本着对市场负责的态度暂停发布指数；中国电力企业联合会对数据停发的解释是“电煤市场现货价格大幅上涨，定价体系混乱，部分样本已不具代表性”。中国电力企业联合会、中国煤炭市场网分别从2017年11月、2018年8月起发布上述指数。此轮价格高涨系供需偏紧所致。供给方面，受倒查煤炭领域违法违规行动影响，主产区内蒙古严格控制超产，年内产量下滑；叠加进口煤受限，北方港口库存处于历史低位。需求方面，宏观经济复苏，加之气温偏低，今冬电煤需求高于去年同期。煤炭价格指数在现货价格基础上编制，反映供需走势；同时也作为交易主体的定价参考，对实际成交价格产生影响。一旦停发，意味着市场主体判断供需形势的难度加大。因此，停发指数也被业内人士视作相关部门的一种价格调控手段。为了稳价保供，国家发改委12月以来还出台了包括主产区增产、适度放开进口在内的系列调控举措。（详见财新网“内蒙古煤炭日产量同比增7% 应对冬季保供”）但由于供需矛盾仍未得到实质性缓解，在多重调控手段出台的12月，动力煤现货价格仍持续走高。近期个别电厂库存告急，直接反映供给态势严峻。据河南安阳发改委官网12月24日披露，该市两个热电厂的电煤库存分别为5天、10天，严重低于“可用15天以上”的警戒水平，导致电煤告急的原因之一即煤源紧张。对于当前的电煤供需态势，中电联12月28日刊文分析称，尽管国家层面高度重视电煤保供，但临近年底，产地增产难度较大，产地和北港库存偏低、累库困难，优质低硫品种紧缺，迎峰度冬前期电煤保障压力仍然很大。'
# summary = extract(context)
# print(summary)
