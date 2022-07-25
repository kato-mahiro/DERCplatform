#Thank youと言うページ
@app.route('/Thankyou_web', methods=['GET'])
def Thankyou_web():
    name = session['name']
    channel = session['channel'] 
    session.pop(channel,channel)
    ############################
    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    chan_list =all_webchan[:, 1]#チャンネルリストを取得
    Number = 0
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    starttimestr = all_webchan[Number, 4]#議論の始まりの時間取得##
    print(Number)
    print(chan_list)
    zibun = all_user.index(name)#自分の名前の番号取得
    kakeperson = all_webchan[Number , (2 * zibun) + 6]#自分が賭けた人を記録##
    kakepoint = all_webchan[Number, (2 * zibun) + 7]#自分が賭けたポイント数を記録##
    if kakepoint != " ":#賭けがあれば「1」無ければ「0」
        kakezyouhou = 0

    else:
        kakezyouhou = 1

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('Thankyou_web.html',
    channel = channel,
    name = name,
    starttime =starttimestr,
    kakeperson = kakeperson,
    kakepoint = kakepoint,
    kakezyoukyou = kakezyouhou,
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
    title='Thank you for your cooperation!!')
