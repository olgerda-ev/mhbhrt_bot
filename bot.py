import telebot
import conf
from telebot import types
import time
import markovify
import json
import re
import spacy
import shelve

bot = telebot.TeleBot(conf.TOKEN)

nlp = spacy.load("en_core_web_sm")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


with open('combo_model.json', 'r') as outfile:
    commod = json.load(outfile)

comb_mod = POSifiedText.from_json(commod)

shelve_name = 'shelve.db'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton(text="А 'Махабхарата' - это вообще что?", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Хочу предсказание", callback_data="button2")
    button3 = types.InlineKeyboardButton(text="А расскажи мне о...", callback_data="button3")
    button4 = types.InlineKeyboardButton(text="Мудрость дня", callback_data="button4")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)

    bot.send_message(message.chat.id, "*кажется, оракул лениво пробуждается ото сна*")
    bot.send_message(message.chat.id, "Здравствуйте! Что бы Вы хотели узнать?", reply_markup=keyboard)


@bot.message_handler(commands=['about'])
def tell_about(message):
    bot.send_message(message.chat.id, "Бот создан в рамках итогового проекта по курсу программирования.\n"
                                      "Для успешного взаимодействия с ним достаточно нажимать разные кнопочки и "
                                      "следовать присылаемым рекомендациям.\n"
                                      "Для того, чтобы перезапустить оракула, достаточно ввести /start - "
                                      "это можно сделать в любой момент.\n\n"
                                      "Оракул обучался на английском переводе 'Махабхараты', "
                                      "доступном на gutenberg.org/")


@bot.message_handler(commands=['send_sticker'])
def send_sticker(message):
    user_id = message.chat.id
    key = str(user_id)
    with shelve.open(shelve_name) as storage:
        if key in storage:
            bot.send_sticker(message.chat.id, storage[key])
        else:
            pass


@bot.callback_query_handler(func=lambda call: call.data == 'button1')
def callback_inline(call):
    if call.message and call.data == "button1":
        url = 'https://upload.wikimedia.org/wikipedia/commons/8/81/Kurukshetra.jpg'
        bot.send_photo(chat_id=call.message.chat.id, photo=url)
        bot.send_message(call.message.chat.id, "(на иллюстрации из манускрипта - фрагмент битвы на Курукшетре, "
                                               "одного из основных эпизодов 'Махабхараты')\n\n"
                                               "'Махабхарата' (санскр. महाभारतम्) - памятник древнеиндийского "
                                               "эпоса, состоящий из 18 книг - парв. Авторство оригинального "
                                               "текста приписывается мудрецу по имени Вьяса (~III тыс. до н.э.)."
                                               "\nИзначально произведние повествовало о борьбе за престол между "
                                               "наследниками двух княжеских родов, Каурава и Паурава. "
                                               "Со временем поэма дополнялась текстами разных жанров, "
                                               "связанными с философией, мифологией, историей, правом и другими "
                                               "областями. В настоящий момент 'Махабхарата' - "
                                               "одно из крупнейших произведений мировой литературы, "
                                               "утверждающее, что в нем содержится информация обо всём на свете. "
                                               "В индийской традиции нередко называется 'пятой Ведой'.\n"
                                               "to read more: https://en.wikipedia.org/wiki/Mahabharata")


