from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    radio = RadioField('选择身份', choices=[('2', '用户'), ('1', '图书管理员'), ('0', '系统管理员')],
                       validators=[DataRequired()], default = '2')
    submit = SubmitField('登陆')


class AddBook(FlaskForm):
    bookName = StringField('书名', validators=[DataRequired()])
    author = StringField('作者', validators=[DataRequired()])
    publisher = StringField('出版商', validators=[DataRequired()])
    publisheDate = StringField('出版日期', validators=[DataRequired()])
    money = StringField('价格', validators=[DataRequired()])
    class_ = StringField('分类', validators=[DataRequired()])
    num = StringField('数量', validators=[DataRequired()])
    readerRange = StringField('读者范围', validators=[DataRequired()])
    submit = SubmitField('添加')


class AddUser(FlaskForm):
    name = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    role = StringField('职务（0.管理员 1.图书管理员 2.教师 3.学生）', validators=[DataRequired()])
    num = StringField('学号', validators=[DataRequired()])
    class_ = StringField('班级', validators=[DataRequired()])
    submit = SubmitField('添加')


class Borrow(FlaskForm):
    ID = StringField('用户ID', validators=[DataRequired()])
    BookID = StringField('图书ID', validators=[DataRequired()])
    submit = SubmitField('借书')


class Return(FlaskForm):
    ID = StringField('用户ID', validators=[DataRequired()])
    BookID = StringField('图书ID', validators=[DataRequired()])
    submit = SubmitField('还书')


class UserEdit(FlaskForm):
    name = StringField('用户名')
    password = StringField('密码')
    role = StringField('职务（0.管理员 1.图书管理员 2.教师 3.学生）')
    num = StringField('学号')
    class_ = StringField('班级')
    debt = StringField('欠款')
    lossReporting = StringField('是否挂失')
    submit = SubmitField('修改')


class EditBook(AddBook):
    bookName = StringField('书名', validators=[DataRequired()])
    author = StringField('作者', validators=[DataRequired()])
    publisher = StringField('出版商', validators=[DataRequired()])
    publisheDate = StringField('出版日期', validators=[DataRequired()])
    money = StringField('价格', validators=[DataRequired()])
    class_ = StringField('分类', validators=[DataRequired()])
    num = StringField('数量', validators=[DataRequired()])
    readerRange = StringField('读者范围', validators=[DataRequired()])
    readedTimes = StringField('借阅次数', validators=[DataRequired()])
    submit = SubmitField('修改')
