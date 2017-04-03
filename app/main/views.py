from flask import render_template, session, redirect, url_for, flash, request
from .forms import NameForm
from ..connectSQL import *


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['password'] = form.password.data
        temp = form.radio.data
        if temp == '0':
            return redirect('/admin')
        elif temp == '1':
            return redirect('/book_admin')
        elif temp == '2':
            return redirect('/user')
    return render_template('index.html', form=form)


@main.route('/logout')
def logout():
    session.clear()
    return redirect('/')
