import telebot
import config
import requests

bot = telebot.TeleBot("ваш_токен")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Введите сумму для конвертации и валюту в формате "сумма валюта" (например, "100 USD"):')


@bot.message_handler(func=lambda message: True)
def convert(message):
    try:
        amount, currency = message.text.split()
        amount = float(amount)


        rate = get_exchange_rate(currency.upper())


        converted_amount = amount * rate

        bot.send_message(message.chat.id, f"{amount} {currency.upper()} = {converted_amount:.2f} EUR")
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка. Проверьте правильность ввода и попробуйте еще раз.')



def get_exchange_rate(currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates']['EUR']


bot.polling()