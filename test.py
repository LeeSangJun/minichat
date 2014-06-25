from flask import Flask, request, url_for, redirect, session,\
     render_template, abort, g, flash
import pusher

app = Flask(__name__)


@app.route("/")
def main():
	return render_template('index.html')

@app.route("/chat", methods=['POST'])
def chat():
	id = request.form['id']
	pwd = request.form['pwd']
	return render_template('pusher_test.html', id=id)

@app.route("/login", methods=['POST'])
def login():
	return render_template('index.html')


@app.route("/trigger")
def trigger():
	p = pusher.Pusher(
	  app_id='79059',
	  key='c87201b48ba8607c7298',
	  secret='280c237409fc6f0f3bc6'
	)

	input = request.args.get('input')
	p['test_channel'].trigger('my_event', {'message': input})

	return ""

if __name__ == "__main__":
	app.run(debug=True)