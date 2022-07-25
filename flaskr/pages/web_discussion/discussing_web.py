#議論を選択したら、各議論の状態のページに行くことができる（議論中→評価ページ、議論前→賭けページ、など）
@app.route('/Discussing_Web/<channel>', methods=['GET'])
def Discussing_Web(channel):
    nam = session['login']
    Number = 0
    
    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    chan_list = all_webchan[:, 1]# シート2のチャンネルリストをとってくる。
    # 注意！！クエリパラメーターのchannelをそのまま持ってくると、channelには実は"BBQ日程決め"などの本当に得たいものと"site.webmanifest"というものも入ることがわかったので、"site.webmanifest"を除外している。
    if channel != "site.webmanifest":
        chan = channel
        for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
            if i != chan:
                Number += 1
            elif i == chan:
                break
        session['Number'] = Number

    chan_list_PorA = all_webchan[:, 3] # シート2からチャンネルがDERC設定が有か無しかを取得（playing or not）。


    if chan_list_PorA[Number] == "ari":
        session['channel'] = channel
        return redirect('/kake_web')  #kake_webへ

    elif chan_list_PorA[Number] == "playing":
        session['channel'] = channel
        discussNo = all_webchan[Number, 2]#議論番号取ってくる。
        session['discussNo'] = discussNo
        return redirect('/webdiscuss')

    elif chan_list_PorA[Number] == "shuuryou":
        session['channel'] = channel
        print("ここまで")
        return redirect('/finish')