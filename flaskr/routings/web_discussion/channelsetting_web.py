#議論情報「nasi」から飛んできた場合
@app.route('/ChannelSetting_Web', methods=['GET'])
def ChannelSetting_Web():
    nam = session['login']
    name = session['name']
    # 注意！！クエリパラメーターのchannelをそのまま持ってくると、channelには実は"BBQ日程決め"などの本当に得たいものと"site.webmanifest"というものも入ることがわかったので、"site.webmanifest"を除外している。
    
    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    return render_template('ChannelSetting_Web.html',#notなので賭けるページへ
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
        name = name)

#ビデオ議論が設定できる。
@app.route('/ChannelSetting_Web', methods=['POST'])
def ChannelSetting_WebPOST():
    discussionstartdate = request.form.get('discussionstartdate')#開始
    discussionstarttime = request.form.get('discussionstarttime')
    discussionfinishdate = request.form.get('discussionfinishdate')#終了
    discussionfinishtime = request.form.get('discussionfinishtime')
    odai = request.form.get('odai')#お題を取ってくる。
    chan_list = webchan.col_values(2)  # シート2のチャンネルリストをとってくる。################################################
    webchan.update_cell(len(chan_list) + 1, 2, odai)################################################
    discussionstart = discussionstartdate +" " +discussionstarttime
    discussionfinish = discussionfinishdate +" " +discussionfinishtime
    webchan.update_cell(len(chan_list) + 1, 5, discussionstart)################################################
    webchan.update_cell(len(chan_list) + 1, 6, discussionfinish)################################################
    webchan.update_cell(len(chan_list) + 1, 4, "ari")################################################

    session['channel'] = odai

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #評価するチャンネルのID取ってくる
    chan_id ="C022UPX11FB"##オンライン議論おしらせチャンネル

    # DMを送信する
    client.chat_postMessage(channel= chan_id, text= "「" + odai + "」というお題で" + discussionstart + "から" + discussionfinish +"までのDERCが設定されました。" + "参加される方は開始時刻までに賭けを行ってください。")
    #評価を通知するプログラム終わり



    return redirect('/Thankyou_web')
