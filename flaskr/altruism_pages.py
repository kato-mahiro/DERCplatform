#利他行動に関連するページの定義
from utils import *
from global_settings import *
from flask import Flask, flash, render_template, request, session, redirect, send_file, g, Blueprint
bp_altruism = Blueprint('bp_altruism',__name__)

#ページ選択ができるページ
@bp_altruism.route('/rita', methods=['GET'])
def rita():
    name = session['name']

    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
  
    return render_template('rita.html',
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
    title='利他行為')

#賭けができる
@bp_altruism.route('/ritakake', methods=['GET'])
def ritakake():
    name = session['name']
    all_worksheet1 = np.array(worksheet1.get_all_values())#worksheet1の全てのログを持ってくる。################################################

    ritaozzu = all_worksheet1[:, 6] #ユーザーの歩数でのオッズを一次元配列で取得。
    kakezyouhou = []

    for i in range(len(all_user)):
        kakezyouhou.append([all_user[i], ritaozzu[i + 2]])#上記の4つの一次元配列を足し合わせて二次元配列にする。

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

    return render_template('ritakake.html',
    title='利他行為賭けページ',
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

@bp_altruism.route('/ritakake', methods=['POST'])
def ritakakePOST():
    name = session['name']
    mNumber = all_user.index(name)#賭け対象選択ページで自分の名前を表示させないために配列の何番目が自分なのか取得。
    kakeperson = request.form.get('kakeperson')#開始
    kakepoint = request.form.get('kakepoint')

    ritasheet.update_cell(6, mNumber + 12, kakeperson)################################################書き込み
    ritasheet.update_cell(7, mNumber + 12, kakepoint)################################################書き込み
    
    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペース
    client = WebClient(token)
    #自分のuserID取ってくる
    user_id = all_user_ID[mNumber]#自分のslackのIDを取ってくる。
    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "利他行為の賭けであなたは" + kakeperson + "に" + kakepoint + "ポイントの賭けを行いました。")
    #評価を通知するプログラム終わり

    return redirect('/ritakakefin')

#賭けが終わった後に表示されるページ
@bp_altruism.route('/ritakakefin', methods=['GET'])
def ritakakefin():
    name = session['name']
    mNumber = all_user.index(name)#自分の番号何番目
    all_ritasheet = np.array(ritasheet.get_all_values())#ritasheetの全てのログを持ってくる。################################################

    kakeperson = all_ritasheet[ 5 , mNumber + 11]#賭けた対象を取得
    kakepoint = all_ritasheet[ 6 , mNumber + 11]#賭けたポイントを取得
    

    if kakeperson == " ":
      return redirect('/ritakake')#賭けている人がいない場合、賭けページに戻る。
    
    else :
        id = session['id']
        updateBadgeinfo(id)
        Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
        return render_template('ritakakefin.html',
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
        title='Thank you')

#利他行為の履歴に入れる情報:自分が何回利他行為を行ったか、自分が利他行為を何回受け取ったか、誰に賭けたのか、賭けが成功したか。
@bp_altruism.route('/ritarireki', methods=['GET'])
def ritarireki():
    name = session['name']
    mNumber = all_user.index(name)#自分の番号何番目
    all_ritasheet = np.array(ritasheet.get_all_values())#ritasheetの全てのログを持ってくる。################################################

    date = all_ritasheet[:, 10]#日にちを取得
    ritarireki = all_ritasheet[:, mNumber + 11]#自分の利他行為の履歴を取得

    rita = []
    rita.append(["日時", "利他行為されたと他者に認定された回数", "Lv1の受け取りポイント" , "利他行為されたと自らで認定した回数" , "賭けた人" , "賭けたポイント" , "Lv2の受け取りポイント"])#紹介文を先に入れておく

    for i in range(20):
      rita.append([date[i*7+9] , ritarireki[i*7+9] , ritarireki[i*7+10] , ritarireki[i*7+11] , ritarireki[i*7+13] , ritarireki[i*7+14] , ritarireki[i*7+15]])#上記の5つの一次元配列を足し合わせて二次元配列にする。
    
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('ritarireki.html',
    name = name,
    rita = rita,
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
    title='利他行為履歴')
