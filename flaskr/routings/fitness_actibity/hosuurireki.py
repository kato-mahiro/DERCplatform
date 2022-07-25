#今までの歩数や、履歴を見れるページ
@app.route('/hosuurireki', methods=['GET'])
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