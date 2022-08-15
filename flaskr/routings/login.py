from flask import Flask, flash, render_template, request, session, redirect, send_file, g, Blueprint
#ホームページ
bp_login = Blueprint('login', __name__)

#ログインページ
@bp_login.route('/Login', methods=['GET'])
def Login():
    return render_template('Login.html',
            title='Login page',
            err=False,)
            
#入力された名前とpasswordがスプレッドシートと合致していたらログインできる。
@bp_login.route('/Login', methods=['POST'])
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
