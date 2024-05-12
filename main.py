import json

from flask import Flask, render_template, redirect, request, session, url_for
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8b8e1c38fabc194db7de522c7d736b9e79a9badb'

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
                return redirect(url_for('chats'), code=307)
            case "wrong pass":
                return render_template('login.html', errorMessage = 'Неправильный пароль!')
            case "user not exists":
                return render_template('login.html', errorMessage = 'Такого пользователя не существует!')



    if request.method == "GET":
        return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template('register.html')

    username = request.form.get("username")
    phone = request.form.get("phone")
    password = request.form.get("password")

    isUsernameInt = False
    try:
        int(username)
        isUsernameInt = True
    except:
        pass

    if isUsernameInt:
        return render_template('register.html', errorMessage="Имя пользователя должно содержать буквы!")

    data = {
        "phone": phone,
        "username": username
    }

    req = requests.post("http://127.0.0.1:1232/api/possibleToReg", data=data).json()['status']

    match req:
        case "OK":

            userdata = {
                "username": username,
                "phone": phone,
                "password": password
            }

            session['userdata'] = userdata

            return redirect("/phone-confirm")
        case "username exists":
            return render_template('register.html', errorMessage="Имя пользователя занято!")
        case "phone exists":
            return render_template('register.html', errorMessage="Номер телефона занят!")


@app.route('/phone-confirm', methods=["POST", "GET"])
def phcon():
    if request.method == "GET":

        if not 'userdata' in session:
            return render_template('login.html', errorMessage="INVALID SESSION!")

        userIP = -1
        code = requests.get(f"http://127.0.0.1:1232/api/voicecode?userIP={userIP}&userPhone=str({session['userdata']['phone']})").json()['code']


        session['voicecode'] = code


        return render_template('phone-confirm.html', userdata=session['userdata'])


    inputCode = request.form.get("code")



    if str(inputCode) == str(session['voicecode']):

        data = {
            "phone": session['userdata']['phone'],
            "username": session['userdata']['username'],
            "password": session['userdata']['password']
        }


        reg_status = requests.post("http://127.0.0.1:1232/api/register", data=data).json()['status']

        if reg_status == "OK":
            return redirect(url_for('chats'), code=307)


    return render_template('phone-confirm.html', errorMessage="Неверный код!", userdata=session['userdata'])


@app.route("/sms-confirm", methods=["POST","GET"])
def smscon():
    if request.method=="GET":

        if not "userdata" in session:
            return render_template('login.html',erorMessage='INVALID SESSION')

        code = requests.get(f"http://127.0.0.1:1232/api/textcode?userPhone=str({session['userdata']['phone']})").json()['code']


        session['textcode']=code

        return render_template('sms-confirm.html', userdata=session['userdata'])

    inputCode=request.form.get("code")


    if str(inputCode) == str(session['textcode']):

        data={
             "phone": session['userdata']['phone'],
             "username": session['userdata']['username'],
             "password": session['userdata']['password']
        }

        reg_status = requests.post("http://127.0.0.1:1232/api/register", data=data).json()['status']

        if reg_status == "OK":
            return redirect(url_for('chats'), code=307)


    return render_template('sms-confirm.html', errorMessage="Неверный код!", userdata=session['userdata'])



@app.route("/chats", methods=['POST', 'GET'])
def chats():
    # if request.method == "GET":
    #     return redirect('login')
    #
    #
    # phone = request.form.get('phone')
    # if phone == None:
    #     phone = session['userdata']['phone']
    #
    # session.clear()
    #
    # data = {
    #     "phone": phone
    # }
    #
    #
    # username = requests.post("http://127.0.0.1:1232/api/getUsernameByPhone", data={"phone": phone}).json()
    #
    # req = requests.post("http://127.0.0.1:1232/api/getdialogs", data=data).json()

    username = {
        "username": "verstka"
    }

    req = ['chat1', 'chat2', 'chat3']

    return render_template('chats.html', username=username['username'], chatlist=req)



if __name__ == "__main__":
    app.run(debug=True, port=5050)