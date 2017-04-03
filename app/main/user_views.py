from ..connectSQL import *
from ..loginTest import is_user
from flask import render_template, session

@main.route('/user')
@is_user
def user_page():
    db = get_db()
    cur = db.execute("SELECT * FROM BORROW WHERE ID=%s" % session.get('ID'))
    books = cur.fetchall()
    print(books)
    cur = db.execute("SELECT DEBT FROM USER WHERE ID=%s" % session.get('ID'))
    debt = cur.fetchall()[0][0]
    return render_template('user.html', name=session.get('name'), books=books, debt=debt)


@main.route('/library')
@is_user
def library():
    db = get_db()
    cur = db.execute('''SELECT * FROM BOOK ORDER by READERTIME desc''')
    books = cur.fetchall()

    return render_template('library.html', books=books)