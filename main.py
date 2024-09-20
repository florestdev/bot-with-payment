import os

try:
    import telebot # pip install pyTelegramBotAPI
    from telebot import types, TeleBot
except ImportError:
    input(f'Нажмите Enter для установки библиотеки...')
    os.system('pip install pyTelegramBotAPI')

token = 'your token.'
id_of_channel = 'ID of your Telegram channel.'
price = 100

bot = TeleBot(token, protect_content=True)

@bot.message_handler(commands=['start', 'help', 'buy'])
def start(message: types.Message) -> None:
    bot.reply_to(message, f'Привет! С помощью кнопки ниже, Вы можете купить вход в наш приватный Telegram канал!', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Купить вход', callback_data='join-channel-telegram')))

@bot.callback_query_handler(lambda query: True)
def query_obrab(query: types.CallbackQuery) -> None:
    if query.data == 'join-channel-telegram':
        bot.delete_message(query.message.chat.id, query.message.id)
        bot.send_invoice(query.message.chat.id, 'Подписка на приватный канал', 'Подписка на мой личный приватный Telegram канал, где Вы узнаете много обо мне!', 'bought-prohodka', '', 'XTR', [types.LabeledPrice('Подписка на приватный канал', price)])

@bot.pre_checkout_query_handler(lambda query: True)
def obrab_plat(pre_chekout: types.PreCheckoutQuery) -> None:
    bot.answer_pre_checkout_query(pre_chekout.id, True)

@bot.message_handler(content_types=['succesful_payment'])
def success(message: types.Message) -> None:
    if message.successful_payment.invoice_payload == 'bought-prohodka':
        create_link = bot.create_chat_invite_link(id_of_channel, member_limit=1).invite_link
        bot.reply_to(message, create_link)
        
bot.infinity_polling()
