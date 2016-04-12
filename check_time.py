import datetime
from mongoengine import *
import codecraper

connect('amazon_rank',host='mongodb://amazon:mlab1234@ds015740.mlab.com:15740/amazon_rank')

class Xephang(EmbeddedDocument):
    rank = StringField()
    time = StringField()

class Nhom(EmbeddedDocument):
    ten_nhom = StringField()
    xephang = ListField(EmbeddedDocumentField(Xephang))

class Sanpham(Document):
    id_sanpham = StringField()
    ten_sanpham = StringField()
    nhom = ListField(EmbeddedDocumentField(Nhom))


if len(Sanpham.objects()) == 0:
    print("khong")
else:
    for sp in Sanpham.objects():
        codecraper.check_rank(sp.id_sanpham)