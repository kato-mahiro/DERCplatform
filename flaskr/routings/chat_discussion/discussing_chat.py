#評価ページ
@app.route('/Discussing_Chat', methods=['GET'])
def Discussing_Chat():
    channel = session['playingchannel']
    # slackのログを保存したスプレッドシートを指名する
    #SlackのチャンネルIDとチャンネル名を合わせる。
    worksheet_slacklog = workbook_slacklog_EventAPI.worksheet(channel)#チャンネルのログを取ってくる。
    all_worksheet_slacklog = np.array(worksheet_slacklog.get_all_values())#worksheet_slacklogの全てのログを持ってくる。###############################################
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。###############################################
  
    slacklog_time =  all_worksheet_slacklog[:, 1] # slacklog_timeにシート1からB（議論のログ）の列を一次元配列で取得。
    slacklogname_list = all_worksheet_slacklog[:, 2] #slacklogname_listにシート1からC（名前）の列を一次元配列で取得。
    slacklog_list = all_worksheet_slacklog[:, 3]  # slacklog_listにシート1からD（時間）の列を一次元配列で取得。
    hihyoukanum = all_worksheet_slacklog[:, 5]  # slacklog_listにシート1からF（批評家回数）の列を一次元配列で取得。]

    chan_list = all_worksheet2[:, 1]#チャンネルリストを取得
    Number = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    finishtime = all_worksheet2[Number - 1][4]  # 終了時刻を格納

    slacklog = []
    name = session['name']
    
    for j in range(len(slacklogname_list)-2):
        if slacklogname_list[j + 2] != name:
             hihyoukanum[j + 2] = "tanin"
    

    for i in range(len(slacklogname_list)-2):
        if  slacklog_list[i + 2] != "": #ログがなくなったら終わり。     
            slacklog.append([slacklog_time[i+2], slacklog_list[i+2],slacklogname_list[i+2] , i, hihyoukanum[i+2]])#上記の4つの一次元配列を足し合わせて二次元配列にする。
    
        else:
            break
    
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
    
    return render_template('Discussing_Chat.html', #上の一文でエラーが出たらログ、名前、日時のどこかが抜けている。
    data=slacklog,
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
    finishtime = finishtime,
    channel = channel,
    title=channel +"  " 'Log')

@app.route('/Discussing_Chat', methods=['POST'])
def Discussing_Chat_POST():
    log = request.form.get('item')
    print(log)
    return redirect('/')