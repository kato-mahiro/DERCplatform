#テキスト議論選択ページ
@app.route('/Channelselection_Chat', methods=['GET'])
def Channelselection_Chat():
    name = session['name']
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。################################################
    chan_list = all_worksheet2[:, 1]#シート2のチャンネルリストをとってくる。
    chan_info = all_worksheet2[:, 2]#チャンネルの議論の情報を取ってくる。
    chan_info_a = []#上のari,nasi,playingをDERC設定あり、DERC設定なし、DERCでの議論進行中、に変える。
    for i in range(len(chan_list)):
        if chan_info[i] == "ari":
            chan_info_a.append("ゲーム設定あり")

        elif chan_info[i] == "nasi":
            chan_info_a.append("ゲーム設定なし")

        elif chan_info[i] == "playing":
            chan_info_a.append("ゲーム進行中")

        else:
            chan_info_a.append("エラー")

    chan_a = []#チャンネル名とチャンネル情報を合わせた二次元配列
    for j in range(len(chan_list)):
        if chan_list[j] =="" :
            break
        else:
            chan_a.append([chan_list[j], chan_info_a[j]])
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    
    return render_template('Channelselection_Chat.html',
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
            title='Channel selection(Chat)',
            chan_list = chan_a)
