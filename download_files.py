from datetime import datetime
import requests
import time
from datetime import datetime
from random import choice, randint
from select import error
from urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = 'https://api.thecatapi.com/v1/images/search'
ua = UserAgent()

i = 1001
while i < 2001:
    try:
        print(f'Котик № {i}')
        #try:
        fake_ua = {'user-agent': ua.chrome}
        response = requests.get(url, verify=False, headers=fake_ua)
        response.encoding = 'utf-9'
        if not response.json()[0]['url']:
            print(response.text + 'Это при КРИВОМ АДРЕСЕ КАРТИНКИ')
            time.sleep(10)

        #except requests.exceptions.RequestException as e:
            #print(response.text)
            #print(e + 'Это при запросе АДРЕСА картинки')
        #    time.sleep(50)
        print(response.text  + 'Это при НОРМАЛЬНОЙ работе')
        cat_img_url = response.json()[0]['url']
        date_number = datetime.today().strftime('%Y-%m-%dT%H_%M_%S_%f')[:-3]

        #try:
        response_with_cat = requests.get(cat_img_url, verify=False,  headers=fake_ua)
        response_with_cat.encoding = 'utf-8'
        #except requests.exceptions.RequestException as er:
            #print(response_with_cat.text)
        #    print(er + 'Это при запросе САМОЙ КАРТИНКИ')
        #    time.sleep(50)

        if response.status_code == 200:
            with open(f'cat_images/{i}.jpg', 'wb') as file:
                file.write(response_with_cat.content)
            print('Пикча ссэйвена')
        else:
            print('Ошибка при запросе:', response.status_code)
        #i += 1
        time.sleep(1.3)
        i += 1
    except requests.exceptions.RequestException as e:
        i = i                                              # Если ошибка загрузки картинки, то счетчик остается прежним
        print(e)                                           # и очередность имен файлов сохраняется
        time.sleep(8)
