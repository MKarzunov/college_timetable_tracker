import requests
import bs4

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

soup = bs4.BeautifulSoup(response.text, 'html.parser')
announcements = soup.find_all(class_="announcements__element news__col")
last_announcement = announcements[0]
print(last_announcement)