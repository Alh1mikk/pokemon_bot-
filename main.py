import telebot 
from telebot import types
from config import token

from logic import Pokemon

bot = telebot.TeleBot(token) 
battle_requests = {}  # Словарь для хранения запросов на бой: {opponent_username: challenger_username}

user_chat_ids = {}    # Словарь для хранения соответствия username и chat_id

@bot.message_handler(func=lambda message: True)
def update_user_chat_id(message):
    if message.from_user.username:  # Проверяем, есть ли username у пользователя
        user_chat_ids[message.from_user.username] = message.chat.id

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)   
    btn = types.KeyboardButton("создать покемона")
    btn1 = types.KeyboardButton("мой покемон")
    btn2 = types.KeyboardButton("битва")
    btn3 = types.KeyboardButton("картинка покемона")
    markup.add(btn, btn1, btn2, btn3)
    
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, 
                        text="Приветствую тебя {0.first_name}, я твой бот по покемонам. Твой покемон: {1}".format(
                            message.from_user, pokemon.name), 
                        reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 
                        text="Приветствую тебя {0.first_name}, я твой бот по покемонам. У тебя пока нет покемона, создай его!".format(
                            message.from_user), 
                        reply_markup=markup)

@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        
        # Проверяем и применяем восстановление HP перед кормлением
        pokemon.check_hp_recovery()
        
        # Проверяем не закончились ли баффы
        buff_message = pokemon.check_buffs()
        if buff_message:
            bot.send_message(message.chat.id, buff_message)
        
        # Кормим покемона
        result = pokemon.feed()
        bot.send_message(message.chat.id, result)
        bot.send_message(message.chat.id, f"Твой покемон теперь:\n{pokemon.info()}")
    else:
        bot.send_message(message.chat.id, "У вас нет покемона для кормления. Создайте его сначала!")

# Добавим проверку восстановления HP и баффов в другие обработчики
def check_pokemon_status(pokemon):
    messages = []
    if pokemon.check_hp_recovery():
        messages.append("Покемон восстановил 10 HP (автоматическое восстановление каждые 10 минут).")
    
    buff_message = pokemon.check_buffs()
    if buff_message:
        messages.append(buff_message)
    
    return messages

# Модифицируем существующие обработчики для проверки статуса
@bot.message_handler(func=lambda message: message.text == "мой покемон")
def my_pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        
        # Проверяем статус перед показом информации
        status_messages = check_pokemon_status(pokemon)
        for msg in status_messages:
            bot.send_message(message.chat.id, msg)
        
        bot.send_message(message.chat.id, text=f"покемон {message.from_user.first_name}, характеристики: {pokemon.info()}")
    else:
        bot.send_message(message.chat.id, text=f"у {message.from_user.first_name} нет покемона, создай его через команду /pkmn")

