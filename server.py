from flask import Flask, render_template,request,g,flash,redirect,url_for,jsonify
import sqlite3

#initialising app
app = Flask(__name__)
app.secret_key = 'some_secret'

#connecting to DB before every request
@app.before_request
def before_request():
    g.db = sqlite3.connect('usersDB.db')

#closing connection after every request
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def test():
	if(request.method=='POST'):
		uid = request.form['sp_uid']
		passw = request.form['sp_pass']
		name = request.form['uname']
		email = request.form['email']
		phone = request.form['cell']
		city = request.form['city']

		li = g.db.execute("SELECT * from Users WHERE uid = ?;",[uid]).fetchall();

		if(len(li)>0):
			flash("User-id already exists!")
			return redirect(url_for('index'))
			# return jsonify(result='User-id already exists!')
		else:
			g.db.execute("INSERT INTO Users VALUES (?,?,?,?,?,?);", (uid,passw,name,email,phone,city))
			g.db.commit()
			flash("User-id already exists!")
			return redirect(url_for('index'))

#clicking on Login
@app.route('/login',methods=['GET', 'POST'])
def login():
	if(request.method=='POST'):
		uid = request.form['uid']
		passw = request.form['pass']

		li = g.db.execute("SELECT pass from Users WHERE uid = ?;",[uid]).fetchall();

		if(len(li)==0):
			return jsonify(result="Invalid login id")


#clicking on "manage your hall"
@app.route('/mgHall')
def manageHall():
	return render_template('choice.html')


@app.route('/examp')
def dyn_txt():
    str = 'hello123'
    return jsonify(result='okokok')

		
if __name__ == '__main__':
  app.run(host= '0.0.0.0', port=5000)#,debug=False)
#host= '0.0.0.0', port=5000,
