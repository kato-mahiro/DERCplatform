#DBへの書き込みの例(上のmodel classもいるよ)
@app.route('/sample2aaa', methods=['GET'])
def sample2aaa():
    name = "ccc"
    mail = "ddd"
    age = "33"
    id = 12
    Session = sessionmaker(bind = engine)
    ses = Session()
    mydata = ses.query(Mydata).filter(Mydata.id == id).one()
    mydata.name = name
    mydata.mail = mail
    mydata.age = int(age)
    ses.add(mydata)
    ses.commit()
    ses.close()
    return render_template('sample.html', 
        title='Index', 
        message='※SQLite3 Databaseaaa',
        alert='This is SQLite3 Database Sample!',
        )
