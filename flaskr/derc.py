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
from routings.home import *
from routings.login import *


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
app.register_blueprint(bp_home)
app.register_blueprint(bp_login)

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


#外部公開したい場合は下のapp.runを使用する。ローカルでテストで走らせたいだけの場合は上のapp.runを使用する。
if __name__ == '__main__':
    app.run()
    #app.run(debug=False, host='0.0.0.0', threaded=True, port=50009)
