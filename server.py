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

@app.route('/searchHalls',methods=['POST'])
def searchHalls():
	if(request.method=='POST'):
		
		city = request.form['hallcity']
		no_of_seats = (request.form['seats'])
		
		ac = request.form['ac']
		sb = request.form['sb']
		pr = request.form['pr']
		a=1
		s=1
		p=1
		li=[]

		if(no_of_seats==''):
			no_of_seats=0
		else:
			no_of_seats=int(no_of_seats)

		if(ac==""):
			a=0
		if(sb==""):
			s=0
		if(pr==""):
			p=0
		

		if(city=='City'):
			li = g.db.execute("SELECT r_name,loc,seats from Rooms WHERE seats >= ? and ac = ? and sb = ? and prj = ?;",(no_of_seats,a,s,p)).fetchall()
		else:
			li = g.db.execute("SELECT r_name,loc,seats from Rooms WHERE city = ? and seats >= ? and ac = ? and sb = ? and prj = ?;",(city,no_of_seats,a,s,p)).fetchall()
		
		return jsonify(list=li)



		
if __name__ == '__main__':
  app.run(host= '0.0.0.0', port=5000, debug=True)
#host= '0.0.0.0', port=5000,
