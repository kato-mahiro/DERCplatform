##web議論を行うページ（評価した後もこのページをリダイレクトしている。）
##やっていること：DBから自分の行を取り出して被評価の時間を出している。
##そして、評価されていたら（actionが1になっていたら）、HTMLに評価されたよという表示を出し、actionfinishtimeを0に戻す。）
@app.route('/webdiscuss', methods=['GET'])
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