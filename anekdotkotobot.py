import json
import random
import pyodbc
import time
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile  # Используем FSInputFile вместо InputFile

BOT_TOKEN = '7790039133:AAFR0RDWpVcL348npNuJI6jNBqRM3aEk-Ik'

# Словарь с фразами котиков
cat_phrases = ['Я тут главный!', 'Погладь меня!', 'У меня лапки!', 'Смотри, какой я пушистый!', 'Поклоняйся мне!',
               'Я – грация, я – мощь!', 'Ты видел мой хвост? Он идеален!', 'Я пришёл за вкусняшками!', 'Мур-мур-мур!',
               'Я не сплю, я… жду!', 'Где еда?', 'Открой дверь!', 'Освободи место!', 'Это моё!', 'Ты уже покормил меня?',
               'Я решаю, когда уходить!', 'Чего смотришь? Дай печеньку!', 'Я не спал, я проверял веки на прочность!',
               'Ты должен служить мне!', 'Мне нужно внимание. Сейчас!', 'Привет, человечек!', 'Я так по тебе скучал!',
               'Обнимашки?', 'Тыыы мой человек!', 'Люблю тебя… но не показываю!', 'Я пришёл погреться!', 'Мур-мур-твой!',
               'Ты пахнешь вкусно… как рыбка!', 'Я твой маленький комочек счастья!', 'Давай посидим вместе?',
               'Я знаю то, чего не знаешь ты…', 'Ночью я правлю миром!', 'Тыыы спишь? А я нет!',
               'Я вижу тебя во сне… и сужу!', 'Зачем будишь? Я медитировал!', 'Я – тень в ночи… и свет в твоей жизни!',
               'Ты думаешь, это твой дом? Ха!', 'Я пришел из космоса… за тунцом!', 'Мой взгляд – твоя судьба!',
               'Я – вечность в пушистой обёртке!', 'Саркастичные и вредные', 'Опять работаешь? Скучно!',
               'Я разбросал твои вещи… для твоего же блага!', 'Ты убрал? А я уже набросал!', 'Это не я! (Это я.)',
               'Ты зовёшь меня? Я игнорирую!', 'Мяу – это всё, что ты заслуживаешь!',
               'Я сломаю этот цветок… просто потому что могу!', 'Ты купил новую мебель? Отлично, поточу когти!',
               'Я не толстый, я бодипозитивный!', 'Ты думал, это твой стул? Смешно!',
               'Я умираю… от голода… уже пять минут!', 'Никто меня не любит… (пока не дашь вкусняшку)!',
               'Меня забыли… предали… (хотя ты просто вышел в туалет)!', 'Я – король! А ты – мой слуга!',
               'В этом доме всё для меня… даже ты!', 'Я не просил рождаться таким милым!',
               'Я – загадка, которую ты никогда не разгадаешь!', 'Я не просыпаюсь рано… я жертвую своим сном ради тебя!',
               'Ты смеешь гладить других котиков? Измена!', 'Я не сплю, я… экономлю энергию!',
               'Я не ленивый, я энергосберегающий!', 'Моя работа – лежать. И я профессионал!',
               'Ты хочешь поиграть? Я хочу поспать!', 'Сон – моя вторая любимая вещь… после еды!',
               'Я не кот… я пушистый инопланетянин!', 'Мяу-покажи-где-тут-рыба!',
               'Я не влезаю в коробку… но попробую ещё раз!', 'Мой хвост – мой личный враг!',
               'Я упал… но это был трюк!', 'Я не толстый, это шерсть пушится!', 'Я не мяукал, это ветер!',
               'Я не тыгыдыкал по ночам… это призраки!', 'Я – кот, а значит, я всегда прав!', 'Мяу...', 'Мур мур...']

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

kb_builder = ReplyKeyboardBuilder()

# Создаем объекты кнопок
button_text_get_joke = '😄рассказать анекдот😄'
button_text_get_cat = '😸прислать котика😸'

button_get_joke = KeyboardButton(text=f'{button_text_get_joke}')
button_get_cat = KeyboardButton(text=f'{button_text_get_cat}')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard = ReplyKeyboardMarkup(keyboard=[[button_get_joke], [button_get_cat]], resize_keyboard=True)

try:
    # conn = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; trusted_connection=no; UID={2}; PWD={3}".format('172.18.27.124','AnekdotKidBot','sa','Ms0987654321!'))
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=172.18.27.124;"
        "DATABASE=AnekdotKotoBot;"
        "UID=sa;"
        "PWD=Ms0987654321!;"
    )
except pyodbc.OperationalError:
    print('Ахтунг, че-то с базой!!!')

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Привет! Хочешь посмеяться и умилиться?\n\n'
                              'АнекдотКотоБот знает сотни смешных шуток, а ещё дарит милые картинки котиков!\n\n'
        'Каждый раз — свежий анекдот или котик, и никаких повторов.\n '
        f'Чтобы получить шутку нажми кнопку:\n "{button_text_get_joke}"\n\n'
        f'Чтобы получить котика нажми кнопку:\n "{button_text_get_cat}"',
        reply_markup=keyboard
        )

# with open('kids_anekdot_small_test.json', mode='r', encoding='utf-8') as file:
with open('kids_anekdot.json', mode='r', encoding='utf-8') as file:
    anekdot_dict_str = json.load(file)          # Из файла json делаем словарь с анекдотами (ключи пока строки)

