#ビデオ議論に関連するページ
from utils import *
from global_settings import *
from flask import Flask, flash, render_template, request, session, redirect, send_file, g, Blueprint
bp_webdiscussion = Blueprint('bp_webdiscussion',__name__)

#ビデオ議論選択ページ
@bp_webdiscussion.route('/Channelselection_web', methods=['GET'])
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
#議論情報「nasi」から飛んできた場合
@bp_webdiscussion.route('/ChannelSetting_Web', methods=['GET'])
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
@bp_webdiscussion.route('/ChannelSetting_Web', methods=['POST'])
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
#議論を選択したら、各議論の状態のページに行くことができる（議論中→評価ページ、議論前→賭けページ、など）
@bp_webdiscussion.route('/Discussing_Web/<channel>', methods=['GET'])
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
        return redirect('/finish')#web評価の作業（評価を実行後/webdiscussをredirectする。）
@bp_webdiscussion.route('/Discussing_Web2/<hyouka>', methods=['GET'])
def Discussing_Web2(hyouka):
#スプレッドシートに保存する用プログラム始まり
    name = session['name']#評価の欄に書き込む自分の名前を取ってくる。
    channel = session['channel']
    # チャンネルIDとチャンネル名を合わせる。
    discussNo = session['discussNo'] 
    webinfo = workbook_webdiscuss.worksheet(discussNo)################################################
    all_webinfo = np.array(webinfo.get_all_values())#webchanの全てのログを持ってくる。################################################
    discususer_list = all_user

    #評価した相手の行の処理(uNumber=評価相手の番号、mNumber=自分の番号)
    uNumber  = discususer_list.index(hyouka)#評価する相手の名前を見つけてくる。
    hihyoukacount =  all_webinfo[uNumber, 2]#評価される相手の批評価回数##
    
    ###以下、スプレッドシートへの書き込み###
    webinfo.update_cell(uNumber +1, (int(hihyoukacount)*2) + 8, name)#自分の名前を書き込む################################################書き込み
    now = datetime.datetime.now()
    webinfo.update_cell(uNumber+1, (int(hihyoukacount)*2) + 7, (str(now.hour) +':'+  str(now.minute)))#評価した時間を書き込むjson.dumps(now.hour, default=support_datetime_default)################################################書き込み
    ###スプレッドシートへの書き込み終わり###

    ###以下、DBへの書き込み###
    # model class
    class hyoukaDB(Base):
      __tablename__ = discussNo
      __table_args__ = {'extend_existing': True}
      id = Column(Integer, primary_key=True)
      actionfinishtime = Column(String(255))
      for oo in range(1,48):#hihyouka?にColumn(String(255))を入れまくる。
        exec_command = 'hihyouka' + str(oo) + '= Column(String(255))'
        exec(exec_command)


    # get Dict data
    def toDict(self):
        return {
            'id':int(self.id), 
            'actionfinishtime':str(self.actionfinishtime),
            'hihyouka1':str(self.actionfinishtime),
            'hihyouka2':str(self.actionfinishtime),
            'hihyouka3':str(self.actionfinishtime),
            'hihyouka4':str(self.actionfinishtime),
            'hihyouka5':str(self.actionfinishtime),
            'hihyouka6':str(self.actionfinishtime),
            'hihyouka7':str(self.actionfinishtime),
            'hihyouka8':str(self.actionfinishtime),
            'hihyouka9':str(self.actionfinishtime),
            'hihyouka10':str(self.actionfinishtime),
            'hihyouka11':str(self.actionfinishtime),
            'hihyouka12':str(self.actionfinishtime),
            'hihyouka13':str(self.actionfinishtime),
            'hihyouka14':str(self.actionfinishtime),
            'hihyouka15':str(self.actionfinishtime),
            'hihyouka16':str(self.actionfinishtime),
            'hihyouka17':str(self.actionfinishtime),
            'hihyouka18':str(self.actionfinishtime),
            'hihyouka19':str(self.actionfinishtime),
            'hihyouka20':str(self.actionfinishtime),
            'hihyouka21':str(self.actionfinishtime),
            'hihyouka22':str(self.actionfinishtime),
            'hihyouka23':str(self.actionfinishtime),
            'hihyouka24':str(self.actionfinishtime),
            'hihyouka25':str(self.actionfinishtime),
            'hihyouka26':str(self.actionfinishtime),
            'hihyouka27':str(self.actionfinishtime),
            'hihyouka28':str(self.actionfinishtime),
            'hihyouka29':str(self.actionfinishtime),
            'hihyouka30':str(self.actionfinishtime),
            'hihyouka31':str(self.actionfinishtime),
            'hihyouka32':str(self.actionfinishtime),
            'hihyouka33':str(self.actionfinishtime),
            'hihyouka34':str(self.actionfinishtime),
            'hihyouka35':str(self.actionfinishtime),
            'hihyouka36':str(self.actionfinishtime),
            'hihyouka37':str(self.actionfinishtime),
            'hihyouka38':str(self.actionfinishtime),
            'hihyouka39':str(self.actionfinishtime),
            'hihyouka40':str(self.actionfinishtime),
            'hihyouka41':str(self.actionfinishtime),
            'hihyouka42':str(self.actionfinishtime),
            'hihyouka43':str(self.actionfinishtime),
            'hihyouka44':str(self.actionfinishtime),
            'hihyouka45':str(self.actionfinishtime),
            'hihyouka46':str(self.actionfinishtime),
            'hihyouka47':str(self.actionfinishtime),
            'hihyouka48':str(self.actionfinishtime),
        }
    Session = sessionmaker(bind = engine)
    ses = Session()
    hyoukasubject = ses.query(hyoukaDB).filter(hyoukaDB.id == uNumber + 1).one()##評価する相手のidを入れる。
    print(uNumber)
    hyoukasubject.actionfinishtime = 1##actionの部分を1に変える。
    hihyoukacount_DB = int(hihyoukacount) + 1
    exec_code = 'hyoukasubject.hihyouka' + str(hihyoukacount_DB) + '='  + '"' + str(now.hour) + '時' + str(now.minute) + '分' +'"' ##相手の評価の部分に時間を記入する。
    exec(exec_code)
    hyoukasubject.actionfinishtime = "1"##actionを1にして評価されたという」記録を残す。
    ses.add(hyoukasubject)
    ses.commit()
    ses.close()

    ###DBの書き込み終わり###

    #評価された回数を数えてその時間を表示させるための処理
    print(discususer_list)
    mNumber = discususer_list.index(name)
    hihyoukanum =  all_webinfo[mNumber, 2]



    return redirect('/webdiscuss')#継続中に議論の時間を変更するページ。
