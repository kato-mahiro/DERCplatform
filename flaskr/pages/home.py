#ホームページ
@app.route('/', methods=['GET'])
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

@app.route('/', methods=['POST'])
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