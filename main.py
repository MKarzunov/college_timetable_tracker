import requests
import bs4
import telebot
import time
import logging

def get_announcements():
    sess = requests.Session()

    with open("credentials", 'r') as credentials_file:
        data = credentials_file.read().split()
        login = data[0]
        password = data[1]

    sess.post("https://portal.petrocollege.ru/lk/login/",
              data={"USER_LOGIN": login, "USER_PASSWORD": password, "AUTH_ACTION": "Войти"})

    response = sess.get("https://portal.petrocollege.ru/department-of-distance-learning/ads/")

    if "Карзунов" not in response.text:
        return

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    announcements = soup.find_all(class_="announcements__element news__col")
    return announcements

def check_announcements(announcements: list, old_announcements: list) -> tuple[str, list]:
    if announcements is None:
        return 'LoginError', []
    if announcements[0] == old_announcements[0]:
        return 'NoUpdates', []
    for old_index in range(len(old_announcements)):
        for new_index in range(len(announcements)):
            if old_announcements[old_index] == announcements[new_index]:
                break
        else:
            continue
        break
    else:
        return 'NoEqualityFound', announcements
    return 'EqualityFound', announcements[:new_index]


if __name__ == '__main__':
    try:
        logging.basicConfig(filename='log.log', level=logging.INFO)

        logging.info("Program started")

        with open("telegram_bot_token", 'r') as token_file:
            token = token_file.read()

        bot = telebot.TeleBot(token = token)

        @bot.message_handler(commands=['start'])
        def start_bot(message):
            chat_id = message.chat.id
            bot.send_message(chat_id, "Бот запущен")
            old_announcements = [None]
            while True:
                new_announcements = get_announcements()
                status, announcements = check_announcements(new_announcements, old_announcements)
                if status == 'LoginError':
                    logging.error("Login failed")
                if status == 'NoUpdates':
                    logging.info("No updates found")
                else:
                    logging.info(status)
                    if status == 'NoEqualityFound':
                        bot.send_message(chat_id, "Не обнаружено совпадений, отправляю все последние новости")
                    else:
                        bot.send_message(chat_id, "Обнаружены новости")
                    for announcement in announcements:
                        bot.send_message(chat_id, announcement.text)
                old_announcements = new_announcements
                time.sleep(30*60)

        bot.infinity_polling()

    except Exception as ex:
        logging.error(ex)
