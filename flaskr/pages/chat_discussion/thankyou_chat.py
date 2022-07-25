#Thank you言うページ
@app.route('/Thankyou_Chat', methods=['GET'])
def Thankyou_Chat():
    name = session['name']
    print(name)
    channel = session['channel'] 
    session.pop(channel,channel)
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。################################################
    chan_list = all_worksheet2[:, 1]#チャンネルリストを取得
    Number = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    print(Number)
    starttimestr = all_worksheet2[Number - 1][3]#議論の始まりの時間取得
    finishtimestr= all_worksheet2[Number - 1][4]#議論の終わりの時間取得
    zibun = all_user.index(name)#自分の名前の番号取得
    kakeperson = all_worksheet2[Number - 1][(2 * zibun) + 5]#自分が賭けた人を記録
    kakepoint = all_worksheet2[Number - 1][(2 * zibun) + 6]#自分が賭けたポイント数を記録
    
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('Thankyou_Chat.html',
    channel = channel,
    name = name,
    starttime =starttimestr,
    finishtime = finishtimestr,
    kakeperson = kakeperson,
    kakepoint = kakepoint,
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