@bot.callback_query_handler(func=lambda call: call.data == 'button2')
def callback_inline(call):
    if call.message and call.data == "button2":
        bot.send_message(call.message.chat.id, "Чтобы получить предсказание о минувшем или грядущем, "
                                               "Вы можете написать следующее: predict I will / I have / It is / "
                                               "That was. "
                                               "Можно попробовать использовать другие местоимения или другие "
                                               "вспомогательные (!) глаголы. Или просто местоимения. Кроме того, можете"
                                               " попробовать использовать временные наречия вроде Tommorow или Today.\n"
                                               "Пожалуйста, после predict начинайте слова с заглавной буквы.\n"
                                               "Ваше сообщение должно выглядеть примерно так:\n"
                                               "predict I have\n"
                                               "или\n"
                                               "predict That day"
                                               "или\n"
                                               "predict I\n"
                                               "\nОракулу может потребоваться некоторое время на чтение таинственных "
                                               "знаков. Кроме того, успех гадания зависит и от ряда других факторов.\n"
                                               "Если предсказание не удалось получить сразу - не отчаивайтесь! "
                                               "Всегда можно попробовать еще раз ;)")
    markup = types.ForceReply()
    bot.send_message(call.message.chat.id, "Начните высказывание:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'button3')
def callback_inline(call):
    if call.message and call.data == "button3":
        bot.send_message(call.message.chat.id, "А рассказать о чём? Напишите (на английском!) любое слово, которое "
                                               "Вас интересует. Помните, что оракул обучался на довольно древних "
                                               "текстах, поэтому о совсем современных понятиях рассуждать он, скорее "
                                               "всего, откажется ¯\_( ͡° ͜ʖ ͡°)_/¯\n"
                                               "(а ещё можно предложить оракулу имя какого-нибудь героя эпоса - "
                                               "тоже на английском)")


@bot.callback_query_handler(func=lambda call: call.data == 'button4')
def callback_inline(call):
    if call.message and call.data == "button4":
        wisdom = comb_mod.make_short_sentence(284)
        wisdom = re.sub(r'\s([?.,’!;"](?:\s|$))', r'\1', wisdom)
        bot.send_message(call.message.chat.id, "*оракул задумывается на какое-то время, а затем таинственно изрекает*")
        bot.send_message(call.message.chat.id, wisdom)


@bot.message_handler(content_types=['text'])
def mess_for_pred(message):
    s = message.text
    if re.search('[a-zA-Z]+', s):
        if s.startswith('predict '):
            ss = s.split()
            seed = ''
            for i in range(len(ss)):
                if i == 0:
                    continue
                else:
                    seed += ss[i] + ' '

            bot.send_message(message.chat.id, "*оракул задумывается...*")

            timeout = time.time() + 60 * 2 + 5
            for i in range(1):
                while True:
                    if time.time() > timeout:
                        break
                    else:
                        tm = comb_mod.make_short_sentence(200)
                        if tm.startswith(seed):
                            break
            if time.time() <= timeout:
                tm = re.sub(r'\s([?.,’!;"](?:\s|$))', r'\1', tm)
                bot.send_message(message.chat.id, "*наконец, он изрекает*")
                bot.send_message(message.chat.id, tm)
            else:
                bot.send_message(message.chat.id, "Кажется, оракул сегодня не в настроении, поэтому ваши слова "
                                                  "остаются без ответа... А может, звезды так сложились.")
        else:
            mes = s
            mes = mes.lower()
            mes = mes.split()
            m = mes[0]
            bot.send_message(message.chat.id, "*оракул загадочно поскрипывает чешуйками...*")
            timeout = time.time() + 60 * 2 + 5
            for i in range(1):
                while True:
                    if time.time() > timeout:
                        break
                    else:
                        sm = comb_mod.make_short_sentence(200)
                        if m in sm:
                            break
            if time.time() <= timeout:
                sm = re.sub(r'\s([?.,’!;"](?:\s|$))', r'\1', sm)
                bot.send_message(message.chat.id, "*наконец, он изрекает*")
                bot.send_message(message.chat.id, sm)
            else:
                bot.send_message(message.chat.id, "Кажется, оракул сегодня не в настроении, поэтому ваши слова "
                                                  "остаются без ответа... А может, звезды так сложились.")
    else:
        bot.send_message(message.chat.id, "*оракул мирно посапывает во сне...*")


@bot.message_handler(content_types=['sticker'])
def sticker_received(message):
    bot.send_message(message.chat.id, "*кажется, оракул всё ещё спит, но выглядит более довольным...*")
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEUnpiRHF0JEP3YGr55Jm2wuN_ORVATwACfwwAAsYlqUou_E0rSwtKmiME")
    sticker_id = message.sticker.file_id
    user_id = message.chat.id
    with shelve.open(shelve_name) as storage:
        storage[str(user_id)] = sticker_id


if __name__ == '__main__':
    bot.polling(none_stop=True)
