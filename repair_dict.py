# Скрипт пересобирает словарь с анекдотатами, чтобы в случае удаления или добавления анекдота ключи шли по порядку

import json

with open('kids_anekdot.json', mode='r', encoding='utf-8') as file:
    old_dict = json.load(file)

old_list = list(old_dict.values())          # Делаем список из значений словаря
len_old_list = len(old_list)


new_dict = {i + 1: old_list[i] for i in range(len_old_list)}    # Формируем новый словарь с непрерывными ключами

with open('kids_anekdot.json', mode='w', encoding='utf-8') as file:
    json.dump(new_dict, file, indent=4, ensure_ascii=False)

# with open('new_anekdot.json', mode=) !!


print(new_dict)
