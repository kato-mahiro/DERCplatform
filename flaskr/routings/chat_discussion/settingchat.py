#議論情報「nasi」から飛んできた場合、議論を設定できる
@app.route('/settingchat', methods=['GET'])
def settingchat():
    channel = session['channel']
    name = session['name']
    Number = 0
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。################################################
    chan_list = all_worksheet2[:, 1]#シート2のチャンネルリストをとってくる。
    # 注意！！クエリパラメーターのchannelをそのまま持ってくると、channelには実は"BBQ日程決め"などの本当に得たいものと"site.webmanifest"というものも入ることがわかったので、"site.webmanifest"を除外している。
    if channel != "site.webmanifest":
        chan = channel
        for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
            if i != chan:
                Number += 1
            elif i == chan:
                break
    chan_list = all_worksheet2[:, 1]#シート2のチャンネルリストをとってくる。
    chanNumber = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            chanNumber += 1
        elif i == channel:
            break

    chan_list_PorA = chan_info = all_worksheet2[:, 2]  # シート2からチャンネルがDERC設定が有か無しかを取得（Presence or Absence→PorA）。
    session['Number'] = Number
    starttimestr = all_worksheet2[chanNumber - 1][3]
    finishtimestr= all_worksheet2[chanNumber - 1][4]

    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    if len(starttimestr) != 0:
        return render_template('ChannelSetting_Chat.html',
        arinasi = "の議論の設定",
        title='Setting',
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
        zyoukyou1 ="既に",
        start = starttimestr,
        finish = finishtimestr,
        zyoukyou2 = "に設定されています",
        name = name,
        channel=channel)

    else:
        return render_template('ChannelSetting_Chat.html',
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
        arinasi = "の議論の設定",
        title='Setting',
        name = name,
        channel=channel)

@app.route('/settingchat', methods=['POST'])
def settingchatPOST():
    discussionstartdate = request.form.get('discussionstartdate')#開始
    discussionstarttime = request.form.get('discussionstarttime')
    discussionfinishdate = request.form.get('discussionfinishdate')#終了
    discussionfinishtime = request.form.get('discussionfinishtime')
    Number = session['Number']
    zikangime = Number +1
    discussionstart = discussionstartdate +" " +discussionstarttime
    discussionfinish = discussionfinishdate +" " +discussionfinishtime
    worksheet2.update_cell(zikangime, 4, discussionstart)################################################書き込み
    worksheet2.update_cell(zikangime, 5, discussionfinish)################################################書き込み
    worksheet2.update_cell(zikangime, 3, "ari")################################################書き込み



    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #評価する相手のuserID取ってくる
    chan_id = "C025ET1R3UG"###chatお知らせチャンネル

    # DMを送信する
    client.chat_postMessage(channel=chan_id, text= "議論部屋"  + zikangime + "に" + discussionstart + "から" + discussionfinish +"までのDERCが設定されました。" + "参加される方は開始時刻までに賭けを行ってください。")
    #評価を通知するプログラム終わり



    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #評価する相手のuserID取ってくる
    chan_id = chan_IDlist[Number]###chatお知らせチャンネル

    # DMを送信する
    client.chat_postMessage(channel=chan_id, text= "この議論部屋に" + discussionstart + "から" + discussionfinish +"までのDERCが設定されました。" + "参加される方は開始時刻までに賭けを行ってください。")
    #評価を通知するプログラム終わり



    return redirect('/Thankyou_Chat')