# 1) add_user(str user_id, list books ): принимает на вход значения user_id и список книг, в котором лежат book_id.
# Добавляет для пользователя книги, которые ему понравились 2) get_user_info(): по user Id возвращает список книг


import sqlite3


def return_books_of_user(id):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()

        sql_ = """SELECT * FROM users WHERE user_id = ?"""
        cursor.execute(sql_, (id,))
        a = cursor.fetchone()
        b = list(map(str, a[1].split()))
        return (b[::2])
        sqlite_connection.commit()

        cursor.close()
        return (b[::2])
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def return_books_of_user_with_ratings(id):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()

        sql_ = """SELECT * FROM users WHERE user_id = ?"""
        cursor.execute(sql_, (id,))
        a = cursor.fetchone()
        # b = list(map(str, a[1].split()))
        return list(a)
        sqlite_connection.commit()

        cursor.close()
        return (b[::2])
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def check_user(id):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()

        sql_ = """SELECT * FROM users WHERE user_id = ?"""
        cursor.execute(sql_, (id,))
        a = cursor.fetchone()

        sqlite_connection.commit()

        cursor.close()
        if a is None:
            return 0
        else:
            return 1
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_user(id):
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()

        sql_delete_same_id = """delete from users where user_id = ?"""
        cursor.execute(sql_delete_same_id, (id,))

        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_user(user_id, books):
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        delete_user(user_id)
        sqlite_add_user = """INSERT INTO users VALUES (?, ?);"""

        data_tuple = (user_id, str(''.join(books)))

        cur.execute(sqlite_add_user, data_tuple)

        con.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if con:
            con.close()


def user_ratings(us_id, books_ids):
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        sql_select_user = """select * from users where user_id = ?"""

        cur.execute(sql_select_user, (us_id,))
        user_vector = cur.fetchall()
        user_vec = list(map(str, user_vector[0][1].split()))
        user_books = dict()
        for i in range(0, len(user_vec), 2):
            user_books[user_vec[i]] = user_vec[i + 1]
        result_vector = [0] * len(books_ids)
        for i in range(len(books_ids)):
            if books_ids[i] in user_books:
                result_vector[i] = user_books[books_ids[i]]
        return result_vector
        con.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if con:
            con.close()

# a = ['3', '1', '4', '3', '45', '5']
# add_user(1, a)
# add_user(2, a)
# user_ratings('1', ['2', '4', '45'])
