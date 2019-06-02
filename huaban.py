from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import requests
import lxml.html
import os


## 设置webdriver 的种类

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
browser.set_window_size(1400,900)

'''
parser(url, param)这个函数用来解析网页，
后面有几次都用用到这些代码，所以直接写一个函数会让代码看起来更整洁有序。
函数有两个参数：一个是网址，另一个是显性等待代表的部分，
这个可以是网页中的某些板块，按钮，图片等等...

'''

def parser(url,param):
    browser.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,param)))
    html = browser.page_source
    doc = lxml.html.fromstring(html)
    return doc


def get_main_url():
    print('打开主页搜索链接...')
    try:
        doc = parser('http://huaban.com/boards/favorite/beauty/','#waterfall')
        name = doc.xpath('//*[@id="waterfall"]/div/a[1]/div[2]/h3/text()')
        u = doc.xpath('//*[@id="waterfall"]/div/a[1]/@href')
        for item,fileName in zip(u,name):
            main_url = 'http://huaban.com' + item
            print('主链接已找到' + main_url)
            if '*' in fileName:
                fileName = fileName.replace('*','')
            download(main_url,fileName)
    except Exception as e:
        print(e)





def download(main_url,fileName):
    print("------准备下载中------")
    try:
        doc = parser(main_url,'#waterfall')
        if not os.path.exists('image\\' + fileName):
            print('创建文件夹...')
            os.makedirs('image\\' + fileName)
        link = doc.xpath('//[@id="waterfall"]/div/a/@href')
        # print(link)
        i = 0
        for item in link:
            i += 1
            minor_url = 'http://huaban.com' + item
            doc = parser(minor_url,'#pin_view_page')
            img_url = doc.xpath('//*[@id="baidu_image_holder"]/a/img/@src')
            img_url2 = doc.xpath('//*[@id="baidu_image_holder"]/img/@src')
            img_url += img_url2
            try:
                url = 'http:' + str(img_url[0])
                print('正在下载第' + str(i) + '张图片，地址:' + url)
                r = requests.get(url)
                filename = 'image\\{}\\'.format(fileName) + str(i) + '.jpg'
                with open(filename,'wb') as fo:
                    fo.write(r.content)
            except Exception:
                print('出错')
    except Exception:
        print('出错')

if __name__ == '__main__':
    get_main_url()