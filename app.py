from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import models
from database_config import db, app
from forms import EditForm, AddForm, RegisterForm, LoginForm
from user import User

bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users_in_process = []


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if current_user.user_lvl == 3:
                    return redirect(url_for('load_entrance_page'))
                return redirect(url_for('home'))
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = models.User(username=form.username.data, name=form.name.data, surname=form.surname.data,
                               midname=form.midname.data, user_lvl=3, password=hashed_password, email=form.email.data,
                               phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/home')
@login_required
def home():
    active_users = []
    if current_user.user_lvl == 3:
        for i in users_in_process:
            if i.is_ready == True and i.user_lvl == 2:
                active_users.append(i)
        for i in users_in_process:
            if i.id == current_user.id:
                for j in users_in_process:
                    if j.connected_id == current_user.id:
                        return render_template('home.html', current_user=current_user, users=active_users,
                                               is_ready=i.is_ready, gate=i.gate,
                                               connected_user=j.name + " " + j.surname, connected_id=0)
                return render_template('home.html', current_user=current_user, users=active_users, is_ready=i.is_ready,
                                       gate=i.gate)
    elif current_user.user_lvl == 2:
        for i in users_in_process:
            if i.is_ready == True and i.user_lvl == 3:
                active_users.append(i)
        for i in users_in_process:
            if i.id == current_user.id:
                for j in users_in_process:
                    if j.connected_id == current_user.id:
                        return render_template('home.html', current_user=current_user, users=active_users,
                                               is_ready=i.is_ready, gate=i.gate,
                                               connected_user=j.name + " " + j.surname, connected_id=0)
                return render_template('home.html', current_user=current_user, users=active_users, is_ready=i.is_ready)
    return render_template('home.html', current_user=current_user, users=active_users, is_ready=False)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username, name=current_user.name,
                           surname=current_user.surname, midname=current_user.midname, user_lvl=current_user.user_lvl)


@app.route('/home/take<index>', methods=['GET', 'POST'])
@login_required
def load_take_page(index):
    for i in users_in_process:
        if i.id == int(index):
            i.connected_id = current_user.id
            i.in_process = True
        if i.id == current_user.id:
            i.connected_id = int(index)
            i.in_process = True
    return redirect(url_for('home'))

@app.route('/home/cancel', methods=['GET', 'POST'])
@login_required
def load_cancel_page():
    temp = 0;
    for i in users_in_process:
        if i.id == current_user.id:
            temp = i.connected_id
            i.connected_id = 0
            i.in_process = False
            for j in users_in_process:
                if j.id == temp:
                    j.connected_id = 0
                    j.in_process = False
    return redirect(url_for('home'))

@app.route('/admin/del<index>/', methods=['POST'])
@login_required
def admin_del(index):
    user = db.session.query(models.User).get(index)
    db.session.delete(user)
    db.session.commit()
    users = models.User.query.all()
    return render_template('admin.html', id=current_user.id, name=current_user.username, users=users)


@app.route('/admin')
@login_required
def admin():
    if current_user.user_lvl == 0:
        users = models.User.query.all()
        return render_template('admin.html', name=current_user.username, users=users)
    return render_template('home.html', FIO=current_user.name + ' ' + current_user.midname,
                           username=current_user.username, name=current_user.name, surname=current_user.surname,
                           midname=current_user.midname, user_lvl=current_user.user_lvl)


@app.route('/admin/edit<index>/', methods=['GET', 'POST'])
@login_required
def load_edit_page(index):
    user = db.session.query(models.User).get(index)
    form = EditForm()
    form.name.data = user.name
    form.surname.data = user.surname
    form.midname.data = user.midname
    form.username.data = user.username
    form.email.data = user.email
    form.phone.data = user.phone
    form.lvl.data = user.user_lvl
    return render_template('edit.html', form=form, id=index)


@app.route('/home/entrance', methods=['GET', 'POST'])
@login_required
def load_entrance_page():
    counter = 0
    if users_in_process.__len__() == 0:
        add_user(False)
    for i in users_in_process:
        if i.id != current_user.id:
            counter += 1
            if counter == users_in_process.__len__():
                add_user(False)
    return render_template('entrance.html')


@app.route('/home/entrance<index>', methods=['GET', 'POST'])
@login_required
def set_gate(index):
    for i in users_in_process:
        if i.id == current_user.id:
            i.gate = index
    return redirect(url_for('home'))


@app.route('/saving<index>', methods=['GET', 'POST'])
@login_required
def save_changes(index):
    form = EditForm()
    if form.validate_on_submit():
        user = db.session.query(models.User).get(index)
        user.name = form.name.data
        user.midname = form.midname.data
        user.surname = form.surname.data
        user.username = form.username.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.user_lvl = form.lvl.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = models.User(username=form.username.data, name=form.name.data, surname=form.surname.data,
                               midname=form.midname.data, user_lvl=3, password=hashed_password, phone=form.phone.data,
                               email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('add.html', form=form)


@app.route('/change', methods=['GET', 'POST'])
@login_required
def change_status():
    counter = 0
    if users_in_process.__len__() == 0:
        add_user(True)
    else:
        for i in users_in_process:
            if current_user.id == i.id and i.is_ready == False:
                i.is_ready = True
            elif current_user.id == i.id and i.is_ready == True:
                i.is_ready = False
    for i in users_in_process:
        if i.id != current_user.id:
            counter += 1
            if counter == users_in_process.__len__():
                add_user(True)
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def add_user(is_ready):
    users_in_process.append(
        User(current_user.id, current_user.user_lvl, current_user.name, current_user.surname, current_user.email,
             current_user.phone, is_ready))


if __name__ == '__main__':
    app.run(debug=True)
