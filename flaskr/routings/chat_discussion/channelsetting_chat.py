#テキスト議論を選択したら、各議論の状態のページに行くことができる（議論中→評価ページ、議論前→賭けページ、など）
@app.route('/ChannelSetting_Chat/<channel>', methods=['GET'])
def ChannelSetting_Chat(channel):
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

    chanNumber = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            chanNumber += 1
        elif i == channel:
            break
    session['chanNumber'] = chanNumber

    chan_list_PorA = chan_info = all_worksheet2[:, 2]  # シート2からチャンネルがDERC設定が有か無しかを取得（Presence or Absence→PorA）。
    session['Number'] = Number
    if chan_list_PorA[Number] == "ari":
        session['channel'] = channel
        return redirect('/kake_chat')  #kake_chatへ

    elif chan_list_PorA[Number] == "playing":
        session['playingchannel'] = channel
        return redirect('/Discussing_Chat')  # 議論が始まっているのでDiscussing_Chatへ

    elif chan_list_PorA[Number] == "nasi":
        session['channel'] = channel
        return redirect('/settingchat')