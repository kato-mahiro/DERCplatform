#賭け対象選択ページ
@app.route('/kake_web', methods=['GET'])
def kake_web():
    channel = session['channel']
    name = session['name']

    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    all_worksheet1 = np.array(worksheet1.get_all_values())#webinfoの全てのログを持ってくる。################################################
    chan_list =all_webchan[:, 1]#チャンネルリストを取得
    Number = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break

    starttimestr = all_webchan[Number - 1, 4]
    ozzu_list = all_worksheet1[:, 3] #ozzu_listからユーザーのオッズを一次元配列で取得。##
  

    kakezyouhou = []

    for i in range(len(all_user)):
        kakezyouhou.append([all_user[i], ozzu_list[i + 2]])#上記の4つの一次元配列を足し合わせて二次元配列にする。

    zibun = all_user.index(name)#賭け対象選択ページで自分の名前を表示させないために配列の何番目が自分なのか取得。
    kakezyouhou.pop(zibun)

    point =  int(all_worksheet1[zibun + 2, 4])#自分のポイント数を取得##
    kakepointlow = point//10#賭けることができる最低ポイント数を取得
    kakepointhigh = kakepointlow*2#賭けることができる最高ポイント数を取得

    kakerange = []
    for p in range(kakepointlow,kakepointhigh + 1):#最低ポイント～最高ポイントで１ずつ配列に入れる。
        kakerange.append(p)

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。    

    return render_template('kake_web.html',
    title='Setting',
    arinasi = "は議論が設定されていますが変更しますか？",
    start = starttimestr,
    channel=channel,
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

#賭け対象選択後ページ
@app.route('/kake_web', methods=['POST'])
def kake_web_POST():
    
    name = session['name']
    channel = session['channel']
    chan_list =webchan.col_values(2)#チャンネルリストを取得################################################
    Number = 0
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    

    #賭け情報の書き込み
    kakeperson = request.form.get('kakeperson')#賭ける対象
    kakepoint = request.form.get('kakepoint')#賭けるポイント数
    zibun = all_user.index(name)#自分の名前の番号取得
    webchan.update_cell(Number + 1, (2 * zibun) + 7, kakeperson)#自分が賭けた人を記録################################################
    webchan.update_cell(Number + 1, (2 * zibun) + 8, kakepoint)#自分が賭けたポイント数を記録################################################

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペース
    client = WebClient(token)
    #自分のuserID取ってくる
    user_id = all_user_ID[zibun]#評価相手のslackのIDを取ってくる。
    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "オンライン議論であなたは" + channel + "のお題で" + kakeperson + "に" + kakepoint + "ポイントの賭けを行いました。")
    #評価を通知するプログラム終わり

    return redirect('/Thankyou_web')