anekdot_dict_int = {}                            # Меняем ключи словаря со строк на инты
for key, value in anekdot_dict_str.items():
    anekdot_dict_int[int(key)] = anekdot_dict_str[key]

########################################################################################################################

#Функция случайного выбора анекдота, и записи в базу id анекдота и данных пользователя
def get_joke(user_id: int, first_name, last_name, user_name):    # user_id и имена пользователя тг, будет браться во время обращения пользователя к боту
    set_keys_full = set(anekdot_dict_int.keys())  # Множество со всеми ключами словаря с анекдотами

    cursor_read = conn.cursor()
    query_select = f"select joke_id from users_jokes where user_id = {user_id}"   # Выбираем из базы использованные id анекдотов
    cursor_read.execute(query_select)

    set_keys_used = set(j[0] for j in list(cursor_read))        # Множество с ключами прочитанных анекдотов
    conn.commit()

    set_keys_work = set_keys_full - set_keys_used                   # Множество с ключами, из которых можно еще выбирать
    #print(f'set_keys_full = {(set_keys_full)}\n set_keys_used = {(set_keys_used)}\n set_keys_work = {set_keys_work}\n')

    try:                                                            # Обработка исключения на случай если все анекдоты прочитаны, т.к. из пустого списка нельзя случайно выбрать (х.з. почему)
        key_joke = random.choice(list(set_keys_work))               # Случайный выбор id анекдота из рабочего набора
    except IndexError:
       return 'Ну ты индеец БОМБОМ, все прочитал'
    print(f'user_id = {user_id}, key_joke = {key_joke}  \n{anekdot_dict_int[key_joke]}\n')

    cursor_write = conn.cursor()
    query_insert = (f'insert into users_jokes (user_id, joke_id, first_name, last_name, user_name) '
                    f'values ({user_id}, {key_joke}, \'{first_name}\', \'{last_name}\', \'{user_name}\')') # Заносим в базу выбранный из рабочего списка id анекдота и данные пользователя ТГ
    cursor_write.execute(query_insert)
    conn.commit()
    return f'{key_joke}\n {anekdot_dict_int[key_joke]}'

########################################################################################################################

#Функция случайного выбора картинки, и записи в базу имя файла (с расширением или без) и данных пользователя

#Функция случайного выбора анекдота, и записи в базу id анекдота и данных пользователя
def get_cat(user_id: int, first_name, last_name, user_name):    # user_id и имена пользователя тг, будет браться во время обращения пользователя к боту
    set_files_full = set(range(1, 1400))  # Множество с именами файлов (без расширений)

    cursor_read = conn.cursor()
    query_select = f"select file_id from users_cats where user_id = {user_id}"   # Выбираем из базы использованные id анекдотов
    cursor_read.execute(query_select)

    set_files_used = set(j[0] for j in list(cursor_read))        # Множество с ключами прочитанных анекдотов
    conn.commit()

    set_files_work = set_files_full - set_files_used                   # Множество с ключами, из которых можно еще выбирать
    #print(f'set_keys_full = {(set_keys_full)}\n set_keys_used = {(set_keys_used)}\n set_keys_work = {set_keys_work}\n')

    try:                                                            # Обработка исключения на случай если все анекдоты прочитаны, т.к. из пустого списка нельзя случайно выбрать (х.з. почему)
        key_file = random.choice(list(set_files_work))               # Случайный выбор id анекдота из рабочего набора
    except IndexError:
       return 'Ну ты индеец БОМБОМ, все прочитал'
    print(f'user_id = {user_id}, key_file = {key_file} \n')

    cursor_write = conn.cursor()
    query_insert = (f'insert into users_cats (user_id, file_id, first_name, last_name, user_name) '
                    f'values ({user_id}, {key_file}, \'{first_name}\', \'{last_name}\', \'{user_name}\')') # Заносим в базу выбранный из рабочего списка id анекдота и данные пользователя ТГ
    cursor_write.execute(query_insert)
    conn.commit()
    return key_file


@dp.message(Command(commands='getjoke'))
async def process_getjoke_command(message: Message):
    user_id = message.from_user.id                      # Берем данные пользователя ТГ
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    await message.answer(
        f'{user_id}, {get_joke(user_id, first_name, last_name, username)}'
    )

@dp.message(F.text.lower() == f'{button_text_get_joke}')
async def process_getjoke_command(message: Message):
    user_id = message.from_user.id                      # Берем данные пользователя ТГ
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    await message.answer(
        f'{get_joke(user_id, first_name, last_name, username)}'
    )

@dp.message(F.text.lower() == f'{button_text_get_cat}')
async def process_getcat_command(message: Message):
    user_id = message.from_user.id                      # Берем данные пользователя ТГ
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    # await message.answer(
    #     f'{get_cat(user_id, first_name, last_name, username)}'
    # )
    # await message.reply_photo(f'{get_cat(user_id, first_name, last_name, username)}.jpg')
    #with open('cat_images/1.jpg', 'rb') as photo:
    photo = FSInputFile(f'cat_images/{get_cat(user_id, first_name, last_name, username)}.jpg')
    # await message.reply_photo(photo)
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f'{random.choice(cat_phrases)}')


if __name__ == '__main__':
    dp.run_polling(bot)

conn.close()
