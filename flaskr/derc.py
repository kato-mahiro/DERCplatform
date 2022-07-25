#ssやGASなどはこちらのリンクから持ってきてください。https://drive.google.com/drive/folders/1zCVqcMWUY0W2wT9kEX5VcTyeV3cTgOsD?usp=sharing

from typing import Awaitable
import gspread
import json
import subprocess
import datetime
import schedule
import time
from slack_sdk import WebClient
from flask import Flask, flash, render_template, request, session, redirect, send_file, g
import numpy as np
from threading import Thread
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String#以下4文SQLAlchemyのためのimport
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


###################スプレッドシート操作
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('***.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
#DB用
SPREADSHEET_KEY_DB = '***'
#EventAPIでslackのログを保存しているスプレッドシート
SPREADSHEET_KEY_slacklog_EventAPI = '***'
#共有設定したスプレッドシートを指定
#DB用
workbook_DB = gc.open_by_key(SPREADSHEET_KEY_DB)
#EventAPIでslackのログを保存しているスプレッドシート
workbook_slacklog_EventAPI = gc.open_by_key(SPREADSHEET_KEY_slacklog_EventAPI)
#ユーザー名からslackのアカウントIDを取ってくるためのシート
userIDchange = workbook_slacklog_EventAPI.worksheet('userIDchange')
#スプレッドシートの中のワークシート名を直接指定
worksheet1 = workbook_DB.worksheet('ポイント管理')
worksheet2 = workbook_DB.worksheet('チャンネル関連')
pointrireki = workbook_DB.worksheet('ポイント履歴')


#ビデオ会議関連のスプレッドシート
SPREADSHEET_webdiscuss = '設定してください'
workbook_webdiscuss = gc.open_by_key(SPREADSHEET_webdiscuss)
webchan = workbook_webdiscuss.worksheet('会議チャンネル関連')


#歩数計算のワークシート
SPREADSHEET_hosuukeisana = '設定してください'
SPREADSHEET_hosuukeisan = gc.open_by_key(SPREADSHEET_hosuukeisana)
hosuukeisan = SPREADSHEET_hosuukeisan.worksheet('歩数')


#日常生活のワークシート
SPREADSHEET_rita = '設定してください'
SPREADSHEET_rita = gc.open_by_key(SPREADSHEET_rita)
ritasheet = SPREADSHEET_rita.worksheet('利他行為')

###################スプレッドシート操作終わり

app = Flask(__name__)
app.secret_key = b'random string...'
engine = create_engine('sqlite:///derc.db',
connect_args={'check_same_thread': False}
)#SQLAlchemyのため
Base = declarative_base()#SQLAlchemyのため

all_user =["shimamoto","komori","shimaoka","hiramoto","asakura","banno","morinaga","sumitani","iwata","yamato","test"]
all_user_pswd=["lucas","afro","dark","gene","hero","riot","poruka","takemi","boss","tutida","aaa"]
all_user_ID =  ["slackの個人ID","slackの個人ID","X","","","","","","","",""]
chan_IDlist = ["slackのチャンネルID","slackのチャンネルID","","",""]

member_data = {}
message_data = []


# get Database Object.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('derc.db', check_same_thread=False)
    return g.db


# close Dataabse Object.
def close_db(e=None):
    db = g.pop('db', None)


    if db is not None:
        db.close()


#下のDBのバッヂ情報を更新するための関数(def updateBadgeinfo(id))
def updateBadgeinfoDB(badgeinfo,id):    
    # model class
    class updateBadgeinfoclass(Base):
      __tablename__ = 'badgedata'
      __table_args__ = {'extend_existing': True}
      id = Column(Integer, primary_key=True)
      zentai_3000 = Column(Integer)
      zentai_6000 = Column(Integer)
      zentai_10000 = Column(Integer)
      zentai_15000 = Column(Integer)
      zentai_20000 = Column(Integer)
      zentai_30000 = Column(Integer)
      zentai_40000 = Column(Integer)
      zentai_50000 = Column(Integer)
      zentai_60000 = Column(Integer)
      discuss_dou = Column(Integer)
      discuss_gin = Column(Integer)
      discuss_kin = Column(Integer)
      discussLv1_dou = Column(Integer)
      discussLv1_gin = Column(Integer)
      discussLv1_kin = Column(Integer)
      discussLv2_dou = Column(Integer)
      discussLv2_gin = Column(Integer)
      discussLv2_kin = Column(Integer)
      hosuu_dou = Column(Integer)
      hosuu_gin = Column(Integer)
      hosuu_kin = Column(Integer)
      hosuuLv1_dou = Column(Integer)
      hosuuLv1_gin = Column(Integer)
      hosuuLv1_kin = Column(Integer)
      hosuuLv2_dou = Column(Integer)
      hosuuLv2_gin = Column(Integer)
      hosuuLv2_kin = Column(Integer)
      ritakoui_dou = Column(Integer)
      ritakoui_gin = Column(Integer)
      ritakoui_kin = Column(Integer)
      ritakouiLv1_dou = Column(Integer)
      ritakouiLv1_gin = Column(Integer)
      ritakouiLv1_kin = Column(Integer)
      ritakouiLv2_dou = Column(Integer)
      ritakouiLv2_gin = Column(Integer)
      ritakouiLv2_kin = Column(Integer)

    Session = sessionmaker(bind = engine)
    ses = Session()
    mydata = ses.query(updateBadgeinfoclass).filter(updateBadgeinfoclass.id == id).one()
    exec_code = 'mydata.' + badgeinfo + '= 1' 
    exec(exec_code)
    ses.add(mydata)
    ses.commit()
    ses.close()

#バッヂの更新情報をSlackで通知する。
def badgeinfotuuti(user_id):
    #評価を通知するプログラム始まり
    token = "設定してください"#ワークスペース名前
    client = WebClient(token)
    #自分のuserID取ってくる
    user_id = all_user_ID[user_id]#自分のslackのIDを取ってくる。
    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "新しいバッヂをゲットしました！")
    #評価を通知するプログラム終わり

