import sqlite3
from flask import g
from .main import main
from config import basedir


def connect_db():
    """连接到数据库"""
    rv = sqlite3.connect(basedir + '\\SQL.db')
    return rv


def get_db():
    """如果没有连接数据库，则进行连接"""
    if not hasattr(g, 'sql_db'):
        g.sql_db = connect_db()
    return g.sql_db


@main.teardown_app_request
def close_db(error):
    """如果已经连接数据库，则释放连接"""
    if hasattr(g, 'sql_db'):
        g.sql_db.close()
