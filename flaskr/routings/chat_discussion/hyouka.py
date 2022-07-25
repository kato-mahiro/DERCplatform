#評価ページ（最初の評価以外はこのページを使用する。）
@app.route('/hyouka/<number>', methods=['GET'])
def hyouka(number):
#スプレッドシートに保存する用プログラム始まり
    name = session['name']#評価の欄に書き込む自分の名前を取ってくる。
    channel = session['playingchannel']
    # slackのログを保存したスプレッドシートを指名す
    # SlackのチャンネルIDとチャンネル名を合わせる。
    worksheet_slacklog1 = workbook_slacklog_EventAPI.worksheet(channel)################################################
    # 評価ボタンを押した部分の発言の場所をスプレッドシートから探す。
    #cell = worksheet_slacklog1.find(log)
    #評価欄に自分以外の名前があったらそれ以降のセルに記入する。
    useridcell = all_user.index(name)
    worksheet_slacklog1.update_cell(int(number) + 3, useridcell +7 , "good")################################################書き込み
#スプレッドシートに保存する用プログラム終わり

#評価を通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #評価する相手のuserID取ってくる
    all_worksheet_slacklog1 = np.array(worksheet_slacklog1.get_all_values())#worksheet_slacklog1の全てのログを持ってくる。################################################
    user_id = all_worksheet_slacklog1[int(number) + 2, 0]
    post_content = all_worksheet_slacklog1[int(number) + 2, 1]

    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "チャット議論のチャンネル[" + channel +"]であなたの「" + post_content[0:10] + "」の投稿が評価されました。")
#評価を通知するプログラム終わり

#評価を自分に通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #自分のuserID取ってくる

    zibun = all_user.index(name)#自分の名前の番号取得
    user_id = all_user_ID[zibun]#評価相手のslackのIDを取ってくる。

    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "chat議論で評価しました！")
#評価を通知するプログラム終わり

    return redirect('/Discussing_Chat')