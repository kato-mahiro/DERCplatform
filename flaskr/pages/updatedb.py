@app.route('/UpdateDB', methods=['GET'])
def UpdateDB_GET():
    UpdateDB()

    return render_template('UpdateDB.html')