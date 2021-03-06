from telethon import TelegramClient, events, sync
import re
import requests
import pyshorteners
import os

api_id = 1601965
api_hash = 'a8ea394b73cd8d7df7a955e6be7643b2'

client = TelegramClient('anon', api_id, api_hash)

my_channel = -1001408071194
host_channel = -1001380024851
#host_channel = -1001259793382
target_channel = -485269698


def unshorten_url(url):
    return requests.head(url, allow_redirects=True).url


def amz_aff(url):
    if re.search(r'(\&|\?)tag=+[a-zA-Z0-9]+-21', url):
        return re.sub(r"tag=+[a-zA-Z0-9]+-21", "tag=node17-21", url)
        # output = re.search(r"(?<=tag).*?(?=-21)", url).group(0)
        # return url.replace(output, '=node17')
    elif re.search(r'(\&|\?)linkCode=+[a-zA-Z0-9]+\&', url):
        return url + "&tag=node17-21"
    else:
        return url + "&linkCode=sl1&tag=node17-21"


def fk_aff(url):
    x = re.search(r"affid=+[a-zA-Z0-9]+", url)
    if x:
        a = re.sub(r"affExtParam(1|2)=+[a-zA-Z0-9]+", '', url)
        b = re.sub(r"affid=+[a-zA-Z0-9]+", 'affid=syedimran', a)
        return b
    else:
        a = url + '&affid=syedimran'
        return re.sub(r'/itm[a-zA-Z0-9]+\&', r'/itm[a-zA-Z0-9]+\?', a)


def short_url(url):
    s = pyshorteners.Shortener(api_key='23dea256440ca121bbb2d80492d153c9c5c827ee')
    short = s.bitly.short(url)
    return short

def ekro(url):
    base_ekaro_url = requests.get(url).text
    ek_link = re.findall(r'cashbackUrl = .*;', base_ekaro_url)
    ekro_amz_link = (ek_link[0].replace('cashbackUrl =', '').replace('"', '').replace(';', '').strip())
    return ekro_amz_link


def proper_url(url):
    if 'amzn.to' or 'fkrt.it' or 'bit.ly' in url:
        return unshorten_url(url)
    else:
        return url


def final_link(link):
    if 'amazon.in' in link:
        a = amz_aff(link)
        return short_url(a)
    elif 'ekaro' in link:
        a = ekro(link)
        if 'amazon.in' in a:
            b = amz_aff(a)
            return (short_url(b))
        elif 'flipkart' in a:
            b = fk_aff(a)
            return short_url(b)
    elif 'flipkart' in link:
        a = fk_aff(link)
        return short_url(a)
    else:
        return (f'Non Aff Url: {link}')


def prod_link(link):
    z = proper_url(link)
    return final_link(z)


def listToString(s):
    out = "\n"
    return (out.join(s))


@client.on(events.NewMessage(chats=host_channel))
async def my_event_handler(event):
    a = event.raw_text
    buffer = a.splitlines()
    for i, matter in enumerate(buffer):
        if 'http' in matter:
            pl = re.search("(?P<url>https?://[^\s]+)", matter).group()
            x = final_link(proper_url(pl))
            buffer[i] = (matter.replace(pl, x))

        else:
            buffer[i] = matter
    msg = listToString(buffer)
    msg_new = re.sub(r"(????)", '\n', msg)
    print(msg_new)
    await client.send_message(
        target_channel,
        msg_new,
        link_preview=False)


client.start()
client.run_until_disconnected()
