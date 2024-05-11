import json

from flask import Flask, render_template, redirect, request, session, url_for
import requests

app = Flask(__name__)

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        data = {
            "phone": phone,
            "password": password
        }

        req = requests.post("http://127.0.0.1:1232/api/login", data=data).json()['status']

        match req:
            case "OK":
                return redirect(url_for('/chats', phone=phone))
            case "wrong password":
                pass
            case "user not exists":
                pass


        return render_template('login.html')
    if request.method == "GET":
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


@app.route("/chats", methods=['POST'])
def chats():

    phone = request.form.get("phone")

    data = {
        "phone": phone
    }

    req = requests.post("http://127.0.0.1:1232/api/getdialogs", data=data).json()

    return render_template('chats.html', chatlist=req)



if __name__ == "__main__":
    app.run(debug=True, port=5050)