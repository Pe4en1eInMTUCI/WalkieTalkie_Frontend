from flask import Flask, render_template

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
    return render_template('chats.html')


if __name__ == "__main__":
    app.run(debug=True, port=5050)