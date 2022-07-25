#point_history、ポイント履歴確認ページ
@app.route('/point_history', methods=['GET'])
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
