import os #Чтобы скрыть номер токена
from json import JSONDecodeError
import telebot
from telebot import types
import change_data_for_bot_udar as ch_d
import scores_for_bot_udar as sc_user
import get_word_api as g_word

os.environ['TELEGRAM_TOKEN']

token = os.environ['TELEGRAM_TOKEN']


bot = telebot.TeleBot(token)


MAIN_STATE = 'main'
ASK_STATE = 'ask_state'
WORD_STATE = 'word_state'

show_score = ['покажи счет', 'покажи счёт']
ask_option = ['спроси меня слово',
              'спроси меня',
              'спроси у меня',
              'спроси у меня слово'
              ]

data = ch_d.data

markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb1 = types.KeyboardButton('Покажи счёт')
kb2 = types.KeyboardButton('Спроси меня')
markup.add(kb1, kb2)


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    user_id = str(message.from_user.id)
    state = data['states'].get(user_id, MAIN_STATE)

    if state == MAIN_STATE:
        main_handler(message)
    elif state == ASK_STATE:
        ask_state(message)
    elif state == WORD_STATE:
        word_state(message)


def main_handler(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    ch_d.change_data('users', user_id, user_name)

    if 'привет' in message.text.lower():
        bot.send_message(user_id, 'Здравствуй, ' + user_name + '!',
                         reply_markup=markup
                         )

    elif message.text.lower() in ask_option:
        ch_d.change_data('states', user_id, ASK_STATE)
        reset_markup = types.ReplyKeyboardRemove()
        bot.send_message(user_id,
                         'Напиши, на какую букву начинается слово, или укажи "любая"',
                         reply_markup=reset_markup
                         )

    elif message.text.lower() in show_score:
        try:
            user_vict = str(data['score'][user_id]['victories'])
            user_def = str(data['score'][user_id]['defeats'])
            ans = user_vict + ':' + user_def
            bot.send_message(user_id, ans)

        except KeyError:
            ch_d.change_data('score', user_id, {'victories': 0, 'defeats': 0})
            user_vict = str(data['score'][user_id]['victories'])
            user_def = str(data['score'][user_id]['defeats'])
            ans = user_vict + ':' + user_def
            bot.send_message(user_id, ans)

    else:
        bot.send_message(user_id,
                         'Это бот-тренажер ударений: он поможет научиться '
                         'правильной постановке ударений в сложных словах',
                         reply_markup=markup
                         )


def ask_state(message):
    user_id = str(message.from_user.id)
    ch_d.change_data('user_let', user_id, message.text.lower())
    letter = data['user_let'][user_id]

    try:
        response = g_word.get_response(letter)

        ch_d.change_data('states', user_id, WORD_STATE)
        ch_d.change_data('user_word', user_id, response['word'])
        word = data['user_word'][user_id].lower()
        bot.send_message(user_id,
                         'Поставь ударение в слове - {}. '
                         'Напиши все буквы в нижнем регистре, а букву с ударением '
                         'поставь в верхнем. Например, искрА. '
                         .format(word)
                         )

    except JSONDecodeError:
        ch_d.change_data('states', user_id, ASK_STATE)
        bot.send_message(user_id, 'Попробуй еще раз')


def word_state(message):
    user_id = str(message.from_user.id)
    ch_d.change_data('states', user_id, MAIN_STATE)

    if message.text == data['user_word'][user_id]:
        bot.send_message(user_id, 'Правильно!', reply_markup=markup)
        sc_user.add_victories(user_id, 1)
    else:
        bot.send_message(user_id, 'Неправильно :(', reply_markup=markup)
        sc_user.add_defeats(user_id, 1)


bot.polling()


