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
# fixed variables
driver_path= "C:/Users/aksha/chromedriver.exe"
URL="https://www.deviantart.com/users/login"
NUM_CLUSTERS = 5
FOLDER="C:/Users/aksha/Desktop/Wallpapers"
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
        wd.find_element_by_id("username").send_keys("akshatgarg789")
        wd.find_element_by_id("password").send_keys("Swcusbr7$89")
        wd.find_element_by_id("loginbutton").submit()
def find_urls():
    print("getting wallpaper ....")
    wd.get("https://www.deviantart.com/topic/wallpaper")
    wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    images=wd.find_elements_by_xpath('//div[@class="_1CX6F"]/..')
    print("getting image urls ...")
    for image in images:
        urls.append(image.get_attribute('href'))
    print('-'*50)
def inspect_img(dom:str=None):
    for url1 in urls:
        try:
            wd.get(url1)
            src=wd.find_element_by_xpath("//img[@class='_1izoQ vbgSM']").get_attribute('src')
            img_urls.append(src)
        except Exception:
            pass
    wd.quit()
    for url in img_urls:
        try:
            print("getting image from url...")
            img_content = requests.get(url).content
        except Exception as e:
            print('-'*50)
            print("ERROR -unable to get image from url")
            print('-'*50)
        img_file=io.BytesIO(img_content)
        img= Image.open(img_file).convert('RGB')
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
                    img.save(f, "JPEG", quality=85)
        elif dom=='G':
            if g>b and g>r:
                print("getting file path")
                file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
                print(f"saving image in {FOLDER}")
                with open(file_path, 'wb') as f:
                    img.save(f, "JPEG", quality=85)
        elif dom == 'R':
            if r>b and r>g:
                print("getting file path")
                file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
                print(f"saving image in {FOLDER}")
                with open(file_path, 'wb') as f:
                    img.save(f, "JPEG", quality=85)
        else:
            print("getting file path")
            file_path=  path.join(FOLDER,hashlib.sha1(img_content).hexdigest()[:10] + '.jpg')
            print(f"saving image in {FOLDER}")
            with open(file_path, 'wb') as f:
                img.save(f, "JPEG", quality=85)
        
# execute
if __name__ == "__main__":
    login()
    find_urls()
    inspect_img()
