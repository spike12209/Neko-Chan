import aiodns,asyncio
from functions import logger
from pprint import pprint

DESC="Gets the DNS-Records for a Domain"
USAGE="dig [type] domain"

loop = asyncio.get_event_loop()
types=["A","AAAA","CNAME","MX","NAPTR","NS","PTR","SOA","SRV","TXT"]
async def init(bot):
    try:
        if len(bot.args) == 0:
            await bot.sendMessage( "You have to specify a domain!")
            return False
        if len(bot.args)>1:
            if not bot.args[0].upper() in types:
                await bot.sendMessage( "Unknown DNS entry type.")
                return False
            type = bot.args[0].upper()
            domain = bot.args[1]
        else:
            domain=bot.args[0]
            type = "A"
        try:
            resolver = aiodns.DNSResolver()
            f = await resolver.query(domain,type)
        except Exception as e:
            if "answer with no data" in str(e):
                await bot.sendMessage("There are no NS entries for {} with type {}".format(domain,type))
                return False
            if "name not found" in str(e):
                await bot.sendMessage( "Can't resolve the domain {}".format(domain))
                return False
            logger.PrintException(bot.message)
        result = ""
        for item in f:
            if type == "MX":
                result+="{}.     {}     IN     {}     {} {}\r\n".format(domain,item.ttl,type,item.priority,item.host)
            else:
                if type == "NS":
                    result+="{}.     IN     {}     {}\r\n".format(domain,type,item.host)
                else:
                    result+="{}.     {}     IN     {}     {}\r\n".format(domain,item.ttl,type,item.host)
        await bot.sendMessage( result)
    except:
        logger.PrintException(bot.message)
