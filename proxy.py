from time import sleep
from requests import get
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import aiohttp
import asyncio
import multiprocessing


# pip3 install fake-useragent
# pip3 install BeautifulSoup4

# False - Отключает логирование
# True - Включает логирование
log = True

# Агент-запрос
userAgent = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"}


async def get_proxy_from_api(proxy_type: str) -> list:
    """Получает тип проки далее парсинг (Ассинхрон)
    ---------------
    :param: proxy_type: ONLY-STR
    :param: proxy_type: `http` - Список из HTTP
    :param: proxy_type: `https` - Список из HTTP / HTTPS
    :param: proxy_type: `s4` - Список из SOCKS4
    :param: proxy_type: `s45` - Список из SOCKS4 / SOCKS5
    
    :return proxy_list: list
    """
        
    pagination = 0
    proxy_list = []
    if log == True:
        print("[#] Сборка прокси..")
        sleep(1.5)

    site_proxy = get('https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=1900&country=all&anonymity=no&ssl=yes').text.split('\r\n')[:-1]
    [proxy_list.append(f'{sit_proxy}') for sit_proxy in site_proxy]

    if log == True:
        print(f"[*] {len(proxy_list)} прокси уже есть..")
        sleep(1.5)


    while True:
        url = f'https://hidemy.name/ru/proxy-list/?maxtime=2700&type={proxy_type}&start={pagination}'
    
        async with aiohttp.ClientSession(trust_env=True) as session:  
            if pagination == 50:
                break          
            page = await session.get(url, ssl=False, headers=userAgent)
            site = bs(await page.text(), 'html.parser')        
            tbody = site.find('tbody')
    
            for tr in tbody.find_all('tr'):                
                ip = tr.find('td').text
                port = tr.find('td').findNext().text
                if log == True:
                    print(f"[+] {ip}:{port} - Новый")

                proxy_list.append(f'{ip}:{port}')

            if not tbody.text.split():
                break

            else:
                pagination += 64

    return proxy_list


def check_proxy(proxy_addr: str):
    """Проверяет прокси на валидность делая запрос на сайт.
    - Если прокси не работает то возвращаеться False
    - Если прокси таботает то возвращает True

    ----------------
    :param: proxy_addr: str (ip:port)
    :return: proxy_addr: str (ip:port)
    """

    try:
        runner = f"http://{proxy_addr}"
        res = get(
            url="https://api.ipify.org?format=json",
            proxies={"http": runner, "https": runner},
            headers=headers, timeout=1.5)

        res.raise_for_status()
        if log == True:
            print(f"[+] {proxy_addr} - Работает")
        
        return (proxy_addr, True)

    except Exception as err:
        if log == True:
            print(f"[!] {proxy_addr} - Не работает")

        return (proxy_addr, False)


def main():
    """ Главная функция к запуску.
    --------------
    - Получает прокси (парс/str)
    - Делает запрос к чекеру и получает ответ (True/False)"""

    proxies = asyncio.run(get_proxy_from_api("http")) #getproxies()
    if log == True:
        sleep(1.5)
        print(f"\n[=] Загрузка {len(proxies)} прокси..")

    good_proxies = []
    with multiprocessing.Pool() as pools:
        if log == True:
            print(f"[+] Проверка добытых {len(proxies)} прокси..")
            sleep(1.5)

        for proxy_addr, result in pools.imap_unordered(check_proxy, proxies, chunksize=8):
            if result:
                good_proxies.append(proxy_addr)
    
    if log == True:
        print(f"\n[*] Всего {len(good_proxies)} работающих прокси..")
   
    return good_proxies

if __name__ == "__main__":
    """ Для вкл/откл логгирования нужно изменить
    значние на первой строке кода (log=True/False)"""

    main()
