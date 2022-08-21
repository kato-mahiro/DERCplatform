from utils import *
from global_settings import *
from flask import Flask, flash, render_template, request, session, redirect, send_file, g, Blueprint
bp_main = Blueprint('bp_main',__name__)

#ホームページ
@bp_main.route('/', methods=['GET'])
def Home():
    
    if 'login' in session and session['login']:
        name = session['name']
        user_info = session['user_info']
        points = int(user_info[4])#自分のポイント数を取得
        tomorrowpoints = points * 85 // 100

        persons = []
        for i in range(len(all_user)):
          persons.append([all_user[i]])

        mNumber = all_user.index(name)#被利他行為選択ページで自分の名前を表示させない。
        persons.pop(mNumber)
        
        id = session['id']
        updateBadgeinfo(id)
        UpdateDB()
        Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

        return render_template('Home.html',
        title = 'Welcome!',
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
        err=False,
        persons = persons,
        name=name ,
        tomorrowpoints = tomorrowpoints,
        points = points)

    else:
        return redirect('/Login')

@bp_main.route('/', methods=['POST'])
def Home_post():
    name = session['name']
    ritaname = request.form.get('ritaperson')
    message = request.form.get('message')

    ritasheetrowlength =1 + len(ritasheet.col_values(1) )#行の長さを取得する。
    ritasheet.update_cell(ritasheetrowlength, 3, name)################################################書き込み
    ritasheet.update_cell(ritasheetrowlength, 4, ritaname)################################################書き込み
    ritasheet.update_cell(ritasheetrowlength, 5, message)################################################書き込み
    ritasheet.update_cell(ritasheetrowlength, 1, "あ")################################################書き込み

    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    return render_template('Thankyourita.html',
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
        title='Thank you!!',
        name = name,
        err=False)

@bp_main.route('/discussHome', methods=['GET'])
def discussHome():
    name = session['name']
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    return render_template('discussHome.html',
            title='Choice of discussion method',
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
            name = name,
            err=False)

#ログインページ
@bp_main.route('/Login', methods=['GET'])
def Login():
    return render_template('Login.html',
            title='Login page',
            err=False,)
            
#入力された名前とpasswordがスプレッドシートと合致していたらログインできる。
@bp_main.route('/Login', methods=['POST'])
def login_post():
    Number = 1
    global member_data
    name = request.form.get('name')
    pswd = request.form.get('pass')
    
    if name in all_user:
      namenum = all_user.index(name)
    
    else:
        return render_template('Login.html',
            title='Login page',
            err=False)



    user_info = worksheet1.row_values(namenum + 3)  #user_listにシート1からユーザーの情報を一次元配列で取得。############################################################
    if pswd ==all_user_pswd[namenum]:#入力されたパスワードがあっているか確認（user_listのなかにあるか確認）
        session['login'] = True
    else:
        session['login'] = False

    session['name'] = name #nameを全ページで保存する。
    session['user_info'] = user_info #user_infoを全ページで保存する。
    session['id'] = all_user.index(name) + 1#DB取得の貯めに必要なidを保存。


    if session['login']:
        return redirect('/')
    else:
        return render_template('Login.html',
            title='Login page',
            err=False)

#ログアウトのため
# logout
@bp_main.route('/logout', methods=['GET'])
def logout():
    session.pop('name', None)
    session.pop('login',None)
    session.pop('id',None)
    return redirect('/Login')

#point_history、ポイント履歴確認ページ
@bp_main.route('/point_history', methods=['GET'])
def point_history():
    name = session['name']
    user_num = all_user.index(name)#自分の名前をログでとってくる。
    all_pointrireki = np.array(pointrireki.get_all_values())#ポイント履歴の全てのログを持ってくる。##############################################
    date_list = all_pointrireki[1]#日付を取ってくる。
    point_list = all_pointrireki[user_num + 2]
    rireki = []
    for i in range(point_list.size - 2):#最初の二つを取って来ないようにするため。
        rireki.append([date_list[point_list.size - (i+1)], point_list[point_list.size - (i+1)]])#2つの一次元配列を足し合わせて二次元配列にする。
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    return render_template('point_history.html',
            title='ポイント履歴',
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
            pointsrireki = rireki,
            name = name,
            err=False,)

#db用、多分使われてない？
@bp_main.route('/UpdateDB', methods=['GET'])
def UpdateDB_GET():
    UpdateDB()

    return render_template('UpdateDB.html')