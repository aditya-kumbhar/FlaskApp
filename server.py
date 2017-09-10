from flask import Flask, render_template,request,g,flash,redirect,url_for,jsonify,json
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
			return jsonify(result='User-id already exists! Please choose a different User-id.')

		else:
			g.db.execute("INSERT INTO Users VALUES (?,?,?,?,?,?);", (uid,passw,name,email,phone,city))
			g.db.commit()
			return jsonify(result='Signup successful! Now login with your new User-id.')
			
			
#clicking on Login
@app.route('/login',methods=['GET', 'POST'])
def login():
	if(request.method=='POST'):
		uid = request.form['uid']
		passw = request.form['pass']

		li = g.db.execute("SELECT pass from Users WHERE uid = ?;",[uid]).fetchall();
		nm = g.db.execute("SELECT uname from Users WHERE uid = ?;",[uid]).fetchall();
		
		if(len(li)==0):
			flash("Invalid User-id")
			return redirect(url_for('index'))
			# return jsonify(result="Invalid login id")
		else:
			if(str(passw)==str(li[0][0])):
				return render_template('choice.html',data = str(nm[0][0]))
			else:
				flash("Incorrect password")
				return redirect(url_for('index'))
			


@app.route('/choice')
def manageHall():
	return redirect(url_for('choice'))

		
if __name__ == '__main__':
  app.run(host= '0.0.0.0', port=5000, debug=True)
#host= '0.0.0.0', port=5000,
