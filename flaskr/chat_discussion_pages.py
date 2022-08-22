#チャット議論関連のページの定義
from utils import *
from global_settings import *
from flask import Flask, flash, render_template, request, session, redirect, send_file, g, Blueprint
bp_chatdiscussion = Blueprint('bp_chatdiscussion',__name__)

#テキスト議論選択ページ
@bp_chatdiscussion.route('/Channelselection_Chat', methods=['GET'])
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

#テキスト議論を選択したら、各議論の状態のページに行くことができる（議論中→評価ページ、議論前→賭けページ、など）
@bp_chatdiscussion.route('/ChannelSetting_Chat/<channel>', methods=['GET'])
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

#継続中に議論の時間を変更するページ。
@bp_chatdiscussion.route('/Discussing_chat_change/<channel>', methods=['GET'])
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

@bp_chatdiscussion.route('/Discussing_chat_change/<channel>', methods=['POST'])
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

#評価ページ
@bp_chatdiscussion.route('/Discussing_Chat', methods=['GET'])
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

@bp_chatdiscussion.route('/Discussing_Chat', methods=['POST'])
def Discussing_Chat_POST():
    log = request.form.get('item')
    print(log)
    return redirect('/')

#評価ページ（最初の評価以外はこのページを使用する。）
@bp_chatdiscussion.route('/hyouka/<number>', methods=['GET'])
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

#賭け対象選択ページ
@bp_chatdiscussion.route('/kake_chat', methods=['GET'])
def kake_chat():
    channel = session['channel']
    name = session['name']
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。################################################

    chan_list = all_worksheet2[:, 1]#シート2のチャンネルリストをとってくる。
    chanNumber = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            chanNumber += 1
        elif i == channel:
            break
    session['chanNumber'] = chanNumber

    starttimestr = all_worksheet2[chanNumber - 1][3]
    finishtimestr= all_worksheet2[chanNumber - 1][4]
    all_worksheet1 = np.array(worksheet1.get_all_values())#worksheet1の全てのログを持ってくる。################################################
    ozzu_list = all_worksheet1[:, 3] #ozzu_listからユーザーのオッズを一次元配列で取得。

    

    kakezyouhou = []

    for i in range(len(all_user)):
        kakezyouhou.append([all_user[i], ozzu_list[i + 2]])#上記の4つの一次元配列を足し合わせて二次元配列にする。

    zibun = all_user.index(name)#賭け対象選択ページで自分の名前を表示させないために配列の何番目が自分なのか取得。
    kakezyouhou.pop(zibun)
 
    point =  int(all_worksheet1[zibun + 2][4])#自分のポイント数を取得
    kakepointlow = point//10#賭けることができる最低ポイント数を取得
    kakepointhigh = kakepointlow*2#賭けることができる最高ポイント数を取得

    kakerange = []
    for p in range(kakepointlow,kakepointhigh + 1):#最低ポイント～最高ポイントで１ずつ配列に入れる。
        kakerange.append(p)
   
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
        
    return render_template('kake_chat.html',
    title='Setting',
    arinasi = "は議論が設定されていますが変更しますか？",
    start = starttimestr,
    finish = finishtimestr,
    channel=channel,
    kakezyouhou = kakezyouhou,
    point = point,
    kakepointlow = kakepointlow,
    kakepointhigh = kakepointhigh,
    kakerange = kakerange,
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
    kakesuu = kakepointhigh -kakepointlow + 1#賭けポイントの数
    )

@bp_chatdiscussion.route('/kake_chat', methods=['POST'])
def kake_chat_POST():
    
    name = session['name']
    chanNumber = session['chanNumber']
    session.pop('chanNumber', None)
    channel = session['channel']
    session.pop(chanNumber,chanNumber)
    print(chanNumber)
    

    #賭け情報の書き込み
    kakeperson = request.form.get('kakeperson')#賭ける対象
    kakepoint = request.form.get('kakepoint')#賭けるポイント数
    zibun = all_user.index(name)#自分の名前の番号取得
    worksheet2.update_cell(chanNumber, (2 * zibun) + 6, kakeperson)#自分が賭けた人を記録###########################################################書き込み
    worksheet2.update_cell(chanNumber, (2 * zibun) + 7, kakepoint)#自分が賭けたポイント数を記録###########################################################書き込み

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペース
    client = WebClient(token)
    #自分のuserID取ってくる
    user_id = all_user_ID[zibun]#評価相手のslackのIDを取ってくる。
    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "chat議論であなたは" + channel + "のお題で" + kakeperson + "に" + kakepoint + "ポイントの賭けを行いました。")
    #評価を通知するプログラム終わり


    return redirect('/Thankyou_Chat')

#議論情報「nasi」から飛んできた場合、議論を設定できる
@bp_chatdiscussion.route('/settingchat', methods=['GET'])
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

@bp_chatdiscussion.route('/settingchat', methods=['POST'])
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

#Thank you言うページ
@bp_chatdiscussion.route('/Thankyou_Chat', methods=['GET'])
def Thankyou_Chat():
    name = session['name']
    print(name)
    channel = session['channel'] 
    session.pop(channel,channel)
    all_worksheet2 = np.array(worksheet2.get_all_values())#worksheet2の全てのログを持ってくる。################################################
    chan_list = all_worksheet2[:, 1]#チャンネルリストを取得
    Number = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    print(Number)
    starttimestr = all_worksheet2[Number - 1][3]#議論の始まりの時間取得
    finishtimestr= all_worksheet2[Number - 1][4]#議論の終わりの時間取得
    zibun = all_user.index(name)#自分の名前の番号取得
    kakeperson = all_worksheet2[Number - 1][(2 * zibun) + 5]#自分が賭けた人を記録
    kakepoint = all_worksheet2[Number - 1][(2 * zibun) + 6]#自分が賭けたポイント数を記録
    
    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('Thankyou_Chat.html',
    channel = channel,
    name = name,
    starttime =starttimestr,
    finishtime = finishtimestr,
    kakeperson = kakeperson,
    kakepoint = kakepoint,
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
    title='Thank you for your cooperation!!')