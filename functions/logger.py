import sys
import sqlite3
import re
import os
import aiofiles
from time import localtime, strftime
import linecache
from functions import botfunc
import asyncio
import global_vars
from pprint import pprint

def printtf(message):
    yield from print_to_file(message)

async def print_to_file(message):
    # file = os.path.join(global_vars.cwd, global_vars.log_dir, global_vars.log_file)
    # async with aiofiles.open(file, mode='a') as f:
        # await f.write("{}\r\n".format(message))
    print(message)

def PrintException(message=None):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    filename = filename.replace(global_vars.cwd,"")
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    time = strftime("%H:%M:%S", localtime())
    #line = '[' + str(time) + '] {} IN ({}:{} -> "{}"): {}'.format(exc_type.__name__, filename, lineno, line.strip(), exc_obj)
    report = "**Bug report**:\r\n"
    report += "Reported by: Exception catcher\r\n"
    if message is not None:
        if message.server is not None:
            report += "Server: `{}` (ID: {})\r\n".format(message.server.name, message.server.id)
        if message.author is not None:
            report += "Author: `{}#{}` (ID: {})\r\n".format(message.author.name, message.author.discriminator, message.author.id)
    report += "Time: {}\r\n".format(time)
    report += "Type: `{}`\r\n".format(exc_type.__name__)
    report += "Exception: `{}`\r\n".format(exc_obj)
    report += "File: `{}:{}`\r\n".format(filename, lineno)
    report += "Line: `{}`\r\n".format(line.strip())
    if message is not None:
        report += "Executed command: {}".format(message.content[:1000])
    print(report)

def GetException():
    try:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        filename = filename.replace(global_vars.cwd,"")
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        time = strftime("%H:%M:%S", localtime())
        line = '[' + str(time) + '] {} IN ({}:{} -> "{}"): {}'.format(exc_type.__name__, filename, lineno, line.strip(), exc_obj)
        return line
    except:
        PrintException()


def debug(msg):
    time = strftime("%H:%M:%S", localtime())
    yield from printtf("[" + str(time) + "] " + str(msg).encode("UTF-8"))


def edit_log(chat, sender, message, messageid):
    try:
        # =============== SQLITE WAY ===============
        try:
            time = strftime("%H:%M:%S", localtime())
            yield from printtf("[" + str(time) + "] [EDITED] " +
                  sender.encode("UTF-8") + ": " + message.encode("UTF-8"))
            con = False
            topic = skype.name(chat)
            con = sqlite3.connect('files/' + topic + '.db')
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender VARCHAR(100), display VARCHAR(100), message TEXT(1000), date VARCHAR(150))")
            cur.execute(
                "UPDATE messages SET message=message || '\n[EDITED] ' || ? WHERE id=?", (message, messageid))
            con.commit()
        except sqlite3.Error as e:
            PrintException()
        finally:
            if con:
                con.close()
    except:
        PrintException()

