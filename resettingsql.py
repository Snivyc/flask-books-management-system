import sqlite3
import os
os.remove('SQL.db')
conn = sqlite3.connect('SQL.db')
curs = conn.cursor()
curs.execute('PRAGMA foreign_keys = ON;')
curs.execute('''CREATE TABLE USER
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR(20) UNIQUE,
NUM INTEGER,
CLASS INTEGER,
DEBT INTEGER default 0,
ROLE INTEGER,
PASSWORD VARCHAR(16),
LOSSREPORTING BOOLEAN default 0)''')

insUser = 'INSERT INTO USER (NAME, NUM, CLASS, ROLE, PASSWORD) VALUES(?,?,?,?,?)'
curs.execute(insUser, ('admin', 0, 0, 0, 'root'))
curs.execute(insUser, ('bookadmin', 0, 0, 1, 'bookroot'))
curs.execute(insUser, ('teacherz', 0, 0, 2, 'zhanglaoshi'))
curs.execute(insUser, ('CTH', 8, 142304, 3, '960325'))
curs.execute(insUser, ('ZY', 29, 142304, 3, '222222'))
curs.execute(insUser, ('GRJ', 12, 142304, 3, '222222'))
curs.execute(insUser, ('YB', 26, 142304, 3, '222222'))

curs.execute('''CREATE TABLE BOOK
(BOOKID INTEGER PRIMARY KEY AUTOINCREMENT,
BOOKNAME VARCHAR(20),
AUTHOR VARCHAR(20),
PUBLISHER VARCHAR,
PUBDATA DATE,
MONEY INTEGER,
CLASS CARCHAR(10),
NUM INTEGER,
NUMINL INTEGER,
READERRANGE VARCHAR(10),
READERTIME INTEGER default 0)''')

insBook = 'INSERT INTO BOOK (BOOKNAME, AUTHOR, PUBLISHER, MONEY, CLASS, NUM, NUMINL, PUBDATA, READERRANGE, READERTIME) VALUES(?,?,?,?,?,?,?,?,?,?)'
curs.execute(insBook, ('Flask Web开发','Miguel Grinberg', '人民邮电出版社', 59, '计算机', 3, 2, '2015-1-26', '所有人',2))
curs.execute(insBook, ('PHP是世界上最好的语言','ZWL', '人民邮电出版社', 250, '计算机', 3, 2, '2013-6-4', '所有人',3))
curs.execute(insBook, ('C++ 从入门到入土','MDZZ', '机械工业出版社', 53, '计算机', 3, 3, '2012-8-26', '所有人',2))
curs.execute(insBook, ('Java 从入门到放弃','AABBC', '清华大学出版社', 29, '计算机', 3, 3, '2012-12-14', '所有人',16))
curs.execute(insBook, ('MySQL 从删库到跑路','ZZXXXC', '清华大学出版社', 79, '计算机', 3, 3, '2012-8-26', '所有人',12))
curs.execute(insBook, ('哲学天堂','Billy', '新日暮里出版社', 80, '文学', 3, 2, '2017-3-8', '老师',5))
curs.execute(insBook, ('百年航母','张召忠', '中国人民出版社', 200, '军事', 3, 3, '2013-4-18', '所有人',4))
curs.execute(insBook, ('森之妖精','木吉', '新日暮里出版社', 80, '文学', 3, 3, '2017-3-18', '所有人',7))
curs.execute(insBook, ('DEEP♂DARK♂FANTASY','佟大为', '新日暮里出版社', 80, '文学', 3, 3, '2017-4-22', '所有人',2))
curs.execute(insBook, ('张元哲学语录','张元', '新日暮里出版社', 80, '文学', 3, 3, '2017-2-8', '所有人',1))
curs.execute(insBook, ('波波五月天','杨波', '新日暮里出版社', 80, '文学', 3, 0, '2017-3-18', '老师',30))
curs.execute(insBook, ('杰哥传奇','高仁杰', '新日暮里出版社', 80, '文学', 3, 3, '2017-3-28', '所有人',5))


curs.execute('''CREATE TABLE BORROW
(ID INTEGER,
BOOKID INTEGER,
TIME DATE,
TIMEOUT DATE,
PRIMARY KEY(ID, BOOKID),
FOREIGN KEY(ID)REFERENCES USER(ID) on delete cascade,
FOREIGN KEY(BOOKID)REFERENCES BOOK(BOOKID) on delete cascade)''')

insBorrow = 'INSERT INTO BORROW (ID, BOOKID, TIME, TIMEOUT) VALUES(?,?,?,?)'
curs.execute(insBorrow, (4,1,'2017-2-21','2017-3-23'))
curs.execute(insBorrow, (1,2,'2017-3-23','2017-4-22'))
curs.execute(insBorrow, (1,11,'2017-3-23','2017-4-22'))
curs.execute(insBorrow, (2,11,'2017-3-20','2017-4-19'))
curs.execute(insBorrow, (2,6,'2017-3-20','2017-4-19'))
curs.execute(insBorrow, (3,11,'2017-3-20','2017-4-19'))




curs.execute('''SELECT * FROM USER''')
rows = curs.fetchall()
print(rows)
curs.execute('''SELECT * FROM BOOK''')
rows = curs.fetchall()
print(rows)
curs.execute('''SELECT * FROM BORROW''')
rows = curs.fetchall()
print(rows)

conn.commit()
curs.close()
conn.close()
