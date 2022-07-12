from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from proxy import main


def service_page(driver, url_al):
    driver.get(url_al)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(3)
    service_input = driver.find_element_by_id("tramiteGrupo[1]")
    time.sleep(3)
    service_input.click()
    time.sleep(3)
    myDDList = Select(driver.find_element_by_id("tramiteGrupo[1]"))
    print("Find Element")
    time.sleep(3)
    myDDList.select_by_value("4010")
    print("Select Value")
    time.sleep(4)
    first_accept_button = driver.find_element_by_id("btnAceptar")
    first_accept_button.click()
    time.sleep(4)


def accept_rules_page(driver, url_al):

    second_accept_button = driver.find_element_by_id("btnEntrar")
    second_accept_button.click()
    time.sleep(13)


def nie_page(driver, url_al):

    nie_input = driver.find_element_by_id("txtIdCitado")
    nie_input.clear()
    nie_input.send_keys("Y8675971V")
    time.sleep(10)
    name_input = driver.find_element_by_id("txtDesCitado")
    name_input.clear()
    name_input.send_keys("Masha Rasterasha")
    time.sleep(9)
    nation_choice = driver.find_element_by_id("txtPaisNac")
    time.sleep(2)
    nation_choice.click()
    time.sleep(3)
    myList = Select(driver.find_element_by_id("txtPaisNac"))
    myList.select_by_value("351")
    third_accept_button = driver.find_element_by_id("btnEnviar")
    third_accept_button.click()
    time.sleep(10)


def accept_rules_second_page(driver, url_al):
    third_accept_button = driver.find_element_by_id("btnEnviar")
    third_accept_button.click()
    time.sleep(10)


# TODO delete global variables
good_cita = 0
bad_cita = 0


def cita_avaliable(driver, url_al):

    try:
        cita = driver.find_element_by_id("idSede")
        if cita:
            global good_cita
            print("We find cita!")
            good_cita += 1
            print("Today we found good citas: ", good_cita)
    except Exception as ex:
        global bad_cita
        print("No cita, sorry")
        bad_cita += 1
        print("We try ", bad_cita, " times")


def start_bot(proxy):

    print("StartBot with proxy: ", proxy)
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(
        executable_path="/home/asus/Desktop/citabot/chromedriver/chromedriver", options=driver_options)
    driver.maximize_window()
    url = "https://icp.administracionelectronica.gob.es/icpplus/citar?p=2&locale=es"
    url_al = "https://icp.administracionelectronica.gob.es/icpco/citar?p=3&locale=es"
    service_page(driver, url_al)
    accept_rules_page(driver, url_al)
    nie_page(driver, url_al)
    accept_rules_second_page(driver, url_al)
    cita_avaliable(driver, url_al)


count_run = 1
while True:
    print(f"[*] Loading-proxy..")
    proxies = main()
    for count_proxy, proxy in enumerate(proxies):

        print(f"[*] Proxy data: {proxy}")
        print(f"[+] Script run: {count_run}, time")
        print(f"[+] Proxy: {count_proxy}")
        count_run += 1
        print(proxy)
        print("today we found good citas: ", good_cita)
        print("we try to find cita ", bad_cita, " times")

        try:
            start_bot(proxy)
        except Exception as ex:
            print(ex)
