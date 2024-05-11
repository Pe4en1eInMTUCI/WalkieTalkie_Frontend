from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
@app.route("/login")
def root():
    return render_template('login.html')

@app.route("/register")
def reg():
    return render_template('register.html')


@app.route('/phoneconfirm')
def phcon():
    return render_template('phone-confirm.html')

@app.route("/smsconfirm")
def smscon():
    return render_template('sms-confirm.html')


@app.route("/chats")
def chats():

    data = {
        "username": "pe4en1e"
    }

    req = requests.post("http://127.0.0.1:1232/api/getdialogs", data=data).json()

    return render_template('chats.html', chatlist=req)


if __name__ == "__main__":
    app.run(debug=True, port=5050)