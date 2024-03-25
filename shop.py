import telebot
import buttons as bt
import database as db
from geopy import Nominatim

bot = telebot.TeleBot('7178774476:AAEolIhSWIMLKdJCiZ27KsmQcGC33zmECp0')

geolacator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/121.0.0.0 Safari/537.36')

admin_id=446409144

users={}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check = db.check_user(user_id)
    prods = db.get_pr()
    if check:
        bot.send_message(user_id, 'Добро пожаловать в наш магазин! ', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id,'выберите товар:',reply_markup= bt.main_menu_buttons(prods))
    else:
        bot.send_message(user_id, 'Здраствуйте! Давайте проведем регистрацию!\n Напишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Супер, а теперь отправьте номер!', reply_markup=bt.num_button())

    bot.register_next_step_handler(message, get_number, user_name)


def get_number(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'А теперь локацию!', reply_markup=bt.loc_button())

        bot.register_next_step_handler(message, get_location, user_name, user_number)
    else:
        bot.send_message(user_id, 'отправите номер по кнопке!', reply_markup=bt.num_button())

        bot.register_next_step_handler(message, get_number, user_name)


def get_location(message, user_name, user_number):
    user_id = message.from_user.id
    if message.location:
        user_location = geolacator.reverse(f'{message.location.longitude}, {message.location.latitude}')

        db.register(user_id, user_name, user_number, user_location)
        bot.send_message(user_id, 'Регистрация прошла успешно!')
    else:
        bot.send_message(user_id, 'Отправте локация через кнопку!', reply_markup=bt.num_button())

        bot.register_next_step_handler(message, get_location, user_name, user_number)


@bot.callback_query_handler(lambda call: call.data in ['increase', 'decrement', 'to_cart', 'back'])
def choose_pr_amount(call):
    if call.data == 'increament':
        new_amount = users[chat_id]['pr_count']
        new_amount +=1
        bot.edit_message_reply_markup(chat_id=chat_id,message_id=call.message.message.id,
                                      reply_markup=bt.count_buttons(new_amount, 'increament'))
    elif call.data == 'back':
        prods = db.get_pr()
        bot.delete_message(chat_id=chat_id,message_id=call.message.message.id)
        bot.send_message(chat_id,'возвращаю вас обратно в меню', reply_markup=bt.main_menu_buttons(prods))

    elif call.data == 'go_cart':
        product = db.get_exact_pr(user[chat_id]['pr_name'])
        pr_amount = users[chat_id['pr_count']]
        total = product[3] * pr_amount
        db.add_pr( chat_id, product [0], pr_amount, total)
        bot.delete_message(chat_id=chat_id,message_id=call.message.message.id)
        bot.send_message(chat_id, 'Товар успешно добавлен в корзину,что хотите сделать?',
                         reply_markup=bt.cart_buttons())


@bot.callback_query_handler(lambda call: call.data in ['cart', 'order', 'back', 'clear'])
def cart_handler(call):
    chat_id= call.message.chat.id
    if call.data == 'cart':
        cart = db.show_cart(chat_id)
        text = f'ваша корзина\n\n'\
               f'товар:{cart[1]}\n' \
               f'количество:{cart[2]}\n' \
               f' итого:{cart[3]}'
        bot.delete_message(chat_id=chat_id,message_id=call.message.message.id)
        bot.send_message(chat_id, reply_markup=bt.cart_buttons())
    elif call.data =='clear':
        db.clear_cart(chat_id)
        prods = db.get_pr()
        bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
        bot.send_message(chat_id,'ваша корзина очищена!', reply_markup= bt.main_menu_buttons(prods))
    elif call.data == 'order':
        cart=db.make_order(chat_id)
        text = f'новый заказ!\n\n'
               f'id пользователя:{cart[0],[0]}!\n\n'
               f'товар:{cart[0],[1]}\n' \
               f'общая сумма: ${cart[0],[3]}\n' \
               f'адрес: ${cart[1],[0]}'
        bot.send_message(admin_id, text)
        bot.delete_message(chat_id=chat_id,message_id=call.message.message.id)
        bot.send_message(chat_id, 'заказ оформлен ,вам позвонят', reply_markup= bt.main_menu_buttons(prods))

    elif call.data == 'back':
        prods = db.get_pr()
        bot.delete_message(chat_id=chat_id,message_id=call.message.message.id)
        bot.send_message(chat_id,'возвращаю вас обратно в меню', reply_markup=bt.main_menu_buttons(prods))
               @bot.callback_query_handler(lambda call: int(call.data) in db.get_pr())

