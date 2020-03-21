import os
import time
from lxml import etree
import requests
import base64
import hashlib
from PIL import Image
import re

from util import Logger as myLogger


from config import myConfig

log = myLogger.Logger()

def getCookiesFromSession(session):
    cookies = session.cookies.get_dict()
    return cookies

def getCkFromCookies(session):
    cookies = getCookiesFromSession(session)
    ck = cookies.get('ck')
    if (ck is None):
        log.error("No ck found in cookies", cookies)
        raise Exception('No ck found in cookies')

    return ck

def loadCookies():
    cookies = {}
    with open('resources/cookies.txt', "r", encoding='utf-8') as f_cookie:
        douban_cookies = f_cookie.readlines()[0].split("; ")
        for line in douban_cookies:
            key, value = line.split("=", 1)
            cookies[key] = value
        return cookies

def flushCookies(session: requests.Session):
    cookies = session.cookies.get_dict()
    line = ""
    with open('resources/cookies.txt', "w", encoding='utf-8') as f_cookie:
        for k, v in cookies.items():
            line += k +'='+v+'; '
        line = line[:len(line)-2]
        f_cookie.write(line)

def getCred(fileName='confidentials/pwd.txt'):
    data = {}
    with open(fileName, 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        for li in lines:
            k, v = li.strip().split('=')
            data[k.strip()] = v.strip()
    
    return data


def getAccessToken():
    url = ''
    cred = getCred('')
    myid = cred['myid']
    mysecret = cred['mysecret']
    url = url + '&client_id='+myid+'&client_secret='+mysecret
    json = requests.get(url).json()
    # if json.get('error') is None:
    return json['access_token']
    
def getTextFromPic(fileName) -> str:
    img = None
    # 二进制方式打开图片文件
    with open(fileName, 'rb') as f:
        img = base64.b64encode(f.read())

    params = {"image":img, 'language_type':'ENG'}
    header = {'Content-Type':'application/x-www-form-urlencoded'}
    request_url = ""
    accessToken = getAccessToken()
    request_url = request_url + "?access_token=" + accessToken
    r = requests.post(request_url, data=params, headers=header)

    # log.info(r.json())
    resp = r.json()
    word = resp.get('words_result')
    if word is None or len(word) == 0:
        log.error("In getTextFromPic", resp)
        return ""
    text = resp['words_result'][0]['words'].lower()
    return re.sub(r"[^a-z]+", '', text)

def getCaptchaInfo(session, postUrl, r=None):
    if r is not None:
        return parseCaptchaInfo(r)
    time.sleep(10)
    r = session.get(postUrl)
    # error handling
    html = etree.HTML(r.text)
    pic_url = html.xpath("")
    pic_id = html.xpath("")
    return pic_url[0], pic_id[0]

def parseCaptchaInfo(r):
    html = etree.HTML(r.text)
    pic_url = html.xpath("")
    pic_id = html.xpath("")
    return pic_url[0], pic_id[0]

def save_pic_to_disk(pic_url, session):
    # 将链接中的图片保存到本地，并返回文件名
    try:
        res = session.get(pic_url)
        if res.status_code == 200:
            # 求取图片的md5值，作为文件名，以防存储重复的图片
            md5_obj = hashlib.md5()
            md5_obj.update(res.content)
            md5_code = md5_obj.hexdigest()
            file_name = myConfig.imgPath + str(md5_code) + ".jpg"
            # 如果图片不存在，则保存
            if not os.path.exists(file_name):
                with open(file_name, "wb") as f:
                    f.write(res.content)
            return file_name
        else:
            log.warning("in func save_pic_to_disk(), fail to save pic. pic_url: " + pic_url +
                                      ", res.status_code: " + str(res.status_code))
            raise Exception
    except Exception as e:
        log.error(e)


if __name__ == "__main__":
    # dic = loadCookies()
    # print(dic)

    # token = getAccessToken()
    # fileName = 'resources/captchas/captcha.jpg'
    # text = getTextFromPic(fileName)
    path = 'resources/captchas/'
    li = os.listdir(path)
    for entry in li:
        text = getTextFromPic(path+entry)
        print(text)