def layid(link_get):
    import requests
    from bs4 import BeautifulSoup
    import re
    link_amazon = requests.get(link_get,headers={ "user-agent": "The Coolest Useragent" })
    link_amazon_html = BeautifulSoup(link_amazon.content,"html.parser")
    link_amazon_id = link_amazon_html.find("div",id="detail-bullets")
    link_amazon_id1 = link_amazon_html.find("table",id="productDetails_detailBullets_sections1")
    if link_amazon_id == None:
        if link_amazon_id1 != None:
            h=link_amazon_id1.text.strip()
            sanpham=re.findall("B.*[0-9].*",h)

        else:
            sanpham="khong support sp nay"
    else:
        b=link_amazon_id.text.strip()
        sanpham=re.findall("ASIN: (.*)",b)
    # print(sanpham)
    return sanpham[0]
# layid("http://www.amazon.com/Lenox-Butterfly-Meadow-Thermal-White/dp/B00H4F2E94/ref=pd_sim_79_4?ie=UTF8&dpID=41p5Gz1dK7L&dpSrc=sims&preST=_AC_UL160_SR160%2C160_&refRID=01KTZHF3YEK9AMMVWK1Z")