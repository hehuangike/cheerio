import datetime
import json
import os

import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from IKE.settings import BASE_DIR
from IKEdata import asset_handler
from IKEdata import models
from . import extract2


def index(request):
    return render(request, 'DataAnalysis/data_analysis_test.html', None)


def loginto(request):
    """
    登录
    :param request: username(str), password(str)
    :return: tips
    """
    una = request.POST.get('username', None)
    pwd = request.POST.get('password', None)
    if una and pwd:
        if User.objects.filter(username=una):
            user = authenticate(username=una, password=pwd)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('IKEdata:dashboard')
                else:
                    tips = '账号未激活,请联系管理员'
            else:
                tips = '用户名或密码错误'
        else:
            tips = '用户不存在'
    else:
        tips = '您需要填写用户名和密码才能登录'
    return render(request, 'base.html', {'tips': tips, 'una': una})


def sign_out(request):
    logout(request)
    tips = '您已退出登录'
    return render(request, 'base.html', {'tips': tips})


def dashboard(request):
    total_no = models.collect.objects.count()
    if total_no == 0:
        df = pd.read_excel(os.path.join(BASE_DIR, 'IKEdata/京东商品评论.xlsx'), sheet_name='Sheet1')
        print(len(df.index.values), 123)
        for j in range(len(df.index.values)):
            i = j + 1
            content = df.iloc[i, 3]
            arthur = df.iloc[i, 0]
            time_string = df.iloc[i, 4]
            time = pd.to_datetime(time_string)
            link = df.iloc[i, 10]

            models.collect.objects.create(
                source='JD',
                content=content,
                arthur=arthur,
                time=time,
                link=link,
            )
    jd_no = models.collect.objects.filter(source='JD').count()
    test_no = models.collect.objects.filter(source='TEST').count()
    other_no = models.collect.objects.filter(source='OTHER').count()
    total_no = models.collect.objects.count()
    jd_data = round(jd_no / total_no * 100)
    test_data = round(test_no / total_no * 100)
    other_data = round(other_no / total_no * 100)
    positive_no = jd_no * 0.99
    negative_no = jd_no * 0.01
    #     Input one page for text analysis
    return render(request, 'Container/dashboard.html', locals())


def result(request):
    context = request.POST['context']
    extract_text = ''
    if context:
        extract_text = extract2.extract(context)
        models.collect.objects.create(
            source='TEST',
            content=context.replace('\r', '').replace('\n', ''),
            arthur='',
            time=datetime.datetime.now(),
            link='',
        )
    #     Input one page for text analysis
    return render(request, 'DataAnalysis/data_result.html', {"context": context, "extract_text": extract_text})


def collect(request):
    """
    数据分析测试
    :param request:
    :return:
    """
    #   Display all comments: Source, Content, Time, link
    all_data = models.collect.objects.all()
    # current_page = request.GET.get('p', 1)
    # paginator = Paginator(all_data, 100)
    # try:
    #     page_obj = paginator.page(current_page)
    # except EmptyPage as e:
    #     page_obj = paginator.page(1)
    # except PageNotAnInteger as not_int_err:
    #     page_obj = paginator.page(1)
    return render(request, 'DataCollect/data_collect_02.html', {"all_data": all_data})


def clean(request):
    #   DataClean data
    return render(request, 'DataClean/clean.html', locals())


def analysis(request):
    # df = pd.read_excel('D:\Python\Project\IKE\IKEdata\京东商品评论.xlsx', sheet_name='Sheet1')
    # comments = ''
    # for j in range(len(df.index.values)):
    #     i = j + 1
    #     content = df.iloc[i, 3]
    #     comments = comments + content
    #     if i == 999:
    #         exit()
    # extract_text = analyse_text.extract(comments)
    #   Display key words, word cloud, word net, text abstract
    return render(request, 'DataAnalysis/data_analysis.html', locals())


def mining(request):
    #   To be updated
    return render(request, 'DataMining/data_mining.html', locals())


def wordnet(request):
    #   DataClean data
    return render(request, 'IKEdata/wordnet.html', locals())


@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式！')
        # 你的检测代码

        sn = data.get('sn', None)

        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)  # [obj]
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('资产数据已经更新。')
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse('没有资产sn，请检查数据内容！')

    return HttpResponse('200 ok')
