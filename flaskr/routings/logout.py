#ログアウトのため
# logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('name', None)
    session.pop('login',None)
    session.pop('id',None)
    return redirect('/Login')