from bs4 import BeautifulSoup
import requests


def matching_words(string_1, string_2):
    count = 0
    string_1 = string_1.split()
    
    for word in string_1:
        if word in string_2:
            count += 1
    return count
    
def good_match(string, num_matching_words):
    string = string.split()
    str_len = len(string)
    if str_len > 0:
        percent =(float(num_matching_words)*100/float(str_len))
        if percent >= 50:
            return True
    return False

def get_data(url):
    try:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        thumbnails = []
        title = ""
        
        if "amazon.com" in url:
            soup_title = soup.find("span",id="productTitle")
            soup_img = soup.find_all("img", id="landingImage")
            
            if not soup_img:
                return {"error":1,"data":{},"message":"Unable to extract images."}
            else:
                for img in soup_img:
                    thumbnails.append(img["src"])
                
                if soup_title:
                    title = soup_title.string

            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
            
        
        elif "ebay.com" in url:
            soup_title = soup.find("h1", id="itemTitle")
            
            soup_img = soup.find_all("img", id="icImg")
            
            if not soup_img:
                return {"error":1,"data":{},"message":"Unable to extract images."}
            else:
                for img in soup_img:
                    thumbnails.append(img["src"])
                
                if soup_title:
                    children = []
                    for child in soup_title.children:
                        children.append(child)
                    title = children[1]

            return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}
        
        
        else:
            
            soup_title = soup.title.string
            
            for img in soup.find_all("img", alt=True):
                alt = img['alt']
                src = img['src']
                numMatchingWords = matching_words(soup_title,alt)
                if good_match(alt, numMatchingWords):
                    
                    if src not in thumbnails and src[-4:]==".jpg" and "sprite" not in src:
                        
                        thumbnails.append(src)
                    if not title:
                        title = soup_title
                        
            if not thumbnails:
                for img in soup.findAll("img", src=True):
                    if "sprite" not in img["src"] and src[-4:]==".jpg":
                        thumbnails.append(img["src"])
                        
            if not thumbnails:
                return {"error":1,"data":{},"message":"Unable to extract images."}
    
    except requests.exceptions.RequestException:
        return {"error":2,"data":{},"message":"URL entered is invalid."}
    
    return {"error":None,"data":{"title":title, "thumbnails":thumbnails},"message":"Success"}

    
    

url1 = "http://www.ebay.com/itm/Apple-iPad-Air-2-64GB-Wi-Fi-4G-Cellular-Apple-SIM-9-7in-Silver-/252314650117?hash=item3abf200605:g:m8sAAOSwN81WDu3a"
url2 = "http://www.ebay.com/itm/Unlocked-Dual-Sim-BLU-PHONE-Advance-5-0-Smartphone-US-GSM-White-/262304395053?hash=item3d128f6f2d:g:ntQAAOSwe7BWzOQU"
url3 = "http://www.amazon.com/gp/product/B00THKEKEQ/ref=s9_ri_gw_g421_i1_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-4&pf_rd_r=1WEK74K6Y8MXQC6BSHDN&pf_rd_t=36701&pf_rd_p=2437869562&pf_rd_i=desktop"

url5 = "http://www.forever21.com/Product/Product.aspx?BR=f21&Category=dress&ProductID=2000187141&VariantID="
url6 = "http://www.homedepot.com/p/Samsung-Chef-Collection-24-1-cu-ft-4-DoorFlex-French-Door-Refrigerator-in-Stainless-Steel-Counter-Depth-RF24J9960S4/206046683"
url7 = "http://www.walmart.com/ip/46201753?findingMethod=wpa&wpa_qs=DzjAXPVfWOGVVepHE5ZfB_oDpEnKXg_YgvHURtkauAM&tgtp=2&cmp=-1&pt=hp&adgrp=-1&plmt=1145x345_B-C-OG_TI_8-20_HL_MID_HP&bkt=__bkt__&pgid=0&adUid=6abe87a7-e10e-47be-95ed-78acc0ced678&adiuuid=4389b3fd-2b89-49e7-b5c6-e21789ccce98&adpgm=hl&pltfm=desktop"
url8 = "http://www.amazon.com/AmazonBasics-Lightweight-On-Ear-Headphones-Black/dp/B00NBEWB4U/ref=sr_1_1?s=electronics&srs=10112675011&ie=UTF8&qid=1459377481&sr=1-1"


#print get_data(url1)
#print get_data(url2)
#print get_data(url3)

#print get_data(url5)
#print get_data(url6)
#print get_data(url7)
#print get_data(url8)