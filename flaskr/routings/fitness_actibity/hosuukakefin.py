#歩数の賭けが終わった後に表示されるページ
@app.route('/hosuukakefin', methods=['GET'])
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
        title='Thank you')