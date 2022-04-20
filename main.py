from flask import Flask, request, render_template
from datetime import datetime

application = Flask(__name__)  # Создаем Flask-приложение
# Начинаем писать мессенджер
all_messages = []  # Список всех сообщений


@application.route("/chat")
def display_chat():
    return render_template("form.html")  # Показываем файл из папки templates


@application.route("/")
def index_page():
    return "Hello, welcome to Skillbox Chat"


@application.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@application.route("/send_message")
def send_message():
    # name, text ?
    # Получаем информацию от пользователя
    sender = request.args["name"]
    text = request.args["text"]

    # Очистим пользовательский ввод от лишнего
    sender = sanitizer(sender)
    text = sanitizer(text)

    # Проверим текст на длинну и если не так - выводим ошибку в чат
    if not 0 < len(text) < 1000:
        text = '[ERROR] Текст должен быть в диапазоне от 1 до 1000 символов'

    # Проверим имя на длинну и если не так - удалим текст и выведем ошибку в чат
    # ибо нечего от всяких анонимов тексты выводить
    if not 2 < len(sender) < 100:
        sender = f'[ERROR] Имя \'{sender}\' должно быть в диапазоне от 3 до 100 символов'
        text = ''

    # Добавляем сообщение в список
    add_message(sender, text)
    return "OK"


# Пример очистки пользовательского ввода
def sanitizer(text_data):
    # Словарь лишнего, что лучше исключить из вывода в HTML-форме во избежание XSS
    # todo: дополнить или почитать про WTForms
    vulnerable = ['<', '&lt;', '>', '&gt;', '&', '&amp;', '\u003c', '\u003e']
    for vuln in vulnerable:
        text_data = text_data.replace(vuln, '')
    return text_data


def add_message(sender, text):
    # 1. Подготовить словарь с данными сообщения
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    # 2. Добавить получившийся словарь в список всех сообщений
    all_messages.append(new_message)


def print_message(mess):
    print(f"[{mess['sender']}]: {mess['text']} / {mess['time']}")


# add_message("Миша", "Всем приветы")
# add_message("Вася", "Библиотека Flask скачать бесплатно")
#
# for message in all_messages:
#     print_message(message)

application.run()  # Запускаем приложение

#  ДЗ:
#  Предусмотреть ограничения для имени и текста (валидация данных) в фунции add_message

#  День 3:
#  Подгтовить код к размещению на хостинге
#  Настроить хостинг и запустить там чат
#  Сохранение сообщений в файл
