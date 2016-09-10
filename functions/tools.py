from bs4 import BeautifulSoup
from functions import logger, tools
import shlex
import hashlib
import datetime
import calendar
import re
import json
import time
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from pydoc import locate
from urllib.parse import urlsplit
import global_vars

access_token = ""
access_expire = 0
voiceCache = []

def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    """
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec

def convertVal(type,value):
    type = locate(type)
    if type == bool:
        return value.lower() in ["yes","1","true", "allow"]
    else:
        sparse = ignore_exception(ValueError)(type)
        return sparse(value)

def getBetween(source, start, stop):
    data = re.compile(start + '(.*?)' + stop).search(source)
    if data:
        found = data.group(1)
        return found.replace('\n', '')
    else:
        return False


def sub_days(today, sdays):
    past = today - datetime.timedelta(days=sdays)
    return past


def md5(string):
    return hashlib.md5(string).hexdigest()

async def isUP(url):
    try:
        url = 'http://www.downforeveryoneorjustme.com/{}'.format(url)
        with aiohttp.ClientSession() as session:
            async with session.get(url) as source:
                source = await source.text()
                if source.find('It\'s just you.') != -1:
                    return 'The website is up'
                elif source.find('It\'s not just you!') != -1:
                    return 'The website is down'
                elif source.find('Huh?') != -1:
                    return 'Invalid URL'
                else:
                    return 'UNKNOWN'
    except:
        logger.PrintException()
        return 'UNKNOWN ERROR'


async def getURLTitle(url):
    try:
        with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                parser = BeautifulSoup(await r.text(), "html.parser")
                return parser.title.string
    except:
        logger.PrintException()
    return None

async def excuse():
    with aiohttp.ClientSession() as session:
        async with session.get("http://codingexcuses.com/", headers={'Accept':'application/json'}) as r:
            r = await r.text()
            r = json.loads(r)
            return r['excuse']

async def unshort(url):
    try:
        urls = [
        "t.co",
        "goo.gl",
        "bit.ly",
        "tinyurl.com",
        "ow.ly",
        "migre.me",
        "ff.im",
        "tiny.cc",
        "flic.kr",
        "l.gg",
        "sn.im"]
        if "{0.netloc}".format(urlsplit(url)) in urls:
            with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}) as session:
                async with session.get(url) as source:
                    return source.url
        else:
            return None
    except:
        logger.PrintException()
        return 'UNKNOWN ERROR'


async def btcrate(currency='USD'):
    url = "https://api.bitcoinaverage.com/ticker/global/{}/".format(currency)
    with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 404:
                return False
            else:
                r = await r.text()
                r = json.loads(r)['last']
                return float(r)

def ytid(url):
    youtube_regex = (
        r'(https?://)?(www\.)?' '(youtube|youtu|youtube-nocookie)\.(com|be)/' '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match

async def mal_anime(name):
    try:
        url = "https://myanimelist.net/api/account/verify_credentials.xml"
        basicauth = aiohttp.BasicAuth(login=global_vars.myanimelist['user'], password=global_vars.myanimelist['password'], encoding='utf8')
        with aiohttp.ClientSession(auth=basicauth) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    url = "https://myanimelist.net/api/anime/search.xml?q={}".format(name)
                    async with session.get(url) as resp2:
                        return await resp2.text()
                else:
                    return None
    except:
        logger.PrintException()
        return None
        
async def mal_manga(name):
    try:
        url = "https://myanimelist.net/api/account/verify_credentials.xml"
        basicauth = aiohttp.BasicAuth(login=global_vars.myanimelist['user'], password=global_vars.myanimelist['password'], encoding='utf8')
        with aiohttp.ClientSession(auth=basicauth) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    url = "https://myanimelist.net/api/manga/search.xml?q={}".format(name)
                    async with session.get(url) as resp2:
                        return await resp2.text()
                else:
                    return None
    except:
        logger.PrintException()
        return None
        
async def fetch_rss(url):
    try:
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    return None
    except:
        logger.PrintException()
        return None
