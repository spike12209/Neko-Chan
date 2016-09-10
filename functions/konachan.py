import random
from random import randint
from functions import logger
import json
import asyncio
import aiohttp

cooldown_arr = {}

def gelbooru(tag):
    count = 0
    try:
        result = urllib2.urlopen(
            "http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=1000&tags=-censored+" + tag).read()
        result2 = soup(result).findAll('post')
        count = len(result2)
        if count > 0:
            post = random.choice(result2)
            post_attrs = dict(post.attrs)
            imgurl = post_attrs['file_url']
            return imgurl
        else:
            return False
    except:
        logger.PrintException()
        return False


def yandere(tag):
    count = 0
    try:
        req = urllib2.Request("https://yande.re/post/index.json?limit=1000&tags=-censored+" + tag, headers={
                              'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
        result = urllib2.urlopen(req).read()
        result = json.loads(result)
        count = len(result)
        if count > 0:
            randomint = randint(0, count - 1)
            #id = (result[randomint]['id'])
            imgurl = (result[randomint]['jpeg_url'])
            return imgurl
        else:
            return False
    except:
        logger.PrintException()
        return False


async def select(tag):
    count = 0
    try:
        #result = urllib2.urlopen("http://konachan.com/post/index.json?site=1&limit=1000&tags=-censored+" + tag).read()
        url = "http://konachan.com/post/index.json?site=1&limit=1000&tags=-censored+{}".format(tag)
        with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                r = await req.text()
                result = json.loads(r)
                count = len(result)
                if count > 0:
                    randomint = randint(0, count - 1)
                    #id = (result[randomint]['id'])
                    imgurl = (result[randomint]['jpeg_url'])
                    return imgurl
                else:
                    return None
    except:
        logger.PrintException()
        return None


def randomloli():
    r = requests.get(
        "http://konachan.com/post/index.json?site=1&limit=1000&tags=-censored+loli")
    result = r.json
    randomint = randint(0, len(result) - 1)
    #id = (result[randomint]['id'])
    imglink = (result[randomint]['jpeg_url'])
    return imglink


def randomcat():
    r = requests.get(
        "http://konachan.com/post/index.json?site=1&limit=1000&tags=-censored+catgirl")
    result = r.json
    randomint = randint(0, len(result) - 1)
    #id = (result[randomint]['id'])
    imglink = (result[randomint]['jpeg_url'])
    return imglink
