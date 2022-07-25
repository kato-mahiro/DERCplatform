#web評価の作業（評価を実行後/webdiscussをredirectする。）
@app.route('/Discussing_Web2/<hyouka>', methods=['GET'])
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



    return redirect('/webdiscuss')