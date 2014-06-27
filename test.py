from flask import Flask, request, url_for, redirect, session,\
     render_template, abort, g, flash
from google.appengine.ext import ndb    
import pusher

app = Flask(__name__)
app.secret_key = 'likelionMJU'

class room_info(ndb.Model):
    host = ndb.StringProperty()
    user_count = ndb.IntegerProperty()

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/login", methods=['POST'])
def log_in():
	id = request.form['id']
	pwd = request.form['pwd']
	session["user_id"] = id
	return redirect(url_for('dashboard'))

@app.route("/dashBoard")
def dashboard():
	roomlist = room_info.query().fetch()
	for room in roomlist:
		print room.host
	return render_template('main.html', id = session["user_id"], rooms = roomlist)


@app.route("/makeRoom")
def makeroom():
	room = room_info()
	room.host = session["user_id"]
	room.user_count = 1 #Usercount = 1
	session["host"] = session["user_id"]
	room.put()
	return redirect(url_for('chatRoom', host = session["host"]))


@app.route("/joinChat")
def joinchat():
	room_host = request.args.get('host')
	session["host"] = room_host

	#room userCount increase
	rooms = room_info.query(room_info.host==room_host).fetch(1)
	if(len(rooms) > 0):
		for room in rooms:
			chatRoom = room.key.get()
			chatRoom.user_count = chatRoom.user_count+1
			chatRoom.put()
	
		return redirect(url_for('chatRoom',host = room_host))
	else:
		return redirect(url_for('dashboard'))


@app.route('/<host>')
def chatRoom(host):
	return render_template('chatRoom.html', host = session["host"])


@app.route("/sendMsg")
def send_messege():
	p = pusher.Pusher(
	  app_id='79059',
	  key='c87201b48ba8607c7298',
	  secret='280c237409fc6f0f3bc6'
	)

	chat_host = session["host"]
	input = request.args.get('input')
	p[chat_host].trigger('msg', {'message': input})
	return ""

@app.route("/chatOut")
def chatout():
	rooms = room_info.query(room_info.host==session["host"]).fetch(1)
	for room in rooms:
		chatRoom = room.key.get()
		chatRoom.user_count = chatRoom.user_count-1
		if chatRoom.user_count == 0:
			room.key.delete()
		else:
			chatRoom.put()

	return redirect(url_for('dashboard'))


if __name__ == "__main__":
	app.run(debug=True)