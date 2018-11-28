from app import app
from lib.relay_switch import RelaySwitch
from flask import render_template, flash, redirect, url_for
from flask_socketio import SocketIO, emit
from app.forms import LoginForm
socketio = SocketIO(app)

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title='Index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@socketio.on('control tub', namespace='/test')
def control_tub(json_obj=None):
        RelaySwitch(gpio_pin=18).on()
        emit('my response', {'data': message['data']})

if __name__ == '__main__':
    socketio.run(app)
