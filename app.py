from flask import Flask,render_template,redirect,url_for
from flask import request
import user_listsp

from mongoengine import *

app = Flask(__name__)

connect('amazon_rank',host='mongodb://amazon:mlab1234@ds015740.mlab.com:15740/amazon_rank')

class Xephang(EmbeddedDocument):
    rank = StringField()
    time = StringField()

class Nhom(EmbeddedDocument):
    ten_nhom = StringField()
    xephang = ListField(EmbeddedDocumentField(Xephang))

class Sanpham(Document):
    ten_sanpham = StringField()
    nhom = ListField(EmbeddedDocumentField(Nhom))


class user(Document):
    username = StringField()
    password = StringField()





@app.route('/', methods=['GET', 'POST'])
def trangchu():
    if request.method == 'POST':
        x=request.form['username']
        y=request.form['password']
        for nguoi_dung in user.objects():
            if x == nguoi_dung.username and y == nguoi_dung.password :
                return redirect(url_for('profile', username=nguoi_dung.username))
    return render_template("login.html")


@app.route('/user/<username>', methods=['GET', 'POST'])
def profile(username):
    list_sanpham=user_listsp.list_sanpham(username)
    listsp=[]
    if list_sanpham=="khong":
        kequa=[]
    else:
        for x in list_sanpham:
            listsp.append(Sanpham.objects(ten_sanpham=x.ten_sanpham))
            # listsp.append(x.ten_sanpham)

    if request.method == 'POST':
        id_sp=request.form['id_sp']
        print(id_sp)
        user_listsp.nhap_sanpham(username,id_sp)
        return redirect(url_for('profile', username=username))
    # return render_template("ketqua.html",username=username,sanpham=Sanpham.objects(ten_sanpham="B00IXC1ZMY"))
    return render_template("ketqua.html",username=username,listsp=listsp)





if __name__ == '__main__':
    app.run()
