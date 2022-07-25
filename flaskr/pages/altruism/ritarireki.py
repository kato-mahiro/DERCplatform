#利他行為の履歴に入れる情報:自分が何回利他行為を行ったか、自分が利他行為を何回受け取ったか、誰に賭けたのか、賭けが成功したか。
@app.route('/ritarireki', methods=['GET'])
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
