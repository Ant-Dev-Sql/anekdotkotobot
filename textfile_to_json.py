# Скрипт делает из текстового файла файл json, где ключи идут от 1 до кол-ва строк, а значений ключей - строки файла
import json
import time
from dataclasses import replace

with open('adult_anekdot.txt', mode='r', encoding='utf-8') as file:

    adult_anekdot_dict = {}

    i = 1
    for line in file:
        # тут убираются лишние кавычки и приводятся к нормальному виду диалоги
        adult_anekdot_dict[i] = line.replace('\'', '').replace(',\n', '').replace('.-', '.\n-').replace('?-', '?\n-').replace('!-', '!\n-').replace(':-', ':\n-')
        i += 1
        #time.sleep(1)

with open('adult_anekdot_part_1.json', mode = 'w', encoding='utf-8') as file:
    json.dump(adult_anekdot_dict, file, ensure_ascii=False, indent=4)

print(adult_anekdot_dict[83429])
#print(adult_anekdot_dict)!!