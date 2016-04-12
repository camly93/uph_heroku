import requests
from bs4 import BeautifulSoup
import re
import datetime
from mongoengine import *

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


def check_rank(sanpham):
    now = datetime.datetime.now()
    time=now.strftime("%Y-%m-%d")
    id = sanpham
    link_get = "http://www.amazon.com/dp/"+id
    link_amazon = requests.get(link_get,headers={ "user-agent": "The Coolest Useragent" })
    link_amazon_html = BeautifulSoup(link_amazon.content,"html.parser")
    link_amazon_id = link_amazon_html.find("li",id="SalesRank")
    link_amazon_id1 = link_amazon_html.find("table",id="productDetails_detailBullets_sections1")
    if link_amazon_id == None:
        if link_amazon_id1 != None:
            h=link_amazon_id1.text.strip()
            c=re.findall("#[0-9]*.[0-9]* in .*",h)
            b='\n'.join(c)
        else:
            b=""
    else:
        b=link_amazon_id.text.strip()
    trim_link_amazon =b.replace('\xa0',' ').replace(')','')
    res = re.findall(r"#([0-9]*.[0-9]*)",trim_link_amazon)
    name_group=[]
    for element in re.findall(".*in (.*)",trim_link_amazon):
        if re.match('.*>.*',element)== None:
            name_group.append(element)
        else:
            c=re.findall('.*> (.*)',element)[0]
            name_group.append(c)
    class San_pham:
         def __init__(self,id,rank,group,time):
             self.id=id
             self.rank=rank
             self.group=group
             self.time=time
    sanpham_new= San_pham(id,res,name_group,time)
    # print(sanpham_new.rank)
    # print(sanpham_new.group)
    print(time)
    for i in range(0,len(sanpham_new.rank)):
        print(sanpham_new.rank[i])
        print(sanpham_new.group[i])


        xephang = Xephang(rank=sanpham_new.rank[i],time=time)

        if len(Sanpham.objects())==0:
            nhom=Nhom(ten_nhom=sanpham_new.group[i],xephang=[xephang])
            sanpham= Sanpham(ten_sanpham=id,nhom=[nhom])
            sanpham.save()
        else:
            w=0
            for sp in Sanpham.objects():
                if sp.ten_sanpham==id:
                    w=1
                    # print(sp.ten_sanpham)
                    k=0
                    for nh in sp.nhom:
                        print(nh.ten_nhom)
                        print(sanpham_new.group[i])
                        print('-------')
                        if sanpham_new.group[i] == nh.ten_nhom:
                            k=1
                            m=0
                            for xh in nh.xephang:
                                if time == xh.time:
                                    m=1
                                    break
                            if m==0:
                                nh.xephang.append(xephang)
                                nh.save()
                            break

                    if k==0:
                        nhom=Nhom(ten_nhom=sanpham_new.group[i],xephang=[xephang])
                        sp.nhom.append(nhom)
                        sp.save()
                    break
            if w==0:
                nhom=Nhom(ten_nhom=sanpham_new.group[i],xephang=[xephang])
                sanpham= Sanpham(ten_sanpham=id,nhom=[nhom])
                sanpham.save()

