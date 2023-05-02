from flask import Flask, request, redirect, render_template, session, url_for
import logging
import utils

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/apache2/myapp.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/')
def root():
    app.logger.info("this is a info log")
    utils.create_music_table()
    utils.load_music()
    utils.create_login_table()
    utils.load_login_data()
    return render_template(
        'login.html')


@app.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    user = utils.validate_user(email, password)
    # If the query returned one user entity, redirect to the dashboard
    if user:
        session['email'] = email
        session['user_name'] = user['user_name']
        resp = redirect(url_for('forum'))
        return resp
    # If the query returned no or multiple user entities, show an error message
    else:
        error_msg = 'ID or password is invalid'
        return render_template('login.html', error_msg=error_msg)


@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        # retrieve the entered values from the form
        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        if utils.is_email_exist(email):
            error_message = 'The email already exists'
            return render_template('register.html', error_msg=error_message)

        utils.insert_user(email, user_name, password)
        return redirect(url_for('login'))


@app.route('/forum', methods=['GET', "POST"])
def forum():
    user_name = session.get("user_name")
    return render_template("forum.html", user_name=user_name)
    return redirect(url_for("login"))


@app.route('/logout', methods=['GET', 'POST'])
def logout_():
    del session['email']
    del session['user_name']
    return redirect('/login')


if __name__ == '__main__':
    app.run()
