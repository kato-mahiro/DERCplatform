#歩数関連のページの定義
from utils import *
from global_settings import *
from flask import Flask, flash, render_template, request, session, redirect, send_file, g, Blueprint
bp_fitness = Blueprint('bp_fitness',__name__)

#ページ選択ができるページ
@bp_fitness.route('/hosuu', methods=['GET'])
def hosuu():
    name = session['name']
    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    return render_template('hosuu.html',
    name = name,
    zentai = Badgeinfo[0],
    discuss = Badgeinfo[1],
    discussLv1 = Badgeinfo[2],
    discussLv2 = Badgeinfo[3],
    hosuu = Badgeinfo[4],
    hosuuLv1 = Badgeinfo[5],
    hosuuLv2 = Badgeinfo[6],
    ritakoui = Badgeinfo[7],
    ritakouiLv1 = Badgeinfo[8],
    ritakouiLv2 = Badgeinfo[9],
    title='歩数計算')#歩数の賭けができる
@bp_fitness.route('/hosuukake', methods=['GET'])
def hosuukake():
    name = session['name']
    all_worksheet1 = np.array(worksheet1.get_all_values())#worksheet1の全てのログを持ってくる。################################################

    hosuuozzu = all_worksheet1[:, 5] #ユーザーの歩数でのオッズを一次元配列で取得。
    kakezyouhou = []

    for i in range(len(all_user)):
        kakezyouhou.append([all_user[i], hosuuozzu[i + 2]])#上記の4つの一次元配列を足し合わせて二次元配列にする。

    mNumber = all_user.index(name)#賭け対象選択ページで自分の名前を表示させないために配列の何番目が自分なのか取得。
    kakezyouhou.pop(mNumber)
 
    point =  int(all_worksheet1[mNumber+ 2][4])#自分のポイント数を取得
    kakepointlow = point//10#賭けることができる最低ポイント数を取得
    kakepointhigh = kakepointlow*2#賭けることができる最高ポイント数を取得

    kakerange = []
    for p in range(kakepointlow,kakepointhigh + 1):#最低ポイント～最高ポイントで１ずつ配列に入れる。
        kakerange.append(p)

    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('hosuukake.html',
    title='歩数賭けページ',
    kakezyouhou = kakezyouhou,
    point = point,
    kakepointlow = kakepointlow,
    kakepointhigh = kakepointhigh,
    kakerange = kakerange,
    name = name,
    zentai = Badgeinfo[0],
    discuss = Badgeinfo[1],
    discussLv1 = Badgeinfo[2],
    discussLv2 = Badgeinfo[3],
    hosuu = Badgeinfo[4],
    hosuuLv1 = Badgeinfo[5],
    hosuuLv2 = Badgeinfo[6],
    ritakoui = Badgeinfo[7],
    ritakouiLv1 = Badgeinfo[8],
    ritakouiLv2 = Badgeinfo[9],
    kakesuu = kakepointhigh -kakepointlow + 1#賭けポイントの数
    )

@bp_fitness.route('/hosuukake', methods=['POST'])
def hosuukakePOST():
    name = session['name']
    mNumber = all_user.index(name)#賭け対象選択ページで自分の名前を表示させないために配列の何番目が自分なのか取得。
    kakeperson = request.form.get('kakeperson')#開始
    kakepoint = request.form.get('kakepoint')

    hosuukeisan.update_cell(5, mNumber + 29, kakeperson)################################################書き込み
    hosuukeisan.update_cell(6, mNumber + 29, kakepoint)################################################書き込み
    

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペース
    client = WebClient(token)
    #自分のuserID取ってくる
    user_id = all_user_ID[mNumber]#自分のslackのIDを取ってくる。
    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "歩数計算であなたは" + kakeperson + "に" + kakepoint + "ポイントの賭けを行いました。")
    #評価を通知するプログラム終わり

    return redirect('/hosuukakefin')
#歩数の賭けが終わった後に表示されるページ
@bp_fitness.route('/hosuukakefin', methods=['GET'])
def hosuukakefin():
    name = session['name']
    mNumber = all_user.index(name)#自分の番号何番目
    all_hosuukeisan = np.array(hosuukeisan.get_all_values())#hosuukeisanの全てのログを持ってくる。################################################

    kakeperson = all_hosuukeisan[ 4 , mNumber + 28]#賭けた対象を取得
    kakepoint = all_hosuukeisan[ 5 , mNumber + 28]#賭けたポイントを取得
    

    if kakeperson == " ":
        return redirect('/hosuukake')#賭けている人がいない場合、賭けページに戻る。
    
    else:
        id = session['id']
        Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
        return render_template('hosuukakefin.html',
        name = name,
        kakepoint = kakepoint,
        kakeperson = kakeperson,
        zentai = Badgeinfo[0],
        discuss = Badgeinfo[1],
        discussLv1 = Badgeinfo[2],
        discussLv2 = Badgeinfo[3],
        hosuu = Badgeinfo[4],
        hosuuLv1 = Badgeinfo[5],
        hosuuLv2 = Badgeinfo[6],
        ritakoui = Badgeinfo[7],
        ritakouiLv1 = Badgeinfo[8],
        ritakouiLv2 = Badgeinfo[9],
        title='Thank you')#今までの歩数や、履歴を見れるページ
@bp_fitness.route('/hosuurireki', methods=['GET'])
def hosuurireki():
    name = session['name']
    mNumber = all_user.index(name)#自分の番号何番目
    all_hosuukeisan = np.array(hosuukeisan.get_all_values())#hosuukeisanの全てのログを持ってくる。################################################

    date = all_hosuukeisan[:, 1]#日にちを取得
    hosuurireki = all_hosuukeisan[:, mNumber + 2]#自分の歩数の履歴を取得
    kakerireki = all_hosuukeisan[:, mNumber + 28]#自分の賭けの履歴を取

    hosuukekka = []
    hosuukekka.append(["日時", "自分の歩数", "賭けた相手" , "賭けたポイント" , "賭け成功/失敗"])#紹介文を先に入れておく

    for i in range(50):
      hosuukekka.append([date[i+7] , hosuurireki[i+7] , kakerireki[3 * i + 8] , kakerireki[3 * i + 9] , kakerireki[3 * i + 7]])#上記の4つの一次元配列を足し合わせて二次元配列にする。
    
    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('hosuurireki.html',
    name = name,
    hosuukekka = hosuukekka,
    zentai = Badgeinfo[0],
    discuss = Badgeinfo[1],
    discussLv1 = Badgeinfo[2],
    discussLv2 = Badgeinfo[3],
    hosuu = Badgeinfo[4],
    hosuuLv1 = Badgeinfo[5],
    hosuuLv2 = Badgeinfo[6],
    ritakoui = Badgeinfo[7],
    ritakouiLv1 = Badgeinfo[8],
    ritakouiLv2 = Badgeinfo[9],
    title='歩数関連履歴')