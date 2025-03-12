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
    # last_announcement = announcements[0]
    return announcements

with open("telegram_bot_token", 'r') as token_file:
    token = token_file.read()

bot = telebot.TeleBot(token = token)

# chat_id = None

@bot.message_handler(commands=['start'])
def start_bot(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Бот запущен")
    announcements = get_announcements()
    while True:
        bot.send_message(chat_id, announcements[0].text)
        time.sleep(10)

bot.infinity_polling()
