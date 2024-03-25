from telebot import types

def num_button():

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number= types.KeyboardButton ('Отправить номер', request_contact=True)
    kb.add(number)
    return kb


def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(location)
    return kb


def admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_pr = types.KeyboardButton('Добавить продукт')
    dell_pr = types.KeyboardButton('Удалить продукт')
    edit_pr = types.KeyboardButton('Изменить количество продукта')
    to_menue = types.KeyboardButton('на главную')


    kb.add(add_pr, edit_pr, dell_pr)
    kb.row(to_menue)
    return kb


def main_menu_buttons(all_products):
    kb = types.InlineKeyboardButton(row_width=2)
    prod_buttons=[types.InlineKeyboardButton(text=f'{i[1]}', callback_data= f'{i[0]}', callback_data=f'{i{0}}')
                  for i in all_products if i [2]>0
#  возьми все товары из database но проверяй естди товар больше 0 создавай кнопку , если нет не создавай
cart = types.InlineKeyboardMarkup(text = 'корзина ', callback_data ='cart')
    kb.add(*prod_buttons)
    kb.row(cart)
    return kb

def cout_button(amount=1, plus_or_minus=''):
    kb = types.InlineKeyboardMarkup(row_width=3)
    minus= types.InlineKeyboardButton( text ='-', callback='decriment')
    current_amount = types.InlineKeyboardButton (text= str(amount), callback_data=amount)
    plus= types.InlineKeyboardButton( text='+', callback='incriment' )
    back= types.InlineKeyboardButton( text= 'назад', callback='incriment' )
    if plus_or_minus =='increment':
        amount += 1
        current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    elif plus_or_minus =='descriment':
        if amount > 1:
            amount -= 1
            current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    kb.add(minus,current_amount,plus)
    kb.row(to_cart)
    kb.row(back)
    return kb


def cart_buttons():
    kb = types.InlineKeyboardButton (row_within =2)
    order = types.InlineKeyboardButton( text ='оформить заказэ', callback_data='order')
    back = types.InlineKeyboardButton(text='назад', callback_data='back')
    clear = types.InlineKeyboardButton(text='очистить', callback_data='clear')


    kb.add(clear, back)
    kb.row(order)
    return  kb