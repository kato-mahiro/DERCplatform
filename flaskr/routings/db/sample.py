#DBからの読み取りの例
@app.route('/sample', methods=['GET'])
def sample():
    mydata = []
    db = get_db()
    testtesttest = 4
    cur = db.execute("select * from mydata where id = {testtesttest}".format(testtesttest = testtesttest))
    mydata = cur.fetchall()
    return render_template('sample.html', 
        title='Index', 
        message='※SQLite3 Database',
        alert='This is SQLite3 Database Sample!',
        data=mydata)