def get_product(call):
    chat_id = call.message.chat.id
    exat_product= db.get_exact_pr(int(call.data))
    users[chat_id]={'pr_name': call.data,'pr_count': 1}
    bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
    bot.send_photo(chat_id, photo=exat_product[4],
                   caption= f'название товара: {exat_product[0]},\n\n'
                            f'описание товара:{exat_product[1]}'
                            f'количество товара:{exat_product[2]}'
                            f'Цена товара:{exat_product[3]}',
                   reply_markup=bt.cout_button())



@bot.message_handler(commands=['admins'])
def admin(message):
    if message.from_user.id == admin_id:
        bot.send_message(admin_id,' добро пожаловать в админ панель', reply_markup=bt.admin_buttons())
        bot.register_next_step_handler(message, admin_choise)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!\n Нажмите /start')


def admin_choise(message):
    if message.text == 'добавить продукт':
        bot.send_message(admin_id, 'Введите название товара', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message,get_pr_name)
    elif message.text == 'удалить продукт':
        pr_check = db.check_pr()
        if pr_check:
            bot.send_message(admin_id, 'введите id товара')
            bot.register_next_step_handler(message, get_pr_to_del)
        else:
            bot.send_message(admin_id, 'этого продукта нет на складе')
            bot.register_next_step_handler(message, admin_choise)

    elif message.text == 'изменить количество продукта':
        pr_check: db.check_pr()
        if pr_check:
            bot.send_message(admin_id, 'введите айди товара')
            bot.register_next_step_handler(message, get_pr_to_edit)
        else:
            bot.send_message(admin_id, 'этого продукта нет на складе')
            bot.register_next_step_handler(message, admin_choise)


def get_pr_name(message):
    pr_name = message.text
    bot.send_message(admin_id, 'придумайте описание')
    bot.register_next_step_handler(get_pr_des, pr_name)


def get_pr_des(message, pr_name):
    pr_des = message.text
    bot.send_message(admin_id, 'количество товара?')
    bot.register_next_step_handler(message, get_pr_count, pr_name, pr_des)


def get_pr_count(message, pr_name, pr_des):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Пишите только целые числа')
        bot.register_next_step_handler(message, get_pr_count, pr_name, pr_des)
    else:
        pr_count = int(message.text)
        bot.send_message(admin_id,'Какая цена у продукта')
        bot.register_next_step_handler(message, get_pr_price, pr_name, pr_des, pr_count)


def get_pr_price(message, pr_name, pr_des, pr_count):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Пишите только дробные числа')
        bot.register_next_step_handler(message, get_pr_price, pr_name, pr_des,pr_count)
    else:
        pr_price = float(message.text)
        bot.send_message(admin_id, 'последний этап, зайдите на сайт https://postimages.org/ и загрузите фото\n'
                                   'затем отправьте прямую ссылку на фото')
        bot.register_next_step_handler(message, get_pr_photo, pr_name, pr_des, pr_count, pr_price)


def get_pr_photo(message, pr_name,pr_des, pr_count, pr_price):
    pr_photo = message.text
    db.add_pr(pr_name, pr_des, pr_count, pr_price, pr_photo)
    bot.send_message(admin_id, 'Готово, что то еще?', reply_markup=bt.admin_buttons())
    bot.register_next_step_handler(message, admin_choise)


def get_pr_to_edit(message):
    if message != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа')
        bot.register_next_step_handler(message,get_pr_to_edit)
    else:
        pr_id = int(message.text)
        bot.send_message(admin_id,'сколько товара прибыло')
        bot.register_next_step_handler(message, get_pr_stock,pr_id)


def get_pr_stock(message,pr_id):
    if message != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа')
        bot.register_next_step_handler(message,get_pr_stock,pr_id)
    else:
        pr_stock = int(message.text)
        db.change_pr_count(pr_id,pr_stock)
        bot.send_message(admin_id,'Количество товара изменино', reply_markup= bt.admin_buttons())
        bot.register_next_step_handler(message, admin_choise,)


def get_pr_to_del(message):
    if message != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа')
        bot.register_next_step_handler(message, get_pr_to_del)
    else:
        pr_id = int(message.text)
        db.del_pr(pr_id)
        bot.send_message(admin_id, 'товар успешно измене', reply_markup=bt.admin_buttons())
        bot.register_next_step_handler(message, admin_choise)


bot.polling()