@bp_webdiscussion.route('/Discussing_web_change/<channel>', methods=['GET'])
def Discussing_web_change(channel):
    channel = session['channel']
    name = session['name']
    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    chan_list = all_webchan[:, 1]#シート2のチャンネルリスト全体をとってくる。
    
    chanNum = 0
    for aaa in chan_list:#チャンネルが配列の中の何番目なのかを検索する。
        if aaa != channel:
            chanNum = chanNum + 1
        else:
            break  
    finish = all_webchan[chanNum , 5]#終了時刻の取得
    session['chanNum'] = chanNum#GETとPOSTの間だけ保持

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('Discussing_change.html',
    channel = channel,
    finish = finish,
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
    title='Ending time')

@bp_webdiscussion.route('/Discussing_web_change/<channel>', methods=['POST'])
def Discussing_web_change_POST(channel):
    discussionfinishdate = request.form.get('discussionfinishdate')#終了
    discussionfinishtime = request.form.get('discussionfinishtime')

    chanNum = session['chanNum']#GETとPOSTの間だけ保持
    session.pop('chanNum',None)

    discussionfinish = discussionfinishdate +" " +discussionfinishtime
    webchan.update_cell(chanNum + 1, 6, discussionfinish)################################################

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペーす
    client = WebClient(token)
    #評価するチャンネルのID取ってくる
    chan_id ="C022UPX11FB"##web議論おしらせチャンネル

    # DMを送信する
    client.chat_postMessage(channel= chan_id, text= channel + "の終了時刻が" +  discussionfinish + "に変更されました。")
    #評価を通知するプログラム終わり

    return redirect('/webdiscuss')#終了した議論に自分が関わっていたら成績が見れる。関わっていなかったらあなたはこの議論に参加していません。的なページを出す。
@bp_webdiscussion.route('/finish', methods=['GET'])
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
        title='Result')#賭け対象選択ページ
