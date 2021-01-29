# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import PIL
from PIL import Image
import  requests
import io
from colorthief import ColorThief
import os
import os.path as path
import hashlib
import time
import threading
import sys
# Change these variables
driver_path= "C:/Users/aksha/chromedriver.exe"
FOLDER="C:/Users/aksha/Desktop/Wallpapers"
username="akshatgarg789"
password="Swcusbr7$89"
# fixed variables

URL="https://www.deviantart.com/users/login"

sources=["https://www.deviantart.com/topic/wallpaper","https://www.deviantart.com/search?q=4k%20wallpapers","https://www.deviantart.com/topic/photo-manipulation","https://www.deviantart.com/topic/digital-art"]
# setup_driver
option1= Options()
option1.add_argument('window-size=1920x1080')
option1.add_argument('--log-level=3')
wd = webdriver.Chrome(driver_path,options=option1)

# global variables
urls=[]
img_urls=[]
# Functions
def login():
    print("getting wallpaper website ....")
    wd.get(URL)
    prompt=input('> ')
    if prompt=="y":
        
        print("logging in .....")
        wd.find_element_by_id("username").send_keys(username)
        wd.find_element_by_id("password").send_keys(password)
        wd.find_element_by_id("loginbutton").submit()
    else:
        wd.close()
        raise SystemExit("Since you disagreed to login the script will not work please press y if the login screen appears or you have done captcha") 
def find_urls(source:str="https://www.deviantart.com/topic/wallpaper"):
    try:
        print(f"getting wallpaper from {source}")
        wd.get(source)
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        images=wd.find_elements_by_xpath('//div[@class="_1CX6F"]/..')
        print("getting image urls ...")
        for image in images:
            urls.append(image.get_attribute('href'))
    except Exception:
        pass
    
def inspect_img(dom:str=None):
    for url in urls:
        try:
            wd.get(url)
            src=wd.find_element_by_xpath("//img[@class='_1izoQ vbgSM']").get_attribute('src')
            img_urls.append(src)
        except Exception:
            pass
    
    for url in img_urls:
        try:
            print('-'*50)
            print("getting image from url...")
            img_content = requests.get(url).content
       
            img_file=io.BytesIO(img_content)
            img= Image.open(img_file).convert('RGB')
            if dom!=None:
                print("getting dominant color ...")
                colorthief1=ColorThief(img_file)
                dom_color=colorthief1.get_color(quality=1)
                r,g,b=dom_color
                print(f"checking of the dominant color is of code {dom}")
                if dom == 'B':
                    if b>r and b>g:
                        print("getting file path")
                        file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
                        print(f"saving image in {FOLDER}")
                        with open(file_path, 'wb') as f:
                            img.save(f, "JPEG")
                elif dom=='G':
                    if g>b and g>r:
                        print("getting file path")
                        file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
                        print(f"saving image in {FOLDER}")
                        with open(file_path, 'wb') as f:
                            img.save(f, "JPEG")
                elif dom == 'R':
                    if r>b and r>g:
                        print("getting file path")
                        file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
                        print(f"saving image in {FOLDER}")
                        with open(file_path, 'wb') as f:
                            img.save(f, "JPEG")
            else:
                print("getting file path")
                file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
                print(f"saving image in {FOLDER}")
                with open(file_path, 'wb') as f:
                    img.save(f, "JPEG")
        except Exception as e:
            print('-'*50)
            print("ERROR - UNABLE TO GET IMAGE")
            print('-'*50)
        
# execute
if __name__ == "__main__":
    login()
    find_urls(sources[-1])
    if len(sys.argv)<=1:
        inspect_img()
    else:
        inspect_img(sys.argv[1])
    wd.quit()
        