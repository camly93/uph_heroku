from flask import Flask,render_template
from flask import request
import pygal


from mongoengine import *

app = Flask(__name__)

connect('amazon_rank',host='mongodb://amazon:mlab1234@ds015740.mlab.com:15740/amazon_rank')

# class data_rank(Document):
#     username=StringField()
#     id_sanpham=StringField()
#     group=StringField()
#     rank=StringField()
#     time=StringField()
# rank_list=data_rank.objects

# for rank in rank_list:
#     print(rank.rank)

#http://docs.mongoengine.org/guide/defining-documents.html#embedded-documents
class Xephang(EmbeddedDocument):
    rank = StringField()
    time = StringField()

class Nhom(EmbeddedDocument):
    ten_nhom = StringField()
    xephang = ListField(EmbeddedDocumentField(Xephang))

class Sanpham(Document):
    ten_sanpham = StringField()
    nhom = ListField(EmbeddedDocumentField(Nhom))


# class Username(Document):
#     username= StringField()
#     sanpham = ListField(EmbeddedDocumentField(Sanpham))
#


# comment1 = Comment(content='Good work!')
# comment2 = Comment(content='Nice article!')
# page = Page(comments=[comment1, comment2])

# xephang1 = Xephang(rank='12',time='130116')
# xephang2 = Xephang(rank='12',time='140116')
# nhom1=Nhom(ten_nhom="garden",xephang=[xephang1,xephang2])
# sanpham= Sanpham(ten_sanpham="ABC",nhom=[nhom1])
# # username = Username(username="testsanpham",sanpham=[sanpham1])
# sanpham.save()

# xephang3 = Xephang(rank='115',time='140116')
# for sp in Sanpham.objects(ten_sanpham = "ABC"):
#     for n in sp.nhom:
#         n.xephang.append(xephang3)
#         n.save()

# for sp in Sanpham.objects():
#     print(sp.ten_sanpham)
#     for n in sp.nhom:
#         print(n.ten_nhom)
#         for rank in n.xephang:
#             print(rank.rank)
#             print(rank.time)

@app.route('/testsanpham', methods=['GET', 'POST'])
def sanpham():
    # return "hello"
    if request.method == 'POST':
        x=request.form['group']
        y=request.form['rank']
        z=request.form['time']
        return "Ôi ra rồi sướng quá anh "+ x +" ơi " +" rank " +y +" time "+ z
    return render_template("user_sanpham.html",sanpham =Sanpham.objects)
    return 'Hello World!'

@app.route('/')
def hello_world():
    return render_template("login.html")




if __name__ == '__main__':
    app.run()
