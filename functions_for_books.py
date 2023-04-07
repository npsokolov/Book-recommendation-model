import sqlite3

sqlite_connection = sqlite3.connect('books.db')
cursor_book = sqlite_connection.cursor()

# вывод данных в формате list по id книги
def get_book_info(id):
    try:
        sqlite_connection = sqlite3.connect('books.db')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from books where book_id = ?"""
        cursor.execute(sql_select_query, (id,))
        records = cursor.fetchall()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
    return list(records)


# print(get_book_info(1)) # check work

# удаление данных по id книги
def delete_book(id):
    try:
        sqlite_connection = sqlite3.connect('books.db')
        cursor = sqlite_connection.cursor()

        sql_delete_same_id = """delete from books where book_id = ?"""
        cursor.execute(sql_delete_same_id, (id,))

        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# добавление книги по всем параметрам, неизвестные параметры нужно указывать при передаче данных как None
def add_book(book_id, genres, main_genre, title, pub_year, publisher, ratings_count, book_average_rating, cover_page,
             book_url, is_ebook, num_pages, book_description, mod_title):
    try:
        sqlite_connection = sqlite3.connect('books.db')
        cursor = sqlite_connection.cursor()

        delete_book(book_id)

        # (book_id,genres, main genre ,title_without_series,publication_year,publisher,ratings_count,book_average_rating,cover_page,book_url,is_ebook,num_pages,book_description,mod_title)

        sqlite_insert_with_param = """INSERT INTO books
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (
        book_id, genres, title, main_genre, pub_year, publisher, ratings_count, book_average_rating, cover_page,
        book_url, is_ebook, num_pages, book_description, mod_title)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

# пример использования функций:
# add_book(1,"test","test",None,1,"test",0,0,"test","test",0,0,"test","test")
# print(get_book_info(1))
