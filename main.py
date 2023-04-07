# Imports
import telebot
from telebot import types
import numpy as np
import pandas
import httplib2

# from functions_for_books import *
import model
from functions_for_users import *
from model import *
from pretty import *

''' Loading main components '''
sqlite_connection = sqlite3.connect('books.db', check_same_thread=False)
cursor_book = sqlite_connection.cursor()
print("[DB was connected]")

f = open("collumns.txt", "r")
for line in f:
    book_pattern = line.split()
f.close()
print("[Columns are loaded]")

user_matrix = np.loadtxt("user_matrix.txt", delimiter=" ")
print("[User matrix was loaded]")

df_recommendation = pd.read_csv(r"C:\Users\Pavel\Desktop\Book_Recomendation_System\models\svd_recomendation.csv.gz",
                                sep=',')
print("[Recommendation was loaded]")
''' Loading main components '''


def get_book_info(id: object) -> object:
    '''Вывод данных в формате list по id книги'''
    global sqlite_connection
    global cursor_book
    try:
        sql_select_query = """select * from books where book_id = ?"""
        cursor_book.execute(sql_select_query, (id,))
        records = cursor_book.fetchall()
        return list(records)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


''' BOT CONFIG '''

token = ""
bot = telebot.TeleBot(token)

''' BOT CONFIG '''

''' GLOBAL VARIABLES '''
users_adding_books = {}
book_action = [
    "📚 Получить детальную информацию о книге",
    "🔎 Найти похожие книги по описанию"
]
books_recommended = {}
''' GLOBAL VARIABLES '''


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()

    button_get_book = types.KeyboardButton('🆕 Рекомендуемое')
    button_my_books = types.KeyboardButton('❤️ Мои книги')
    button_get_friend = types.KeyboardButton('📚 Добавить книгу')

    markup.row(button_get_book)
    markup.row(button_my_books)
    markup.row(button_get_friend)

    bot.send_message(message.chat.id, 'Нажми на кнопку!', reply_markup=markup)


@bot.message_handler(content_types=['text', 'photo'])
def text_handler(message):
    global book_pattern
    global df_recommendation
    global books_recommended
    if message.text == '❤️ Мои книги':

        if check_user(str(message.chat.id)):
            user_liked_books = return_books_of_user(str(message.chat.id))
            print(user_liked_books)
            i = 0
            for el in user_liked_books:
                book_info = get_book_info(el)
                print(book_info)
                if len(book_info) != 0:
                    markup_my_books = types.InlineKeyboardMarkup(row_width=1)
                    item = types.InlineKeyboardButton('Описание книги',
                                                      callback_data=('book_info' + str(book_info[0][0])))
                    markup_my_books.add(item)
                    text_to_user = "Название: " + str(book_info[0][3]) + "\n"
                    text_to_user += "Жанр: " + str(book_info[0][2]) + "\n"
                    if cover_check(book_info[0][8]) == 1:
                        i = i + 1
                        h = httplib2.Http('.cache')
                        response, content = h.request(book_info[0][8])
                        bot.send_photo(message.chat.id, content, caption=text_to_user, reply_markup=markup_my_books)
                    else:
                        bot.send_message(message.chat.id, text_to_user, reply_markup=markup_my_books)

        else:
            bot.send_message(message.chat.id,
                             "Похоже, что Вы еще не добавили ни одной книги. \nСделайте это прямо сейчас: /add_new_book")

    elif message.text == '🆕 Рекомендуемое':
        # finding sim user
        user_books_vector = np.array(user_ratings(str(message.chat.id), book_pattern), dtype=float)
        mx = -2
        user_index = -1
        i = 0
        for el in user_matrix:
            temp = model.cosine_similarity(user_books_vector, el)
            if temp > mx:
                mx = temp
                user_index = i
            i += 1

        book_for_user = model.get_recommendation(user_index, df_recommendation,
                                                 return_books_of_user(str(message.chat.id)))

        books_recommended[message.chat.id] = [get_book_info(el) for el in book_for_user]

        book_info = books_recommended[message.chat.id][0]

        markup_rec = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton('•1',
                                           callback_data=('rec:' + '0'))
        item2 = types.InlineKeyboardButton('2',
                                           callback_data=('rec:' + '1'))
        item3 = types.InlineKeyboardButton('•3•',
                                           callback_data=('rec:' + '2'))
        item4 = types.InlineKeyboardButton('4',
                                           callback_data=('rec:' + '3'))
        item5 = types.InlineKeyboardButton('5•',
                                           callback_data=('rec:' + '4'))
        markup_rec.row(item1, item2, item3, item4, item5)

        text_to_user = "Название: " + str(book_info[0][3]) + "\n"
        text_to_user += "Жанр: " + str(book_info[0][2]) + "\n"
        text_to_user += "Описание: " + str(book_info[0][12]) + "\n"
        if cover_check(book_info[0][8]) == 1:
            i = i + 1
            h = httplib2.Http('.cache')
            response, content = h.request(book_info[0][8])
            bot.send_photo(message.chat.id, content, caption=text_to_user, reply_markup=markup_rec)
        else:
            bot.send_photo(message.chat.id, None, caption=text_to_user, reply_markup=markup_rec)

    elif message.text == '📚 Добавить книгу' or message.text == '/add_new_book':
        msg = bot.send_message(message.chat.id, "Введите название(временно book_id) книги, которая вам понравилась: ")
        bot.register_next_step_handler(msg, get_title)
    else:
        bot.send_message(message.chat.id, 'Простите, я Вас не понял :(')