@bp_webdiscussion.route('/kake_web', methods=['GET'])
def kake_web():
    channel = session['channel']
    name = session['name']

    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    all_worksheet1 = np.array(worksheet1.get_all_values())#webinfoの全てのログを持ってくる。################################################
    chan_list =all_webchan[:, 1]#チャンネルリストを取得
    Number = 1
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break

    starttimestr = all_webchan[Number - 1, 4]
    ozzu_list = all_worksheet1[:, 3] #ozzu_listからユーザーのオッズを一次元配列で取得。##
  

    kakezyouhou = []

    for i in range(len(all_user)):
        kakezyouhou.append([all_user[i], ozzu_list[i + 2]])#上記の4つの一次元配列を足し合わせて二次元配列にする。

    zibun = all_user.index(name)#賭け対象選択ページで自分の名前を表示させないために配列の何番目が自分なのか取得。
    kakezyouhou.pop(zibun)

    point =  int(all_worksheet1[zibun + 2, 4])#自分のポイント数を取得##
    kakepointlow = point//10#賭けることができる最低ポイント数を取得
    kakepointhigh = kakepointlow*2#賭けることができる最高ポイント数を取得

    kakerange = []
    for p in range(kakepointlow,kakepointhigh + 1):#最低ポイント～最高ポイントで１ずつ配列に入れる。
        kakerange.append(p)

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。    

    return render_template('kake_web.html',
    title='Setting',
    arinasi = "は議論が設定されていますが変更しますか？",
    start = starttimestr,
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

#賭け対象選択後ページ
@bp_webdiscussion.route('/kake_web', methods=['POST'])
def kake_web_POST():
    
    name = session['name']
    channel = session['channel']
    chan_list =webchan.col_values(2)#チャンネルリストを取得################################################
    Number = 0
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    

    #賭け情報の書き込み
    kakeperson = request.form.get('kakeperson')#賭ける対象
    kakepoint = request.form.get('kakepoint')#賭けるポイント数
    zibun = all_user.index(name)#自分の名前の番号取得
    webchan.update_cell(Number + 1, (2 * zibun) + 7, kakeperson)#自分が賭けた人を記録################################################
    webchan.update_cell(Number + 1, (2 * zibun) + 8, kakepoint)#自分が賭けたポイント数を記録################################################

    #評価を通知するプログラム始まり
    token = "設定してください"# ワークスペース
    client = WebClient(token)
    #自分のuserID取ってくる
    user_id = all_user_ID[zibun]#評価相手のslackのIDを取ってくる。
    # DMを開き，channelidを取得する．
    res = client.conversations_open(users=user_id)
    dm_id = res['channel']['id']

    # DMを送信する
    client.chat_postMessage(channel=dm_id, text= "オンライン議論であなたは" + channel + "のお題で" + kakeperson + "に" + kakepoint + "ポイントの賭けを行いました。")
    #評価を通知するプログラム終わり

    return redirect('/Thankyou_web')
#Thank youと言うページ
@bp_webdiscussion.route('/Thankyou_web', methods=['GET'])
def Thankyou_web():
    name = session['name']
    channel = session['channel'] 
    session.pop(channel,channel)
    ############################
    all_webchan = np.array(webchan.get_all_values())#webchanの全てのログを持ってくる。################################################
    chan_list =all_webchan[:, 1]#チャンネルリストを取得
    Number = 0
    for i in chan_list:#チャンネルが何行目にあるか確認して行数をNumberに代入
        if i != channel:
            Number += 1
        elif i == channel:
            break
    starttimestr = all_webchan[Number, 4]#議論の始まりの時間取得##
    print(Number)
    print(chan_list)
    zibun = all_user.index(name)#自分の名前の番号取得
    kakeperson = all_webchan[Number , (2 * zibun) + 6]#自分が賭けた人を記録##
    kakepoint = all_webchan[Number, (2 * zibun) + 7]#自分が賭けたポイント数を記録##
    if kakepoint != " ":#賭けがあれば「1」無ければ「0」
        kakezyouhou = 0

    else:
        kakezyouhou = 1

    id = session['id']
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。

    return render_template('Thankyou_web.html',
    channel = channel,
    name = name,
    starttime =starttimestr,
    kakeperson = kakeperson,
    kakepoint = kakepoint,
    kakezyoukyou = kakezyouhou,
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
##web議論を行うページ（評価した後もこのページをリダイレクトしている。）
##やっていること：DBから自分の行を取り出して被評価の時間を出している。
##そして、評価されていたら（actionが1になっていたら）、HTMLに評価されたよという表示を出し、actionfinishtimeを0に戻す。）
@bp_webdiscussion.route('/webdiscuss', methods=['GET'])
def webdiscuss():
    channel = session['channel']
    discussNo = session['discussNo']
    nam = session['login']
    Number = 0
    name = session['name']
    hyoukalist = []
    db = get_db()
    id_DB = all_user.index(name) +1
    print(id_DB)
    print(discussNo)
    cur_me = db.execute("select * from {discussNo} where id = {id_DB}".format(id_DB = id_DB, discussNo = discussNo))##DBの中の自分の情報を取得しておく
    hyoukalist = cur_me.fetchall()
    cur_test = db.execute("select * from {discussNo} where id = 11 ".format(discussNo = discussNo))##DBの中の(test)の情報を取得（議論の情報を取得）しておく
    discuss_info = cur_test.fetchall()
    ###以下、参加している人と、自分以外票がボタンを表示しないようにする。###
    userlist = []
    for par in range(1,11):
        cur_par = db.execute("select * from {discussNo} where id = {par}".format(par = par, discussNo = discussNo))##DBの中の各被験者の情報を取得
        user_DB = cur_par.fetchall()
        if user_DB[0][3] == "1":
            userlist.append(user_DB[0][0])
            user_DB.clear()
    if hyoukalist[0][0] in userlist:
        userlist.remove(hyoukalist[0][0])###最後に自分の名前を削除する。
    ###参加している人と、自分以外票がボタンを表示しないようにする。終わり###
    close_db()##コードがくちゃくちゃ過ぎるが一度、データベースの接続を終了（これがないとエラーになるため。）

    #配列中のNoneを全て消す。
    hyoukalist_filtered = []
    for ppp in range(48):
        if hyoukalist[0][ppp] is not None:
            hyoukalist_filtered.append(hyoukalist[0][ppp])
        else:
            pass

    #最初の二つ（nameとidを消す）
    hyoukalist_filtered.pop(0)
    hyoukalist_filtered.pop(0)
    action = hyoukalist_filtered[0]##自分が評価されたかどうかを格納
    hyoukalist_filtered.pop(0)#actionfinishtimeを消す。
    hyoukalist_filtered.pop(0)#participantを消す。

    ##もしactionfinishtimeが1だったら（自分が評価されていたら）0に変える。
    if action == "1":
        # model class（DB書き込み用）
        class actionDB(Base):
          __tablename__ = discussNo
          __table_args__ = {'extend_existing': True}
          id = Column(Integer, primary_key=True)
          actionfinishtime = Column(String(255))

         # get Dict data
        def toDict(self):

            return {
                'id':int(self.id), 
                'actionfinishtime':str(self.actionfinishtime)
            }
         
        Session = sessionmaker(bind = engine)
        ses = Session()
        mydata = ses.query(actionDB).filter(actionDB.id == id_DB).one()
        mydata.actionfinishtime = 0
        ses.add(mydata)
        ses.commit()
        ses.close()

    ##もしtestのparticipantが1だったら（参加者リストが更新されていなかったら）参加者リストを更新して0に変える。
    if discuss_info[0][3] == "1":
        webinfo = workbook_webdiscuss.worksheet(discussNo)################################################
        all_webinfo = np.array(webinfo.get_all_values())#webchanの全てのログを持ってくる。################################################
        # model class（DB書き込み用）
        class participantDB(Base):
          __tablename__ = discussNo
          id = Column(Integer, primary_key=True)
          participant = Column(String(255))

        # get Dict data
        def toDict(self):
            return {
                'id':int(self.id), 
                'participant':str(self.participant)
            }
        Session = sessionmaker(bind = engine)
        ses = Session() 

        for ll in range(1,11):
            if all_webinfo[32][2 + ll] in all_user:#
                mydata = ses.query(participantDB).filter(participantDB.id == ll).one()
                mydata.participant = 1
                ses.add(mydata)

        mydata = ses.query(participantDB).filter(participantDB.id == 11).one()
        mydata.participant = 0
        ses.add(mydata)
        
        ses.commit()
        ses.close()

    id = session['id']
    updateBadgeinfo(id)
    Badgeinfo = getBadgeinfo(id)#バッヂの情報を取得する関数の呼び出し。
        
    return render_template('Discussing_Web.html', 
    channel = channel,
    userlist = userlist, 
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
    hyoukalist = hyoukalist_filtered,
    action = action,

    name = name,)  # 議論が始まっているのでDiscussing_Web.htmlを表示。