#バッヂの情報を更新してSlackで通知する関数
#上の関数を以下の関数内で読み込んでいるよ。
def updateBadgeinfo(id):
    badgedatatwo = []
    badgedata = []
    db = get_db()
    cur_badge = db.execute("select * from badgedata where id = {id}".format(id = id))
    badgedatatwo = cur_badge.fetchall()
    for ooo in range(50):#DBから取ってきたままだと2次元で扱いにくいため一次元に返還する。
        badgedata.append(badgedatatwo[0][ooo])
    #以下それぞれの獲得ポイントを格納する。
    receivePt_zentai = badgedata[2]
    receivePt_discuss = badgedata[3]
    receivePt_discussLv1 = badgedata[4]
    receivePt_discussLv2 = badgedata[5]
    receivePt_hosuu = badgedata[6]  
    receivePt_hosuuLv1 = badgedata[7]
    receivePt_hosuuLv2 = badgedata[8]
    receivePt_ritakoui = badgedata[9]
    receivePt_ritakouiLv1 = badgedata[10]
    receivePt_ritakouiLv2 = badgedata[11]
    del badgedata[:12]#名前とかidとか各アクティビティで取得したポイントとかの情報を削除する。

    ##バッヂの色は銅はほぼ全員が到達した、銀は半分が到達した、金は3人が到達した。という判定で
    #全体ポイントのバッヂの更新
    if receivePt_zentai >= 3000 and badgedata[0] == 0: 
        updateBadgeinfoDB("zentai_3000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 6000 and badgedata[1] == 0: 
        updateBadgeinfoDB("zentai_6000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 10000 and badgedata[2] == 0: 
        updateBadgeinfoDB("zentai_10000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 15000 and badgedata[3] == 0: 
        updateBadgeinfoDB("zentai_15000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 20000 and badgedata[4] == 0: 
        updateBadgeinfoDB("zentai_20000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 30000 and badgedata[5] == 0: 
        updateBadgeinfoDB("zentai_30000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 40000 and badgedata[6] == 0: 
        updateBadgeinfoDB("zentai_40000",id)
        badgeinfotuuti(id -1)
    
    if receivePt_zentai >= 50000 and badgedata[7] == 0: 
        updateBadgeinfoDB("zentai_50000",id)
        badgeinfotuuti(id -1)

    if receivePt_zentai >= 60000 and badgedata[8] == 0: 
        updateBadgeinfoDB("zentai_60000",id)
        badgeinfotuuti(id -1)

    del badgedata[:9]#全体ポイントのバッヂ情報を消去
    
    #議論全体ポイントのバッヂの更新3000,7000,12000
    if receivePt_discuss >= 3000 and badgedata[0] == 0: 
        updateBadgeinfoDB("discuss_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_discuss >= 7000 and badgedata[1] == 0: 
        updateBadgeinfoDB("discuss_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_discuss >= 12000 and badgedata[2] == 0: 
        updateBadgeinfoDB("discuss_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#議論全体ポイントのバッヂ情報を消去

    #議論Lv1ポイントのバッヂの更新2000,5000,8000
    if receivePt_discussLv1 >= 2000 and badgedata[0] == 0: 
        updateBadgeinfoDB("discussLv1_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_discussLv1 >= 5000 and badgedata[1] == 0: 
        updateBadgeinfoDB("discussLv1_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_discussLv1 >= 10000 and badgedata[2] == 0: 
        updateBadgeinfoDB("discussLv1_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#議論Lv1ポイントのバッヂ情報を消去

    #議論Lv2ポイントのバッヂの更新5000,10000,15000
    if receivePt_discussLv2 >= 6000 and badgedata[0] == 0: 
        updateBadgeinfoDB("discussLv2_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_discussLv2 >= 12000 and badgedata[1] == 0: 
        updateBadgeinfoDB("discussLv2_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_discussLv2 >= 25000 and badgedata[2] == 0: 
        updateBadgeinfoDB("discussLv2_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#議論Lv2ポイントのバッヂ情報を消去

    #歩数全体ポイントのバッヂの更新5000,10000,20000
    if receivePt_hosuu >= 5000 and badgedata[0] == 0: 
        updateBadgeinfoDB("hosuu_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_hosuu >= 10000 and badgedata[1] == 0: 
        updateBadgeinfoDB("hosuu_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_hosuu >= 20000 and badgedata[2] == 0: 
        updateBadgeinfoDB("hosuu_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#歩数全体ポイントのバッヂ情報を消去

    #歩数Lv1ポイントのバッヂの更新5000,15000,25000
    if receivePt_hosuuLv1 >= 5000 and badgedata[0] == 0: 
        updateBadgeinfoDB("hosuuLv1_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_hosuuLv1 >= 15000 and badgedata[1] == 0: 
        updateBadgeinfoDB("hosuuLv1_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_hosuuLv1 >= 25000 and badgedata[2] == 0: 
        updateBadgeinfoDB("hosuuLv1_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#歩数Lv1ポイントのバッヂ情報を消去

    #歩数Lv2ポイントのバッヂの更新3000,7000,10000
    if receivePt_hosuuLv2 >= 3000 and badgedata[0] == 0: 
        updateBadgeinfoDB("hosuuLv2_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_hosuuLv2 >= 7000 and badgedata[1] == 0: 
        updateBadgeinfoDB("hosuuLv2_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_hosuuLv2 >= 10000 and badgedata[2] == 0: 
        updateBadgeinfoDB("hosuuLv2_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#歩数LLv2全体ポイントのバッヂ情報を消去

    #利他行為全体ポイントのバッヂの更新1000,2500,4000
    if receivePt_ritakoui >= 1000 and badgedata[0] == 0: 
        updateBadgeinfoDB("ritakoui_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_ritakoui >= 2500 and badgedata[1] == 0: 
        updateBadgeinfoDB("ritakoui_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_ritakoui >= 4000 and badgedata[2] == 0: 
        updateBadgeinfoDB("ritakoui_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#利他行為全体ポイントのバッヂ情報を消去

    #利他行為Lv1ポイントのバッヂの更新500,1500,3000
    if receivePt_ritakouiLv1 >= 500 and badgedata[0] == 0: 
        updateBadgeinfoDB("ritakouiLv1_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_ritakouiLv1 >= 1500 and badgedata[1] == 0: 
        updateBadgeinfoDB("ritakouiLv1_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_ritakouiLv1 >= 3000 and badgedata[2] == 0: 
        updateBadgeinfoDB("ritakouiLv1_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#利他行為Lv1ポイントのバッヂ情報を消去

    #利他行為Lv2ポイントのバッヂの更新500,1500,3000
    if receivePt_ritakouiLv2 >= 500 and badgedata[0] == 0: 
        updateBadgeinfoDB("ritakouiLv2_dou",id)
        badgeinfotuuti(id -1)
    
    if receivePt_ritakouiLv2 >= 1500 and badgedata[1] == 0: 
        updateBadgeinfoDB("ritakouiLv2_gin",id)
        badgeinfotuuti(id -1)

    if receivePt_ritakouiLv2 >= 3000 and badgedata[2] == 0: 
        updateBadgeinfoDB("ritakouiLv2_kin",id)
        badgeinfotuuti(id -1)

    del badgedata[:3]#利他行為Lv2ポイントのバッヂ情報を消去
    

#バッヂの状態を取得する関数
#ゆくゆくは取得して、ポイントに応じてバッヂの状態も更新する関数にしたい。
def getBadgeinfo(id):
    badgedatatwo = []
    badgedata = []
    db = get_db()
    cur_badge = db.execute("select * from badgedata where id = {id}".format(id = id))
    badgedatatwo = cur_badge.fetchall()
    for ooo in range(50):#DBから取ってきたままだと2次元で扱いにくいため一次元に返還する。
        badgedata.append(badgedatatwo[0][ooo])
    del badgedata[:12]#名前とかidとか各アクティビティで取得したポイントとかの情報を削除する。

    if badgedata[8] =="1":#全体ポイントのバッヂの色判定
        zentai = "60000"
    elif badgedata[7] == 1:
        zentai = "50000"
    elif badgedata[6] == 1:
        zentai = "40000"
    elif badgedata[5] == 1:
        zentai = "30000"
    elif badgedata[4] == 1:
        zentai = "20000"
    elif badgedata[3] == 1:
        zentai = "15000"
    elif badgedata[2] == 1:
        zentai = "10000"
    elif badgedata[1] == 1:
        zentai = "6000"
    elif badgedata[0] == 1:
        zentai = "3000"
    else:
        zentai = "nasi"
    del badgedata[:9]#全体ポイントの情報を削除

    if badgedata[2] ==1:#議論のバッヂの色判定
        discuss = "kin"
    elif badgedata[1] ==1:
        discuss = "gin"
    elif badgedata[0] ==1:
        discuss = "dou"
    else:
        discuss = "nasi"
    del badgedata[:3]#議論の情報を削除

    if badgedata[2] ==1:#議論Lv1のバッヂの色判定
        discussLv1 = "kin"
    elif badgedata[1] ==1:
        discussLv1 = "gin"
    elif badgedata[0] ==1:
        discussLv1 = "dou"
    else:
        discussLv1 = "nasi"
    del badgedata[:3]#議Lv1の情報を削除

    if badgedata[2] ==1:#議論Lv2のバッヂの色判定
        discussLv2 = "kin"
    elif badgedata[1] ==1:
        discussLv2 = "gin"
    elif badgedata[0] ==1:
        discussLv2 = "dou"
    else:
        discussLv2 = "nasi"
    del badgedata[:3]#議論Lv2の情報を削除

    if badgedata[2] ==1:#歩数のバッヂの色判定
        hosuu = "kin"
    elif badgedata[1] ==1:
        hosuu = "gin"
    elif badgedata[0] ==1:
        hosuu = "dou"
    else:
        hosuu = "nasi"
    del badgedata[:3]#歩数の情報を削除

    if badgedata[2] ==1:#歩数Lv1のバッヂの色判定
        hosuuLv1 = "kin"
    elif badgedata[1] ==1:
        hosuuLv1 = "gin"
    elif badgedata[0] ==1:
        hosuuLv1 = "dou"
    else:
        hosuuLv1 = "nasi"
    del badgedata[:3]#歩数Lv1の情報を削除

    if badgedata[2] ==1:#歩数Lv2のバッヂの色判定
        hosuuLv2 = "kin"
    elif badgedata[1] ==1:
        hosuuLv2 = "gin"
    elif badgedata[0] ==1:
        hosuuLv2 = "dou"
    else:
        hosuuLv2 = "nasi"
    del badgedata[:3]#歩数Lv2の情報を削除

    if badgedata[2] ==1:#利他行為のバッヂの色判定
        ritakoui = "kin"
    elif badgedata[1] ==1:
        ritakoui = "gin"
    elif badgedata[0] ==1:
        ritakoui = "dou"
    else:
        ritakoui = "nasi"
    del badgedata[:3]#利他行為の情報を削除

    if badgedata[2] ==1:#利他行為Lv1のバッヂの色判定
        ritakouiLv1 = "kin"
    elif badgedata[1] ==1:
        ritakouiLv1 = "gin"
    elif badgedata[0] ==1:
        ritakouiLv1 = "dou"
    else:
        ritakouiLv1 = "nasi"
    del badgedata[:3]#利他行為Lv1の情報を削除

    if badgedata[2] ==1:#利他行為Lv2のバッヂの色判定
        ritakouiLv2 = "kin"
    elif badgedata[1] ==1:
        ritakouiLv2 = "gin"
    elif badgedata[0] ==1:
        ritakouiLv2 = "dou"
    else:
        ritakouiLv2 = "nasi"
    del badgedata[:3]#利他行為Lv2の情報を削除


    return(zentai,discuss,discussLv1,discussLv2,hosuu,hosuuLv1,hosuuLv2,ritakoui,ritakouiLv1,ritakouiLv2)


###DB扱うコードの例始まり##################################################

# model class（mydata用）
class Mydata(Base):
    __tablename__ = 'mydata'
    __table_args__ = {'extend_existing': True}
 
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mail = Column(String(255))
    tosi = Column(Integer)


    # get Dict data
    def toDict(self):
        return {
            'id':int(self.id), 
            'name':str(self.name), 
            'mail':str(self.mail), 
            'age':int(self.age)
        }


#以下メモ
#GASからDBを操作したいと思ったときに、定期実行の方法がないため次の方法で行う。
#pythonファイルで、ssの情報とDBの情報が違っていれば（ssが更新されていれば）スプレッドシートの情報をDBに書き込む、という関数を1分ごとに起動させる
#一番行いたいこととしては、データの保存方法をスプレッドシートにせず、DBのみにしてスプレッドっシートの使用を完全にやめて、全てpythonファイルとDBのみにすることだが、時間がなく、しょうがないので以下の方法で行う。
#「DDG-database+チャットログ（重要）」のポイント管理（スプレッドシート）の3L~15Vを「derc.db」のbadgedataの3列目（receivePt_zentai）~12列目（receivePt_ritakouiLv2）の情報に更新する。
#定期実行を関数を呼ぶことによって行いたいが、関数にしてflask内でその関数を呼んで実行するというやり方だとなぜかできないため、一つのページを更新した時に関数を呼ぶようにし、実験中はサーバー側でwebページを開いておき、定期で更新することでスクリプトが1分ごとに走る仕組みにする。
def UpdateDB():
    all_infoDBss = np.array(worksheet1.get_all_values())#ポイント管理のシートの全ての情報をとってくる。##############################################
    
    # model class（badgedata用）
    class Badgedata(Base):
        __tablename__ = 'badgedata'
        __table_args__ = {'extend_existing': True}
    
        id = Column(Integer, primary_key=True)
        receivePt_zentai = Column(Integer)
        receivePt_discuss = Column(Integer)
        receivePt_discussLv1 = Column(Integer)
        receivePt_discussLv2 = Column(Integer)
        receivePt_hosuu = Column(Integer)
        receivePt_hosuuLv1 = Column(Integer)
        receivePt_hosuuLv2 = Column(Integer)
        receivePt_ritakoui = Column(Integer)
        receivePt_ritakouiLv1 = Column(Integer)
        receivePt_ritakouiLv2 = Column(Integer)

    # get Dict data
    def toDict(self):
        return {
            'id':int(self.id), 
            'receivePt_zentai' : int(self.receivePt_zentai),
            'receivePt_discuss' : int(self.receivePt_discuss),
            'receivePt_discussLv1' : int(self.receivePt_discussLv1),
            'receivePt_discussLv2' : int(self.receivePt_discussLv2),
            'receivePt_hosuu' : int(self.receivePt_hosuu),
            'receivePt_hosuuLv1' : int(self.receivePt_hosuuLv1),
            'receivePt_hosuuLv2' : int(self.receivePt_hosuuLv2),
            'receivePt_ritakoui' : int(self.receivePt_ritakoui),
            'receivePt_ritakouiLv1' : int(self.receivePt_ritakouiLv1),
            'receivePt_ritakouiLv2' : int(self.receivePt_ritakouiLv2),
        }

    for human in range(len(all_user)):
        id = human + 1#その人のidを取ってくる。
        ###ss（スプレッドシート）から情報を取ってくる。
        print(all_infoDBss[2 + human][12])
        print(human)
        receivePt_zentai_ss = int(all_infoDBss[2 + human][12])
        receivePt_discuss_ss = int(all_infoDBss[2 + human][13])
        receivePt_discussLv1_ss = int(all_infoDBss[2 + human][14])
        receivePt_discussLv2_ss = int(all_infoDBss[2 + human][15])
        receivePt_hosuu_ss = int(all_infoDBss[2 + human][16])
        receivePt_hosuuLv1_ss = int(all_infoDBss[2 + human][17])
        receivePt_hosuuLv2_ss = int(all_infoDBss[2 + human][18])
        receivePt_ritakoui_ss = int(all_infoDBss[2 + human][19])
        receivePt_ritakouiLv1_ss = int(all_infoDBss[2 + human][20])
        receivePt_ritakouiLv2_ss = int(all_infoDBss[2 + human][21])

        ###DBから情報を取ってくる。
        DBinfotwo = []
        DBinfo = []
        db = get_db()
        cur_DBss = db.execute("select * from badgedata where id = {id}".format(id = id))
        DBinfotwo = cur_DBss.fetchall()
        for kkk in range(30):#DBから取ってきたままだと2次元で扱いにくいため一次元に返還する。
            DBinfo.append(DBinfotwo[0][kkk])
            #以下それぞれの獲得ポイントを格納する。
        receivePt_zentai = DBinfo[2]
        receivePt_discuss = DBinfo[3]
        receivePt_discussLv1 = DBinfo[4]
        receivePt_discussLv2 = DBinfo[5]
        receivePt_hosuu = DBinfo[6]  
        receivePt_hosuuLv1 = DBinfo[7]
        receivePt_hosuuLv2 = DBinfo[8]
        receivePt_ritakoui = DBinfo[9]
        receivePt_ritakouiLv1 = DBinfo[10]
        receivePt_ritakouiLv2 = DBinfo[11]
        close_db()

        Session = sessionmaker(bind = engine)
        ses = Session()
        BadgedataDBss = ses.query(Badgedata).filter(Badgedata.id == id).one()

        #以下、スプレッドシートの情報とDBの情報が合致していなかったらDBに更新させる。（一つでも更新されていれば、全体のポイント数を更新するようにする。）
        if receivePt_zentai_ss != receivePt_zentai or receivePt_discuss_ss != receivePt_discuss or receivePt_discussLv1_ss != receivePt_discussLv1 or receivePt_discussLv2_ss != receivePt_discussLv2 or receivePt_discussLv2_ss != receivePt_discussLv2 or receivePt_hosuu_ss != receivePt_hosuu or receivePt_hosuuLv1_ss != receivePt_hosuuLv1 or receivePt_hosuuLv2_ss != receivePt_hosuuLv2 or receivePt_ritakoui_ss != receivePt_ritakoui or receivePt_ritakouiLv1_ss != receivePt_ritakouiLv1 or receivePt_ritakouiLv2_ss != receivePt_ritakouiLv2:
            BadgedataDBss.receivePt_zentai = receivePt_zentai_ss
            BadgedataDBss.receivePt_discuss = receivePt_discuss_ss
            BadgedataDBss.receivePt_discussLv1 = receivePt_discussLv1_ss
            BadgedataDBss.receivePt_discussLv2 = receivePt_discussLv2_ss
            BadgedataDBss.receivePt_hosuu = receivePt_hosuu_ss
            BadgedataDBss.receivePt_hosuuLv1 = receivePt_hosuuLv1_ss
            BadgedataDBss.receivePt_hosuuLv2 = receivePt_hosuuLv2_ss
            BadgedataDBss.receivePt_ritakoui = receivePt_ritakoui_ss
            BadgedataDBss.receivePt_ritakouiLv1 = receivePt_ritakouiLv1_ss
            BadgedataDBss.receivePt_ritakouiLv2 = receivePt_ritakouiLv2_ss

        ses.add(BadgedataDBss)
        ses.commit()
        ses.close()


##スプレッドシートの情報をDBにアップデートする関数

#外部公開したい場合は下のapp.runを使用する。ローカルでテストで走らせたいだけの場合は上のapp.runを使用する。
if __name__ == '__main__':
    app.run()
    #app.run(debug=False, host='0.0.0.0', threaded=True, port=50009)