@bot.message_handler(commands=['pkmn'])
def pkmn(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_photo(message.chat.id, pokemon.show_img(), caption=pokemon.get_name())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['btn'])
def btn(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("создать покемона")
    btn1 = types.KeyboardButton("мой покемон")
    btn2 = types.KeyboardButton("битва")
    btn3 = types.KeyboardButton("картинка покемона")
    markup.add(btn, btn1, btn2, btn3)
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, text="покемон {0.first_name}, имя: {1}".format(message.from_user, pokemon.name), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="у {0.first_name} нет покемона, создай его через команду /pkmn".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("создать покемона")
    btn1 = types.KeyboardButton("мой покемон")
    btn2 = types.KeyboardButton("битва")
    btn3 = types.KeyboardButton("картинка покемона")
    markup.add(btn, btn1, btn2, btn3)
    
    if message.text == "картинка покемона":
        if message.from_user.username in Pokemon.pokemons.keys():
            pokemon = Pokemon.pokemons[message.from_user.username]
            bot.send_photo(message.chat.id, pokemon.show_img())
        else:
            bot.send_message(message.chat.id, text="у {0.first_name} нет покемона, создай его через команду /pkmn".format(message.from_user), reply_markup=markup)
    
    elif message.text == "мой покемон":
        if message.from_user.username in Pokemon.pokemons.keys():
            pokemon = Pokemon.pokemons[message.from_user.username]
            bot.send_message(message.chat.id, text="покемон {0.first_name}, характеристики: {1}".format(message.from_user, pokemon.info()), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="у {0.first_name} нет покемона, создай его через команду /pkmn".format(message.from_user), reply_markup=markup)
    
    elif message.text == "создать покемона":
        if message.from_user.username not in Pokemon.pokemons.keys():
            pokemon = Pokemon(message.from_user.username)
            bot.send_photo(message.chat.id, pokemon.show_img(), caption=pokemon.get_name())
        else:
            bot.reply_to(message, "Ты уже создал себе покемона")
    
    elif message.text == "битва":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("вызвать соперника")
        back = types.KeyboardButton("отмена")
        markup.add(btn1, back)
        bot.send_message(message.chat.id, text="Выберите действие:", reply_markup=markup)
    
    elif message.text == "вызвать соперника":
        msg = bot.send_message(message.chat.id, "Введите username соперника (без @):")
        bot.register_next_step_handler(msg, process_opponent_step)
    
    elif message.text == "отмена":
        bot.send_message(message.chat.id, text="Действие отменено", reply_markup=markup)

def process_opponent_step(message):
    opponent_username = message.text.strip()
    challenger_username = message.from_user.username
    
    if opponent_username not in Pokemon.pokemons.keys():
        bot.send_message(message.chat.id, f"Пользователь @{opponent_username} не имеет покемона или не существует.")
        return
    
    if opponent_username == challenger_username:
        bot.send_message(message.chat.id, "Нельзя вызвать на бой самого себя!")
        return
    
    # Сохраняем запрос на бой
    battle_requests[opponent_username] = challenger_username
    
    # Отправляем запрос на бой сопернику
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_accept = types.KeyboardButton("принять бой")
    btn_decline = types.KeyboardButton("отказаться")
    markup.add(btn_accept, btn_decline)
    
    bot.send_message(message.chat.id, f"Запрос на бой отправлен @{opponent_username}!")
    bot.send_message(chat_id=get_user_chat_id(opponent_username), 
                    text=f"@{challenger_username} вызывает вас на бой!",
                    reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["принять бой", "отказаться"])
def handle_battle_response(message):
    opponent_username = message.from_user.username
    
    if opponent_username not in battle_requests:
        bot.send_message(message.chat.id, "Нет активных запросов на бой.")
        return
    
    challenger_username = battle_requests[opponent_username]
    
    if message.text == "принять бой":
        # Проводим бой
        challenger_pokemon = Pokemon.pokemons[challenger_username]
        opponent_pokemon = Pokemon.pokemons[opponent_username]
        
        # Первый удар наносит вызывающий
        result1 = opponent_pokemon.fight(challenger_pokemon)
        # Второй удар наносит противник, если первый не убил
        if opponent_pokemon.pokemon_stats['hp'] > 0:
            result2 = challenger_pokemon.fight(opponent_pokemon)
        
        # Отправляем результаты боя обоим участникам
        bot.send_message(chat_id=get_user_chat_id(challenger_username), 
                       text=f"Результат боя:\n{result1}\n{result2 if 'result2' in locals() else ''}")
        bot.send_message(chat_id=get_user_chat_id(opponent_username), 
                       text=f"Результат боя:\n{result1}\n{result2 if 'result2' in locals() else ''}")
        
        # Обновляем статистику покемонов
        bot.send_message(chat_id=get_user_chat_id(challenger_username), 
                       text=f"Твой покемон теперь:\n{challenger_pokemon.info()}")
        bot.send_message(chat_id=get_user_chat_id(opponent_username), 
                       text=f"Твой покемон теперь:\n{opponent_pokemon.info()}")
    else:
        bot.send_message(chat_id=get_user_chat_id(challenger_username), 
                       text=f"@{opponent_username} отказался от боя.")
        bot.send_message(message.chat.id, "Вы отказались от боя.")
    
    # Удаляем запрос на бой
    if opponent_username in battle_requests:
        del battle_requests[opponent_username]

def get_user_chat_id(username):
    return user_chat_ids.get(username)

bot.infinity_polling(none_stop=True)

