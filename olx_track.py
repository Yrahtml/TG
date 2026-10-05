
import requests
import telebot 
import sqlite3
KEY = '170EF6AAE10E580B091B704964FB7367'
bot = telebot.TeleBot('8591317996:AAEDVJfwc3SB9yVu50bFoqaMWJxtiLCliTY')
def get_player_info(steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={KEY}&steamids={steam_id}"
    response = requests.get(url)

    data = response.json()
    
    player = data['response']['players'][0]
    status = 'Online' if player['personastate'] == 1 else 'offline'

    feedback=(f'Юзерка: {player['personaname']}\n Статус: {status}\n Країна: {player.get('loccountrycode', 'Unknown')}\n Аватар: {player['avatarfull']}\n https://steamcommunity.com/profiles/{steam_id}/')
    
    return feedback
def get_player_friends(steam_id):    
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={KEY}&steamid={steam_id}&relationship=friend"
    response = requests.get(url)
    
    data = response.json()
    
    friends = data['friendslist']['friends']
    
    feedback = ''
    for friend in friends:
        feedback = (f"Steam ID: {friend['steamid']}")   
        return feedback   
#     image_data = requests.get(player['avatarfull']).content
#     with open('img.png', 'wb') as file:
#         file.write(image_data)
#     with open('player_card.txt', 'w') as file:
#          file.write(f'Юзерка: {player['personaname']}\n Статус: {status}\n Країна: {player.get('loccountrycode', 'Unknown')}\n Аватар: {player['avatarfull']}')

@bot.message_handler(commands=["start"])
def answear(message):
    conn = sqlite3.connect("Steam_IDS.sql")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT , steam_id TEXT UNIQUE)")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id,'Введи свій Steam Id')
    bot.register_next_step_handler(message, steam_id)

def steam_id(message):
    steam_id = message.text.strip()
    conn = sqlite3.connect("Steam_IDS.sql")
    cur = conn.cursor()
    
    cur.execute("INSERT OR IGNORE INTO users (steam_id) VALUES (?)", (steam_id,))
    conn.commit()
    cur.close()
    conn.close()


    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Список", callback_data='list'))
    bot.send_message(message.chat.id, "Зареєестровано", reply_markup=markup)

@bot.callback_query_handler(func =lambda callback:True)
def call_back(callback):
    if callback.data == 'list':
        conn = sqlite3.connect("Steam_IDS.sql")
        cur = conn.cursor()
        cur.execute("SELECT steam_id FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()

        if not users:
            bot.send_message(callback.message.chat.id, "База даних порожня.")
            return

        markup = telebot.types.InlineKeyboardMarkup()
        for us in users:
            st_id = us[0]
            markup.add(telebot.types.InlineKeyboardButton(f"Переглянути {st_id}", callback_data=f"view_{st_id}"))

        bot.send_message(callback.message.chat.id, "Оберіть Steam ID для перегляду:", reply_markup=markup)
    elif callback.data.startswith('view_'):
        
        selected_steam_id = callback.data.split('view_')[1]

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(f"Видалити {selected_steam_id}", callback_data=f"delete_{selected_steam_id}"))
        markup.add(telebot.types.InlineKeyboardButton(f"Список друзів {selected_steam_id}", callback_data=f"friends_{selected_steam_id}"))
        info = get_player_info(selected_steam_id)
        bot.send_message(callback.message.chat.id, info , reply_markup= markup)
    elif callback.data.startswith('delete_'):
        selected_steam_id = callback.data.split('delete_')[1]

        conn = sqlite3.connect('Steam_IDS.sql')
        cur = conn.cursor()

        cur.execute("DELETE FROM users WHERE steam_id = ?", (selected_steam_id,))
        conn.commit()

        cur.close()
        conn.close()

        bot.delete_message(callback.message.chat.id , callback.message.id)
        bot.send_message(callback.message.chat.id , "Напишіть /start для заповнення данних")
# def start_work():
#     menu =input("enter + to start and - to exit\n")
#     run = True if menu == '+' else False
#     return run



  



# def get_player_games(steam_id):
#     url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={KEY}&steamid={steam_id}&include_appinfo=1&format=json"
#     response = requests.get(url)

#     data = response.json()

#     games = data.get('response', {}).get('games', [])

#     print("Список ігор:")
#     for game in games:
#         hours = round(game['playtime_forever'] / 60, 1)
#         print(f"{game['name']} — {hours} год.")


# run = start_work()

# while run:
#     choice = int(input("Оберіть, що ви хочете зробити: 1 - Отримати інформацію про гравця, 2 - Отримати список друзів, 3 - отримати всі ігри гравця \n"))
#     steam_id = int(input("Введіть ваш Steam ID: "))
    
#     if choice != 1 and choice != 2 and choice != 3 and choice != 0:
#             print("Введіть правильний номер (1, 2, 3 або 0)")
#     if choice==0:
#         run = False
#         start_work()
#     if choice == 1:
#         get_player_info(steam_id)
#     elif choice == 2:
#        get_player_friends(steam_id)  
#     elif choice == 3:
#         get_player_games(steam_id)

bot.polling(none_stop=True)