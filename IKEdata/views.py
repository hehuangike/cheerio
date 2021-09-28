import datetime
import json
import os

import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from IKE.settings import BASE_DIR
from IKEdata import asset_handler
from IKEdata import models
from . import extract2


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
        tips = '请输入正确的账号和密码'
    return render(request, 'base.html', {'tips': tips, 'una': una})


def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
        tips = '您已退出登录'
    else:
        return redirect('IKEdata:home')
    return render(request, 'base.html', {'tips': tips})


def dashboard(request):
    total_no = models.collect.objects.count()
    if total_no == 0:
        df = pd.read_excel(os.path.join(BASE_DIR, 'IKEdata/京东商品评论.xlsx'), sheet_name='Sheet1')
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
    current = 'dashboard'
    #     Input one page for text analysis
    return render(request, 'Container/Dashboard/index.html', locals())


def analysis_test(request):
    context = request.POST.get('context', None)
    extract_text = ''
    analysis_result = False
    current = 'analysis_test'
    if context:
        extract_text, keywords = extract2.extract(context)
        models.collect.objects.create(
            source='TEST',
            content=context.replace('\r', '').replace('\n', ''),
            arthur='',
            time=datetime.datetime.now(),
            link='',
        )
        analysis_result = True
        current = 'analysis_result'
    return render(
        request, 'Container/Analysis/analysisTest.html',
        {
            "context": context,
            "extract_text": extract_text,
            'analysis_result': analysis_result,
            'current': current,
        }
    )


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
    return render(request, 'Container/Collect/index.html', {"all_data": all_data, "current": "collect"})


def clean(request):
    #   DataClean data
    return render(request, 'Container/Clean/index.html', {"current": "clean"})


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
    
    context = "用了以后再追评一直用这个机油给车子保养，非常不错，相信京东自营。不错，美孚一号大牌子，京东自营值得信赖，爱车非常适用，已经用好多次京东买了，顺便购买了更换机油服务，一步到位，发动机很安静，油耗也降低了一点点，谁用谁知道，希望多搞点活动。一直用的银美孚一号 价格合适 自己保养车更放心 物流很快 一直信赖京东自营的东西选机油，先选SN级的，这是最高级，SL级是低配款，0W-30的意思是机油适用零度，流动性30的。家中常备机油，便宜就先囤一个，一直用这个牌子推荐这家店铺非常不错哦第一次在京东平台上购买美孚一号，之前一直在市场上买，效果特别好，希望京东平台上的美孚保真保质，如果用的好，以后还会接着在京东上购买京东平台优惠力度大，值得推荐，大家快来抢购，以后还会在京东上购买，希望以后赠送礼品多点首先，金美孚一号这款油，一直用这个牌子，质量非常好，其次，京东自营下单，配送时效特别快，晚上下单第二天早上9点就收到了，省去了去实体店的苦恼，而且价格也非常优惠，有优惠券可以领，这款油保养周期长，相信京东自营商城，物流很快，拿去店里换的，维修师傅说有不错，换完车的噪声小了很多，还在在买的发动机是汽车的心脏，润滑油的好坏对车辆的健康与否密切相关。好评一直从京东购买这款美孚一号机油，每次一万公里保养一次。"
    return render(request, 'Container/Analysis/analysis.html', {"context": context, "current": "analysis"})


def mining(request):
    #   To be updated
    return render(request, 'Container/Mining/index.html', {"current": "mining"})


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
