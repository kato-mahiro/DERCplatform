#終了した議論に自分が関わっていたら成績が見れる。関わっていなかったらあなたはこの議論に参加していません。的なページを出す。
@app.route('/finish', methods=['GET'])
def Finish():
    channel = session['channel']
    name = session['name']
    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    chan_list = all_webchan[:, 1]#シート2のチャンネルリスト全体をとってくる。
    chan_info_giron = all_webchan[:, 2]#チャンネルの議論の情報全体を取ってくる(議論1,議論2....など)
    chan_info = all_webchan[:, 3]#チャンネルの議論の情報全体を取ってくる（ari,playing,shuuryou）
    
    chanNum = 0
    for aaa in chan_list:#チャンネルが配列の中の何番目なのかを検索する。
        if aaa != channel:
            chanNum = chanNum + 1
        else:
            break

    chan_info_giron_Num = chan_info_giron[chanNum]#議論番号を取得(議論1,議論2....など)
    chan_info_Num = chan_info[chanNum]#議論情報を取得（ari,playing,shuuryou）

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
   
    if chan_info_Num == "shuuryou":  
        webDisinfo = workbook_webdiscuss.worksheet(chan_info_giron_Num)
        all_webDisinfo = np.array(webDisinfo.get_all_values())#webDisinfoの全てのログを持ってくる。################################################

        result = all_webDisinfo[43]#議論？の中の44行目「レベル１とレベル２の合計」の中で自分の欄が0以外だった場合、議論に参加していたという事。
        mNumber = all_user.index(name)#自分の番号何番目
        zibun_result = result[mNumber + 3]

        if zibun_result == 0:
            return render_template('finish.html',
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
            title='Result')

        else:
            kakeaite = all_webDisinfo[32][mNumber + 3]#賭けた相手
            kakepoint = all_webDisinfo[33][mNumber + 3] #賭けたポイント
            hihyoukapoint1 = all_webDisinfo[38][mNumber + 3]#レベル１で得たポイント
            seikousippai = all_webDisinfo[40][mNumber + 3]#成功/失敗
            hihyoukapoint2 = all_webDisinfo[41][mNumber + 3]#レベル２で得たポイント
            sougoupoint = all_webDisinfo[43][mNumber + 3]#総合的にポイントの加算・減算
            
            return render_template('finish.html',
            name = name,
            channel = channel,
            kakeaite = kakeaite,
            kakepoint = kakepoint,
            hihyoukapoint1 = hihyoukapoint1,
            seikousippai = seikousippai,
            hihyoukapoint2 = hihyoukapoint2,
            sougoupoint = sougoupoint,
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
            title='Result')

    else:
        return render_template('finish.html',
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
        title='Result')