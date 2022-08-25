#ssやGASなどはこちらのリンクから持ってきてください。https://drive.google.com/drive/folders/1zCVqcMWUY0W2wT9kEX5VcTyeV3cTgOsD?usp=sharing
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from flask import Flask, flash, render_template, request, session, redirect, send_file, g
from threading import Thread
import sqlite3

#ページ設定ファイルのimport
from main_pages import *
from altruism_pages import *
from chat_discussion_pages import *
from web_discussion_pages import *
from fitness_pages import *

#以下メモ
#GASからDBを操作したいと思ったときに、定期実行の方法がないため次の方法で行う。
#pythonファイルで、ssの情報とDBの情報が違っていれば（ssが更新されていれば）スプレッドシートの情報をDBに書き込む、という関数を1分ごとに起動させる
#一番行いたいこととしては、データの保存方法をスプレッドシートにせず、DBのみにしてスプレッドっシートの使用を完全にやめて、全てpythonファイルとDBのみにすることだが、時間がなく、しょうがないので以下の方法で行う。
#「DDG-database+チャットログ（重要）」のポイント管理（スプレッドシート）の3L~15Vを「derc.db」のbadgedataの3列目（receivePt_zentai）~12列目（receivePt_ritakouiLv2）の情報に更新する。
#定期実行を関数を呼ぶことによって行いたいが、関数にしてflask内でその関数を呼んで実行するというやり方だとなぜかできないため、一つのページを更新した時に関数を呼ぶようにし、実験中はサーバー側でwebページを開いておき、定期で更新することでスクリプトが1分ごとに走る仕組みにする。

#外部公開したい場合は下のapp.runを使用する。ローカルでテストで走らせたいだけの場合は上のapp.runを使用する。
app = Flask(__name__)
app.secret_key = b'random string...'
app.register_blueprint(bp_main)
app.register_blueprint(bp_altruism)
app.register_blueprint(bp_chatdiscussion)
app.register_blueprint(bp_webdiscussion)
app.register_blueprint(bp_fitness)
app.run(debug=True)
#app.run(debug=False, host='0.0.0.0', threaded=True, port=50009)
