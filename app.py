from flask import Flask,render_template,redirect,url_for,make_response
from flask import request
import user_listsp
import Lay_id

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
    id_sanpham= StringField()
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
        codangnhap = False
        for nguoi_dung in user.objects():
            if x == nguoi_dung.username and y == nguoi_dung.password :
                codangnhap = False
                resp = make_response(redirect(url_for('profile', username=nguoi_dung.username)))
                resp.set_cookie('username', y)
                return resp
        if codangnhap==False:
            return render_template("login.html",saidangnhap="Sai user hoặc mật khẩu.")
    return render_template("login.html")

@app.route('/dangky/', methods=['GET', 'POST'])
def dangky():
    if request.method == 'POST':
        x=request.form['username']
        y=request.form['password']
        codangnhap = True
        for nguoi_dung in user.objects():
            if x == nguoi_dung.username:
                codangnhap = False
                return render_template("dangky.html", saidangky="Tên đăng nhập bị trùng")
        if codangnhap==True:
            user_moi = user(username=x, password=y)
            user_moi.save()
            return redirect(url_for('trangchu'))
    return render_template("dangky.html")



@app.route('/user/<username>', methods=['GET', 'POST'])
def profile(username):
    try:
        x= request.cookies.get('username')
    except NameError:
        x = None
    if x is None:
        return redirect(url_for('trangchu'))
    else:
        password = x
    codangnhap = False

    for nguoi_dung in user.objects():
        if username == nguoi_dung.username and password == nguoi_dung.password:
            codangnhap=True
            list_sanpham=user_listsp.list_sanpham(username)
            listsp=[]
            if list_sanpham=="khong":
                kequa=[]
            else:
                for x in list_sanpham:
                    listsp.append(Sanpham.objects(id_sanpham=x.id_sanpham))
                    # listsp.append(x.ten_sanpham)

            if request.method == 'POST':
                link_id=request.form['link_id']
                print(link_id)
                id_del = request.form['id_del']

                if link_id != "":
                    id_sp=Lay_id.layid(link_id)

                # id_sp=request.form['id_sp']

                if id_del == 'xxx':
                    print(id_sp)
                    user_listsp.nhap_sanpham(username,id_sp)
                    return redirect(url_for('profile', username=username))
                if id_del != 'xxx':
                    user_listsp.xoa_sanpham(username,id_del)
                    list_sanpham = user_listsp.list_sanpham(username)
                    listsp = []
                    for x in list_sanpham:
                        listsp.append(Sanpham.objects(id_sanpham=x.id_sanpham))
                    return render_template("ketqua.html", username=username, listsp=listsp)

            # return render_template("ketqua.html",username=username)
            return render_template("ketqua.html",username=username,listsp=listsp)
    if codangnhap==False:
        return redirect(url_for('trangchu'))




if __name__ == '__main__':
    app.run()