def get_title(message):
    global users_adding_books
    if message.text.isdigit():
        users_adding_books[message.chat.id] = message.text
        print(message.text)
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton('⭐', callback_data='star:1')
        item2 = types.InlineKeyboardButton('⭐⭐', callback_data='star:2')
        item3 = types.InlineKeyboardButton('⭐⭐⭐', callback_data='star:3')
        item4 = types.InlineKeyboardButton('⭐⭐⭐⭐', callback_data='star:4')
        item5 = types.InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data='star:5')
        markup.add(item5)
        markup.add(item4)
        markup.add(item3)
        markup.add(item2)
        markup.add(item1)
        msg = bot.send_message(message.chat.id, "Хорошо! Теперь оцените книгу.", reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, "book_id целое число: ")
        bot.register_next_step_handler(msg, get_title)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global users_adding_books
    if 'book_info' in call.data:
        book_info = get_book_info((call.data.replace('book_info', '')))
        new_text = str(call.message.text) + "\n\nОписание: " + str(book_info[0][12])
        print(new_text)
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=new_text)
        except Exception:
            pass
        try:
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=new_text)
        except Exception:
            pass
    if 'star' in call.data:
        try:
            user_rating = call.data.split(":")[1]

            users_adding_books[call.message.chat.id] += " " + user_rating + " "
            user_ratings = []
            if check_user(int(call.message.chat.id)):
                user_ratings = return_books_of_user_with_ratings(int(call.message.chat.id))[1]

            user_ratings += (users_adding_books[call.message.chat.id])
            add_user(call.message.chat.id, user_ratings)
            bot.answer_callback_query(call.id, text="Книга добавлена")
            print("[debug]: In Callback", user_ratings)
        except Exception:
            bot.send_message(call.message.chat.id, "Что-то пошло не так, попробуйте снова! ")
    if 'rec' in call.data:
        try:
            book_id = call.data.split(":")[1]
            book_info = books_recommended[call.message.chat.id][int(book_id)]
            print(book_info)
            text_to_user = "Название: " + str(book_info[0][3]) + "\n"
            text_to_user += "Жанр: " + str(book_info[0][2]) + "\n"
            text_to_user += "Описание: " + str(book_info[0][12]) + "\n"

            markup_rec = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('•1',
                                               callback_data=('rec:' + '0'))
            item2 = types.InlineKeyboardButton('2',
                                               callback_data=('rec:' + '1'))
            item3 = types.InlineKeyboardButton('•3•',
                                               callback_data=('rec:' + '2'))
            item4 = types.InlineKeyboardButton('4',
                                               callback_data=('rec:' + '3'))
            item5 = types.InlineKeyboardButton('5•',
                                               callback_data=('rec:' + '4'))
            markup_rec.row(item1, item2, item3, item4, item5)

            if cover_check(book_info[0][8]) == 1:
                h = httplib2.Http('.cache')
                response, content = h.request(book_info[0][8])
                bot.edit_message_media(chat_id=call.message.chat.id,
                                       media=telebot.types.InputMedia(type='photo', media=content, caption=text_to_user),
                                       message_id=call.message.id, reply_markup=markup_rec)
            else:
                bot.edit_message_media(chat_id=call.message.chat.id,
                                       media=telebot.types.InputMedia(type='photo', media=None, caption=text_to_user),
                                       message_id=call.message.id, reply_markup=markup_rec)
        except Exception:
            bot.send_message(call.message.chat.id, "Что-то пошло не так =(")


bot.polling()
