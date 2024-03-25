import telebot
from telebot import types

bot = telebot.TeleBot('YOUR_TOKEN_HERE')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Создание клавиатуры с выбором языка
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_ru = types.KeyboardButton(text="RU")
    button_uz = types.KeyboardButton(text="UZ")
    keyboard.add(button_ru, button_uz)
    bot.send_message(user_id, "Выберите язык:", reply_markup=keyboard)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if message.text.lower() == 'привет':
        bot.send_message(user_id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {user_id}')

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if call.data == "ru":
        bot.send_message(user_id, "Вы выбрали русский язык.")
    elif call.data == "uz":
        bot.send_message(user_id, "Сиз ўзбек тилини танладингиз.")

# Запуск бота
bot.polling()
