import requests
import bs4
import telebot
import time

def get_announcements():
    with open("bxsessid", 'r') as session_file:
        session = session_file.read()

    response = requests.get("https://portal.petrocollege.ru/department-of-distance-learning/ads/",
                            cookies={"BXSESSID": session})

    if "Карзунов" in response.text:
        print("Logged in")
        with open("text.html", 'w', encoding="utf-8") as file:
            file.write(response.text)
    else:
        print("No login")
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
    print("Program Started")

    with open("telegram_bot_token", 'r') as token_file:
        token = token_file.read()

    # bot = telebot.TeleBot(token = token)

    # @bot.message_handler(commands=['start'])
    # def start_bot(message):
    #     chat_id = message.chat.id
    #     bot.send_message(chat_id, "Бот запущен")
        # while True:
        #     bot.send_message(chat_id, announcements[0].text)
        #     time.sleep(10)

    # bot.infinity_polling()
