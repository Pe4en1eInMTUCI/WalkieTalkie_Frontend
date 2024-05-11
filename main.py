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

        print(req)

        match req:
            case "OK":
                return redirect(url_for('chats'), code=307)
            case "wrong pass":
                return render_template('login.html', errorMessage = 'Неправильный пароль!')
            case "user not exists":
                return render_template('login.html', errorMessage = 'Такого пользователя не существует!')


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


@app.route("/chats", methods=['POST', 'GET'])
def chats():
    if request.method == "GET":
        return redirect('login')


    phone = request.form.get('phone')

    data = {
        "phone": phone
    }

    username = requests.post("http://127.0.0.1:1232/api/getUsernameByPhone", data={"phone": phone}).json()

    print(username)

    req = requests.post("http://127.0.0.1:1232/api/getdialogs", data=data).json()

    return render_template('chats.html', username=username['username'], chatlist=req)



if __name__ == "__main__":
    app.run(debug=True, port=5050)