#ビデオ議論選択ページ
@app.route('/Channelselection_web', methods=['GET'])
def Channelselection_web():

    name = session['name']
    nam = session['login']
    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    chan_list = all_webchan[:, 1]#シート2のチャンネルリストをとってくる。
    chan_info = all_webchan[:, 3]#チャンネルの議論の情報を取ってくる。
    chan_info_a = []#上のari,nasi,playingをDERC設定あり、DERC設定なし、DERCでの議論進行中、に変える。
    for i in range(len(chan_list)):
        if chan_info[i] == "ari":
            chan_info_a.append("ゲーム設定あり")

        elif chan_info[i] == "nasi":
            chan_info_a.append("ゲーム設定なし")

        elif chan_info[i] == "playing":
            chan_info_a.append("ゲーム進行中")

        elif chan_info[i] == "shuuryou":
            chan_info_a.append("この議論は終了しています。")

        elif chan_info[i] == "":
            chan_info_a.append("空白")

        else:
            chan_info_a.append("エラー")


    chan_a = []#チャンネル名とチャンネル情報を合わせた二次元配列
    for j in range(len(chan_info_a)):
        if chan_info_a[j] == "空白":
            break

        else:
            chan_a.append([chan_list[j], chan_info_a[j]])

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    return render_template('Channelselection_web.html',
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
            title='Channel selection(オンライン議論)',
            chan_list = chan_a)
