from django.db.models import query
from requests.api import get
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # これを書かないとJWTtoken必要
from . import serializers
from .models import Profile,Study

import twitter
import os
import datetime

from django.http import HttpResponse, response

from rest_framework import views


import pandas as pd
import matplotlib.pyplot as plt
import io

# Create your views here.


# user作成
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


# profile作成
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # def get_queryset(self):
    #     # 上位10件のランキング
    #     return Profile.objects.order_by('-point')[:10]

    def perform_create(self, serializer):
        # 現在ログインしているuserとの紐づけ
        serializer.save(userProfile=self.request.user)


# loginしているuserのprofile情報
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)



# 勉強時間の記録
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = serializers.StudySerializer

    def perform_create(self, serializer):
        serializer.save(userStudy=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(userStudy=self.request.user)


# ツイートから勉強時間収集
class GetTweetViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = serializers.StudySerializer

    def get_queryset(self):
        twitter(self.request.user)
        return self.queryset.filter(userStudy=self.request.user)



class GraphCreateAPIView(views.APIView):
    def get(self, request):
        response = get_svg(self.request.user)
        return response


class MostLangAPIView(views.APIView):
    def get(self, request):
        queryset = Study.objects.all().filter(userStudy=self.request.user).order_by('-created_on')
        
        try:
            df_group = studies_groupby(queryset,g_key='language').sort_values(by='study_time')[::-1]
            most_lang =  df_group.index[0]
            response = HttpResponse(most_lang)
        except:
            response = HttpResponse('')
        return response




#pytho-twitternのAPI認証
t = twitter.Api(
                  consumer_key = os.environ.get('CONSUMER_KEY'),
                  consumer_secret = os.environ.get('CONSUMER_SECRET'),
                  access_token_key = os.environ.get('ACCESS_TOKEN_KEY'),
                  access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
                  )

                  
languages = [
      'Python','HTML','CSS','JavaScript','Ruby','Java','Swift','TypeScript',
      'PHP','Kotlin','C#','Go','その他'
    ]


# Tweetからlanguage,study_time,commentを取得する関数
def get_study(string):
    lang = 'その他'
    for language in languages[:-1]:
        if language.lower() in string.lower():
            lang=language
            break

    h1,h10='',''

    try :hour_idx = string.index('時間');h1 = int(string[hour_idx-1])
    except:pass

    try:hour_idx = string.index('時間');h10 = int(string[hour_idx-2])
    except:pass

    hour = f'{h10}{h1}'
    
    return lang,hour,string[:-9]



# twitterの時間を変換する関数
def date_conv(str):
    # strはSun Aug 02 13:13:05 +0000 2020という形式
    year, month, date = str[26:30], str[4:7], str[8:10]
    tdatetime = datetime.datetime.strptime(year + month + date, '%Y%b%d')
    # 日本時間へ変換datetime.timedelta(hours=9)
    tdatetime_jp = tdatetime 
    tdate_jp = datetime.date(tdatetime_jp.year, tdatetime_jp.month, tdatetime_jp.day)

    return tdate_jp


# 過去一週間のデータをTwitterから集める関数
def get_data(name,studies_set):
    end = datetime.date.today() + datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=8)
    tweet_list = t.GetSearch(term='#エンジニアツリー from:' + name + ' since:' + str(start) + ' until:' + str(end) + '_JST')

    date_list,study_list = [],[]

    for s in tweet_list:
        lang,hour,comment = get_study(s.text)
        date = date_conv(s.created_at)

        if (str(date)+str(lang)) in studies_set:continue

        study_list.append((lang,hour,comment))
        date_list.append(date)


    return date_list,study_list



#Twitterボタンの動作
def twitter(user):

    profile = Profile.objects.get(userProfile=user)

    #重複取り除くため
    studies_set = set()
    for s in Study.objects.filter(userStudy=user):
        studies_set.add(str(s.created_on)[:10]+str(s.language))

    twitter_name = profile.twitter_name

    

    if twitter_name != None:
        date_list,study_list = get_data(twitter_name,studies_set)

        for date,(language,study_time,comment) in zip(date_list,study_list):
            if study_time=='':continue
            temp_study = Study(
                userStudy=user,
                created_on=date,
                study_time=study_time,
                language=language,
                comment=comment
                )
            temp_study.save()



# データ集計
def studies_groupby(studies,g_key):
    col = ['language','study_time','comment','created_on']
    df = pd.DataFrame(columns=col)

    for s in studies:
        df = df.append(
            {
            'language':s.language,
            'study_time':int(s.study_time),
            'comment':s.comment,
            'created_on':str(s.created_on)[:10],
            'user':s.userStudy
            }
            ,ignore_index=True)

    df_group = df[[g_key,'study_time']].groupby([g_key]).sum()

    return df_group


#グラフの描画
def setPlt(user):

    studies = Study.objects.filter(userStudy=user).order_by('-created_on')
    df_group = studies_groupby(studies=studies,g_key='created_on')

    plt.bar(df_group.index, df_group['study_time'], color='#A5CDE8')
    plt.title(r"$\bf{ Study Report }$", color='#5fa8da')
    plt.xlabel('date')
    plt.ylabel("time")


# svgへの変換
def pltToSvg():
    buf = io.BytesIO() # メモリ上でバイナリデータを扱う
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

# #グラフ描画のメイン動作
def get_svg(user):
    try:
        setPlt(user)
        svg = pltToSvg()
        plt.cla()
        response = HttpResponse(svg, content_type='image/svg+xml')
    except:
        response = HttpResponse('', content_type='image/svg+xml')

    return response

    
    