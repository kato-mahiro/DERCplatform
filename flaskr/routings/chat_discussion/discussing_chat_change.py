#継続中に議論の時間を変更するページ。
@app.route('/Discussing_chat_change/<channel>', methods=['GET'])
def Discussing_chat_change(channel):
    name = session['name']
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。################################################
    chan_list = all_worksheet2[:, 1]#シート2のチャンネルリスト全体をとってくる。
    
    chanNum = 0
    for aaa in chan_list:#チャンネルが配列の中の何番目なのかを検索する。
        if aaa != channel:
            chanNum = chanNum + 1
        else:
            break  
    finish = all_worksheet2[chanNum , 4]#終了時刻の取得
    session['chanNum'] = chanNum#GETとPOSTの間だけ保持

    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('Discussing_change.html',
    channel = channel,
    finish = finish,
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
    name = name,
    title='Ending time')

@app.route('/Discussing_chat_change/<channel>', methods=['POST'])
def Discussing_chat_change_POST(channel):
    discussionfinishdate = request.form.get('discussionfinishdate')#終了
    discussionfinishtime = request.form.get('discussionfinishtime')

    chanNum = session['chanNum']#GETとPOSTの間だけ保持
    session.pop('chanNum',None)

    discussionfinish = discussionfinishdate +" " +discussionfinishtime
    worksheet2.update_cell(chanNum + 1, 5, discussionfinish)################################################

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #評価するチャンネルのID取ってくる
    chan_id ="C025ET1R3UG"##chat議論おしらせチャンネル

    # DMを送信する
    client.chat_postMessage(channel= chan_id, text= channel + "の終了時刻が" +  discussionfinish + "に変更されました。")
    #評価を通知するプログラム終わり

    return redirect('/Discussing_Chat')
