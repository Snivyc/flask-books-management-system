import sqlite3
from flask import session, redirect, flash
from config import basedir
from functools import wraps
def to_do():
    conn = sqlite3.connect(basedir + '\\SQL.db')
    cur = conn.execute('''SELECT ID,ROLE FROM USER
    WHERE NAME = \'%s\' and PASSWORD = \'%s\'''' % (session.get('name'), session.get('password'))).fetchall()

    conn.close()
    return cur


def is_admin(func):
    '''通过cookie判断该用户是否是管理员'''
    @wraps(func)
    def new_func(*args, **kwargs):
        temp = to_do()
        if temp:
            session['ID'] = temp[0][0]
            if temp[0][1] == 0:
                return func(*args, **kwargs)
            else:
                flash('权限不够')
                return redirect('/')
        else:
            flash('密码错误或用户名不存在')
            return redirect('/')
    return new_func


def is_book_admin(func):
    '''通过cookie判断该用户是否是图书管理员及以上级别的用户'''
    @wraps(func)
    def new_func(*args, **kwargs):
        temp = to_do()
        if temp:
            session['ID'] = temp[0][0]
            if 0 <= temp[0][1] <= 1:
                return func(*args, **kwargs)
            else:
                flash('权限不够')
                return redirect('/')
        else:
            flash('密码错误或用户名不存在')
            return redirect('/')
    return new_func


def is_user(func):
    '''通过cookie判断该用户是否是普通用户及以上级别的用户'''
    @wraps(func)
    def new_func(*args, **kwargs):
        temp = to_do()
        if temp:
            session['ID'] = temp[0][0]
            return func(*args, **kwargs)
        else:
            flash('密码错误或用户名不存在')
            return redirect('/')
    return new_func
