from ..connectSQL import *
from ..loginTest import is_admin
from flask import render_template, session, redirect, flash
from .forms import AddUser, UserEdit


@main.route('/admin')
@is_admin
def admin_page():
    return render_template('admin.html', name=session.get('name'))


@main.route('/all_user')
@is_admin
def all_student():
    db = get_db()
    cur = db.execute('''SELECT * FROM USER''')
    students = cur.fetchall()
    return render_template('all_user.html', students=students)


@main.route('/add_new_user', methods=['GET', 'POST'])
@is_admin
def add_new_user():
    form = AddUser()
    if form.validate_on_submit():
        insUser = 'INSERT INTO USER (NAME, NUM, CLASS, ROLE, PASSWORD) VALUES(?, ?, ?, ?, ?)'
        db = get_db()
        try:
            db.execute(insUser, (form.name.data, form.num.data, form.class_.data,
                                  form.role.data, form.password.data))
            db.commit()
            flash('添加成功')
        except:
            flash('用户名冲突')
        return redirect('/all_user')
    return render_template('add_new_user.html', form=form)


@main.route('/user_edit/<ID>', methods=['GET', 'POST'])
@is_admin
def user_edit(ID):
    form = UserEdit()
    if form.validate_on_submit():
        db = get_db()
        print(form.password.data)
        db.execute("UPDATE USER SET NAME='%s', NUM='%s', CLASS='%s', ROLE='%s', PASSWORD='%s',"
                   "LOSSREPORTING='%s' WHERE ID='%s'" %(form.name.data, form.num.data, form.class_.data,
                                                 form.role.data, form.password.data, form.lossReporting.data, ID))
        db.commit()
        flash('修改成功')
        return redirect('/all_user')
    db = get_db()
    cur = db.execute('''select * from user where ID=%s''' % ID).fetchall()[0]
    form.name.data = cur[1]
    form.password.data = cur[6]
    form.role.data = cur[5]
    form.num.data = cur[2]
    form.class_.data = cur[3]
    form.debt.data = cur[4]
    form.lossReporting.data = cur[7]
    return render_template('user_edit.html', ID=ID, form=form)


@main.route('/delete_user/<ID>')
@is_admin
def delete_user(ID):
    db = get_db()
    db.execute('''delete from user where ID=%s''' % ID)
    db.commit()
    flash('删除成功')
    return redirect('all_user')