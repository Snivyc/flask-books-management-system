from ..connectSQL import *
from ..loginTest import is_book_admin
from flask import render_template, redirect, session, flash
from .forms import AddBook, EditBook, Borrow, Return
import datetime
from config import AppConfig

@main.route('/book_admin')
@is_book_admin
def book_admin():
    return render_template('book_admin.html', name=session.get('name'))


@main.route('/book_admin/borrow', methods=['GET', 'POST'])
@is_book_admin
def book_admin_borrow():
    form = Borrow()
    ID = form.ID.data
    BookID = form.BookID.data
    day = datetime.date.today()
    if form.validate_on_submit():
        insBorrow = 'INSERT INTO BORROW (ID, BOOKID, TIME, TIMEOUT) VALUES(?, ?, ?, ?)'
        db = get_db()
        cur = db.execute("SELECT READERRANGE, NUMINL FROM BOOK WHERE BOOKID='%s'" % BookID).fetchall()
        cur2 = db.execute("SELECT ROLE, LOSSREPORTING FROM USER WHERE ID='%s'" % ID).fetchall()
        cur3 = db.execute("SELECT COUNT(*) FROM BORROW WHERE ID='%s'" % ID).fetchall()
        print(cur3)
        if cur and cur2:  # 输入值是否存在
            if cur2[0][1] == 0:  # 此用户未挂失
                if cur[0][1] > 0:  # 此书没借完
                    if cur2[0][0] <= 2:  # 身份为老师
                        if cur3[0][0] < AppConfig.teacherMaxNumber:
                            try:
                                db.execute(insBorrow, (ID, BookID, day, day + datetime.timedelta(AppConfig.maxDay)))
                                db.execute("UPDATE BOOK SET NUMINL=NUMINL-1 WHERE BOOKID='%s'" % BookID)
                                db.commit()
                                flash('借书成功')
                            except:
                                flash('您已经借了这本书了')
                        else:
                            flash("借书数量已满")
                    else:  # 身份为学生
                        if cur[0][0] == '所有人':
                            if cur3[0][0] < AppConfig.studnetMaxNumber:
                                try:   # 尝试插入，如果有相同值则插入失败
                                    db.execute(insBorrow, (ID, BookID, day, day + datetime.timedelta(AppConfig.maxDay)))
                                    db.execute("UPDATE BOOK SET NUMINL=NUMINL-1 WHERE BOOKID='%s'" % BookID)
                                    db.commit()
                                    flash('借书成功')
                                except:
                                    flash('您已经借了这本书了')
                            else:
                                flash("借书数量已满")
                        else:
                            flash('您没有没有权限借这本书')
                else:
                    flash('此书已被借完')
            else:
                flash('此用户已挂失')
        else:
            flash('输入超出范围')
        return redirect('/book_admin/borrow')
    return render_template('borrow.html', name=session.get('name'), form=form)


@main.route('/book_admin/return', methods=['GET', 'POST']) #没判断！！！！！！
@is_book_admin
def book_admin_return():
    form = Return()
    ID = form.ID.data
    BookID = form.BookID.data
    today = datetime.date.today()
    if form.validate_on_submit():
        db = get_db()
        temp = db.execute("SELECT TIMEOUT FROM BORROW WHERE ID = '%s' AND BOOKID = '%s'" % (ID, BookID)).fetchall()
        print(temp)
        if temp:
            timeout = datetime.datetime.strptime(temp[0][0], '%Y-%m-%d').date()
            db.execute('DELETE FROM BORROW WHERE ID = \'%s\' AND BOOKID = \'%s\'' % (ID, BookID))
            db.execute("UPDATE BOOK SET NUMINL=NUMINL+1 WHERE BOOKID='%s'" % BookID)
            db.commit()
            days = (today - timeout).days
            if days > 0:
                flash('超期%s天' % days)
                db.execute("UPDATE USER SET DEBT=DEBT+'%d' WHERE ID='%s'" % (days * AppConfig.moneyEachDay, ID))
            flash('还书成功')
        else:
            flash('还书失败')
        return redirect('/book_admin/return')
    return render_template('return.html', name=session.get('name'), form=form)


@main.route('/add_new_book', methods=['GET', 'POST'])
@is_book_admin
def add_new_book():
    form = AddBook()
    if form.validate_on_submit():
        insBook = 'INSERT INTO BOOK (BOOKNAME, AUTHOR, PUBLISHER, MONEY, CLASS, NUM, NUMINL, PUBDATA, READERRANGE)' \
                  'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        db = get_db()
        db.execute(insBook, (form.bookName.data, form.author.data, form.publisher.data,
                               form.money.data, form.class_.data, form.num.data, form.num.data,
                               form.publisheDate.data, form.readerRange.data))
        db.commit()
        # form.bookName.data = ''
        # form.author.data = ''
        # form.publisher.data = ''
        # form.money.data = ''
        # form.class_.data = ''
        # form.num.data = ''
        # form.num.data = ''
        # form.publisheDate.data = ''
        # form.readerRange.data = ''
        return redirect('/add_book')
        # curs.execute('''SELECT * FROM BOOK ''')
        # print(curs.fetchall())
    return render_template('add_new_book.html', form=form)


@main.route('/all_book', methods=['GET', 'POST'])
@is_book_admin
def all_book():
    db = get_db()
    cur = db.execute('''SELECT * FROM BOOK''')
    books = cur.fetchall()

    return render_template('all_book.html', books=books)


@main.route('/book_edit/<BookID>', methods=['GET', 'POST'])
@is_book_admin
def book_edit(BookID):
    form = EditBook()
    if form.validate_on_submit():
        db = get_db()
        db.execute("UPDATE BOOK SET BOOKNAME ='%s', AUTHOR='%s', PUBLISHER='%s', PUBDATA='%s', MONEY='%s', CLASS='%s',"
                   "NUM='%s', READERRANGE='%s', READERTIME='%s' WHERE BookID='%s'" %
                   (form.bookName.data, form.author.data, form.publisher.data,form.publisheDate.data, form.money.data,
                    form.class_.data, form.num.data, form.readerRange.data, form.readedTimes.data, BookID))
        db.commit()
        cur = db.execute("select * from BOOK where BookID = '%s'" % BookID)
        print(cur.fetchall()[0])
        return redirect('/all_book')
    db = get_db()
    cur = db.execute('''select * from BOOK where BookID=%s''' % BookID).fetchall()[0]
    form.bookName.data = cur[1]
    form.author.data = cur[2]
    form.publisher.data = cur[3]
    form.publisheDate.data = cur[4]
    form.money.data = cur[5]
    form.class_.data = cur[6]
    form.num.data = cur[7]
    form.readerRange.data = cur[9]
    form.readedTimes.data = cur[10]
    return render_template('book_edit.html', form=form)


@main.route('/delete_book/<BookID>')
@is_book_admin
def delete_book(BookID):
    db = get_db()
    try:
        db.execute('PRAGMA foreign_keys = ON;')
        db.execute('''delete from BOOK where BOOKID=%s''' % BookID)
        db.commit()
    except:
        flash('未找到该图书')
    return redirect('all_book')


@main.route('/timeout')
@is_book_admin
def timeout():
    today = datetime.date.today()
    db = get_db()
    bookList = db.execute('SELECT * FROM BORROW').fetchall()
    books = []
    for x in bookList:
        timeout = datetime.datetime.strptime(x[3],'%Y-%m-%d').date()
        if (today - timeout).days > 0:
            books.append(x)
    return render_template('timeout.html', books = books)