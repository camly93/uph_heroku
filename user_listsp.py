from mongoengine import *
import codecraper


connect('amazon_rank',host='mongodb://amazon:mlab1234@ds015740.mlab.com:15740/amazon_rank')

class Listsp(EmbeddedDocument):
    ten_sanpham = StringField()

class User_sanpham(Document):
    username = StringField()
    sanpham = ListField(EmbeddedDocumentField(Listsp))

class User_nhap_sp:
    def __init__(self, name,ten_sp):
        self.name = name
        self.sp_nhap= ten_sp

def list_sanpham(nhap_user):
    for user_data in User_sanpham.objects():
        if user_data.username==nhap_user:
            return user_data.sanpham
        return "khong"
def nhap_sanpham(nhap_user,nhap_sp):
    user_nhap=User_nhap_sp(nhap_user,nhap_sp)
    print(user_nhap.name)
    #check rank sanpham luon khi nhap
    codecraper.check_rank(nhap_sp)

    listsp=Listsp(ten_sanpham=user_nhap.sp_nhap)

    if len(User_sanpham.objects())==0:
        user_sp=User_sanpham(username=user_nhap.name,sanpham=[listsp])
        user_sp.save()
    else:
        w=0
        for user_data in User_sanpham.objects():
            if user_data.username==user_nhap.name:
                w=1
                # print(sp.ten_sanpham)
                k=0
                for sp in user_data.sanpham:
                    if  user_nhap.sp_nhap== sp.ten_sanpham:
                        k=1
                        break
                if k==0:
                    user_data.sanpham.append(listsp)
                    user_data.save()
                break
        if w==0:
            user_sp=User_sanpham(username=user_nhap.name,sanpham=[listsp])
            user_sp.save()
